from odoo import fields, models, api
from odoo.osv.orm import setup_modifiers
from lxml import etree
import json
import datetime
from datetime import datetime


class LoanDisbursement(models.TransientModel):
    _name = 'loan.report'

    @api.onchange('report')
    def _onchange_report(self):
        for record in self:
            if record.report == 'active_loans_by_loan_officer':
                date =  datetime(2015, 1, 1)
                date = datetime.strftime(date, "%Y-%m-%d")
                record.date_from = date
            
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    report = fields.Selection([('loan_disbursement_report', 'Loan Disbursement Report'),
                               ('active_loans_by_loan_officer', 'Active Loans By Loan Officer'),
                               ('loan_repayment_report', 'Loan Repayment Report'),
                               ('expected_repayments_report', 'Expected Repayments Report')], string="Reports")
    report_type = fields.Selection([('detailed', 'Detailed Report'),
                                    ('summary', 'Summary Report')], string="Report Type")
    loan_product_ids = fields.Many2many(comodel_name="account.loan.loantype", string="Loan Product", )
    loan_officer_boolean = fields.Boolean(string="Group by Loan Officer", default=True)
    #     user_id = fields.Many2one('res.users', string="Loan Officer",)

    users_ids = fields.Many2many('res.users', relation='users_loan_rel',
                                 column1='loan_id',
                                 column2='user_id',
                                 string='Loan Officer')

    @api.model
    def default_get(self, fields_list):
        res = super(LoanDisbursement, self).default_get(fields_list=fields_list)
        res.update({'users_ids': [(6, 0, [self.env.uid])]})
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(LoanDisbursement, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                            submenu=submenu)
        user = self.env['res.users'].browse(self.env.uid)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            node = doc.xpath("//field[@name='users_ids']")[0]
            if user.has_group('pragtech_loan_advance.group_loan_manager'):
                node.set('readonly', '0')
            elif user.has_group('pragtech_loan_advance.group_loan_user'):
                node.set('readonly', '1')
            setup_modifiers(node, res['fields']['users_ids'])
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    def generate_disbursement_report(self):
        if self.report == 'loan_disbursement_report':
            report_id = self.env.ref('pragtech_loan_advance.loan_disbursement_report_wizard').report_action(self)
        if self.report == 'expected_repayments_report':
            report_id = self.env.ref('pragtech_loan_advance.expected_loan_repayment_report_wizard').report_action(self)
        if self.report == 'loan_repayment_report':
            report_id = self.env.ref('pragtech_loan_advance.loan_repayment_report_wizard').with_context(
                {'date_from': self.date_from,
                'date_to': self.date_to}).report_action(None, data={
                'docids': self.get_value(),
                'date_from': self.date_from,
                'date_to': self.date_to,
                'summary': self.report_type,
                'from_wizard': True,
            })
        if self.report == 'active_loans_by_loan_officer':
            report_id = self.env.ref('pragtech_loan_advance.active_loan_by_officer_wizard').report_action(self)
        return report_id

    @api.multi
    def get_value(self):
        res = []
        domain = []
        docargs = []
        e_domain = []
        if self.report == 'loan_disbursement_report':
            if self.date_from:
                domain.append(('disbursement_details.bill_date', '>=', self.date_from))
            if self.date_to:
                domain.append(('disbursement_details.bill_date', '<=', self.date_to))

        if self.report == 'loan_repayment_report':
            if self.date_from:
                domain.append(('repayment_details.pay_date', '>=', self.date_from))
            if self.date_to:
                domain.append(('repayment_details.pay_date', '<=', self.date_to))

        if self.report == 'expected_repayments_report':
            if self.date_from:
                domain.append(('installment_id.date', '>=', self.date_from))
                e_domain.append(('date', '>=', self.date_from))
            if self.date_to:
                domain.append(('installment_id.date', '<=', self.date_to))
                e_domain.append(('date', '<=', self.date_to))

        if self.report == 'active_loans_by_loan_officer':
            if self.date_from:
                domain.append(('disbursement_details.bill_date', '>=', self.date_from))
            if self.date_to:
                domain.append(('disbursement_details.bill_date', '<=', self.date_to))

        users = False
        if self.users_ids:
            loans_obj = self.env['account.loan']
            loans = loans_obj
            for uid in self.users_ids:
                loans += loans_obj.search([('user_id', '=', uid.id)])
            users = loans.mapped('user_id')
        else:
            if self.report != 'loan_repayment_report':
                loans = self.env['account.loan'].search(domain)
                users = loans.mapped('user_id')
                domain = [('disbursement_details.bill_date', '>=', self.date_from),
                          ('disbursement_details.bill_date', '<=', self.date_to),'|', ('state', '=', 'partial'),
                      ('state', '=', 'approved')]
                 

        if self.loan_product_ids:
            loans = self.env['account.loan']
            loan_types = loans
            domain.append(('loan_type', 'in', self.loan_product_ids.ids))
            e_domain.append((('loan_id.loan_type', 'in', self.loan_product_ids.ids)))

