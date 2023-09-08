from odoo import models, api
import datetime
from datetime import datetime

class LoanRepaymentReport(models.AbstractModel):
    _name = 'report.pragtech_loan_advance.repayment_loan_report_id'
    _description = "pragtech loan advance repayment loan report id"

    @api.model
    def _get_report_values(self, docids, data=None):
        docids = data.get('from_wizard', False) and data.get('docids') or docids
        
        return {
            'doc_ids': self.ids,
            'doc_model': 'account.loan',
            'data': data,
            'docs': docids,
            'append': self.prepare_values(docids)
        }

    def prepare_values(self, docids):
        loans = self.env['account.loan'].browse(docids)
        data = {}
        [data.update({user: []}) for user in loans.mapped('user_id.name')]
        print("=data.keys()==",data.keys())
        re_ids = []
        lst =[]
#         for user in data.keys():
#             userids = self.env['res.users'].search([('name','=',user)])
#             loans_rs = loans.search([('user_id','=',userids.id)])
           
        for loan in loans:
            for repayment in loan.repayment_details:
                pay_date = datetime.strftime(repayment.pay_date, 
                                           '%Y-%m-%d')
                if self._context.get('date_from') and self._context.get('date_to'):
                    if pay_date >= self._context.get('date_from') \
                        and pay_date <=self._context.get('date_to'):
                        if repayment.id not in lst:
                            lst.append(repayment.id)
                            if repayment not in re_ids:
                                re_ids.append(repayment)
                elif self._context.get('date_from')  and not self._context.get('date_to'):
                    if pay_date >= self._context.get('date_from'):
                        if repayment.id not in lst:
                            lst.append(repayment.id)
                            if repayment not in re_ids:
                                re_ids.append(repayment)
                elif not self._context.get('date_from')  and  self._context.get('date_to'):
                    if pay_date <= self._context.get('date_from'):
                        if repayment.id not in lst:
                            lst.append(repayment.id)
                            if repayment not in re_ids:
                                re_ids.append(repayment)
        print("===re_ids==",re_ids)
        if re_ids:
            lst_2 = []
            for repayment  in re_ids:
                if repayment.release_number.name not in lst_2:
                    lst_2.append(repayment.release_number.name)
                    vals = {
                    'user_id': repayment.loan_id.user_id.name,
                    'user_len': repayment.release_number.ref and len(repayment.release_number.ref),
                    'currency_id': repayment.loan_id.company_id.currency_id,
                    'loan_id': repayment.release_number.ref,
                    'release_number': repayment.release_number.name,
                    'partner_id': repayment.loan_id.partner_id.name,
                    'pay_date': repayment.release_number.date,
                    'interest': sum(repayment.release_number.line_ids.filtered(
                        lambda x: x.account_id.name.lower() == 'interest on loan').mapped('credit')),
                    'penalty': sum(repayment.release_number.line_ids.filtered(
                        lambda x: x.account_id.name.lower() in ['parking fee', 'penalty fee']).mapped('credit')),
                    'principal': sum(repayment.release_number.line_ids.filtered(
                        lambda x: x.account_id.name.lower() in ['quick loan', 'wezesha loan',
                                                                'emergences loan','school loan','salary loan','staff loan','cwc loan','biashara loan','mshahara loan','business loan','soft loan']).mapped('credit')),
                    }
                    print("==data==",data)
                    data.get(repayment.loan_id.user_id.name).append(vals)
                        
        return data
