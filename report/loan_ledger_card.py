from odoo import models, api


class LoanLedgerCardReport(models.AbstractModel):
    _name = 'report.pragtech_loan_advance.loan_ledger_card_id_print'
    _description = "pragtech loan advance ledger card loan report"

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': self.ids,
            'doc_model': 'account.loan',
            'data': data,
            'docs': docids,
            'append': self.get_ledger_cart_vals(docids)
        }

    def get_ledger_cart_vals(self, docids):
        loans = self.env['account.loan'].browse(docids)
        data = []
        for loan in loans:
            principal = sum(loan.installment_id.mapped('capital'))
            interest = sum(loan.installment_id.mapped('interest'))
            penalty = sum(loan.installment_id.mapped('fees'))
            disbursement_loan = [{
                'date': loan.installment_id.mapped('date')[-1],
                'total_capital': principal,
                'total_interest': interest,
                'total_fees': penalty,
                'partner_id': loan.partner_id.name,
                'currency_id': loan.company_id.currency_id,
                'city': loan.partner_id.city,
                'country_id': loan.partner_id.country_id.name,
                'loan_type': loan.loan_type.name,
                'flat_pa': loan.flat_pa,
                'loan_id': loan.loan_id,
                'loan_period': loan.loan_period.name,
                'user_id': loan.user_id.name,
                'loan_amount': loan.loan_amount,
                'bill_date': loan.disbursement_details.bill_date,
                'month': loan.month,
                'release_number': loan.disbursement_details.release_number.name,
            }]
            data.append(disbursement_loan)
            for repayment in loan.repayment_details:
                disbursement_loan.append({
                    'dis_principal': principal,
                    'dis_interest': interest,
                    'dis_penalty': penalty,
                    'pay_date': repayment.release_number.date,
                    'release_number': repayment.release_number.name,
                    'interest': sum(repayment.release_number.line_ids.filtered(
                        lambda x: x.account_id.name.lower() == 'interest on loan').mapped('credit')),
                    'penalty': sum(repayment.release_number.line_ids.filtered(
                        lambda x: x.account_id.name.lower() in ['parking fee']).mapped('credit')),
                    #lambda x: x.account_id.name.lower() in ['parking fee', 'penalty fee']).mapped('credit')),   - fredy meela commented this in order to disable negativity on penalty for his to find a permanent solution
                    'principal': sum(repayment.release_number.line_ids.filtered(
                        lambda x: x.account_id.name.lower() in ['quick loan', 'wezesha loan',
                                                                'emergences loan','school loan','salary loan','staff loan','cwc loan','biashara loan','mshahara loan','business loan']).mapped('credit')),
                    'balance_principal': principal - sum(repayment.release_number.line_ids.filtered(
                        lambda x: x.account_id.name.lower() in ['quick loan', 'wezesha loan',
                                                                'emergences loan','school loan','salary loan','staff loan','cwc loan','biashara loan','mshahara loan','business loan']).mapped('credit')),
                    'balance_interest': interest - sum(repayment.release_number.line_ids.filtered(
                        lambda x: x.account_id.name.lower() == 'interest on loan').mapped('credit')),
                    'balance_penalty': penalty - sum(repayment.release_number.line_ids.filtered(
                        lambda x: x.account_id.name.lower() in ['parking fee', 'penalty fee']).mapped('credit')),
                })
        return data