#             for type_id in self.loan_product_ids:
#                 
#                 loan_types += loans.search([('loan_type', '=', type_id.id)])
#                 users_loan_type = loan_types.mapped('loan_type')
#                 for rec in users_loan_type:
#                     print('type', rec.name)
        else:
            loans = self.env['account.loan'].search([])
            users_loan_type = loans.mapped('loan_type')
            for rec in users_loan_type:
                print('type', rec.name)
            print('all loan',users_loan_type)

        if self.report == 'loan_repayment_report':
            if users:
                domain.append(('user_id', 'in', users.ids))
            else:
                loans = self.env['account.loan'].search(domain)
                users = loans.mapped('user_id')
                domain.append(('user_id', 'in', users.ids))
            data = self.env['account.loan'].search(domain, order='user_id')
            return data.filtered(
                lambda x: '' not in x.installment_id.mapped('state')).ids


        users = sorted(users, key=lambda x: (x.ref or '', x.name or ''))
        user_loan_dict= {}
        user_loan_lst = []

        for user in users:
            if self.report == 'expected_repayments_report':
                u_domain = e_domain.copy()
                u_domain.insert(0, ('loan_id.user_id', '=', user.id))
                u_domain.append(('state', '!=', 'paid'))
                print("=e_domain==",u_domain)
                data = self.env['account.loan.installment'].search(
                    u_domain)
                user_loan_lst.append({user: data})
        if self.report == 'expected_repayments_report':
            for t in user_loan_lst:
                for key, value in t.items():
                    res.append(key)
                    user_loan_dict.update({key: value})
            docargs.append({'docusign_list': user_loan_dict, 'user_id': res})
            return docargs



        for user in users:
            vdomain = domain.copy()
            vdomain = vdomain[:2]
            vdomain.insert(0, ('user_id', '=', user.id))
            if self.report == 'loan_repayment_report':
                vdomain.append(('state', '=', 'done'))
            if self.report in ('loan_disbursement_report',
                                'active_loans_by_loan_officer') and self.loan_product_ids:
                vdomain.append(('loan_type','in', self.loan_product_ids.ids))
            #data = self.env['account.loan'].search(vdomain)
            if self.report == 'active_loans_by_loan_officer':

                vdomain.append(('state', 'in', ('partial','approved')))
                data = self.env['account.loan'].search(vdomain)

                user_loan_dict.update({user: data})
            data = self.env['account.loan'].search(vdomain)
            if self.report == 'loan_disbursement_report':
                user_loan_dict.update({user: data})
        #    data = self.report == 'expected_repayments_report' and data.filtered(
        #         lambda x: 'paid' not in x.installment_id.mapped('state')) or data
        #     if self.report == 'expected_repayments_report':
        #         user_loan_dict.update({user: data})
        # if self.report == 'expected_repayments_report':
        #     for key, value in user_loan_dict.items():
        #         res.append(key)
        #     docargs.append({'docusign_list': user_loan_dict, 'user_id': res})
        #     return docargs
        if self.report == 'loan_disbursement_report':
            lst= []
            for key, value in user_loan_dict.items():
                lst.append(key)
            print("=user_loan_dict===",user_loan_dict,lst)
            docargs.append({'docusign_list': user_loan_dict, 'user_id': lst})
            return docargs
            
        if self.report == 'active_loans_by_loan_officer':
            for key, value in user_loan_dict.items():
                res.append(key)
            docargs.append({'docusign_list': user_loan_dict, 'user_id': res})
            return docargs
    
