# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

# from odoo.report import report_sxw
import time
import datetime
# from openerp import pooler
# from openerp.osv import osv
import odoo
from odoo import fields
from datetime import date
# import mx.DateTime
# from mx.DateTime import RelativeDateTime, now, DateTime, localtime
import datetime
from odoo import fields, api, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

# class loan_details(report_sxw.rml_parse):
class loan_details(models.AbstractModel):
    _name = 'report.pragtech_loan_advance.loan_cust_info'
    _description = "pragtech_loan_advance.loan_cust_info"
     
    s=0.0
    _capital=0.0
    _interest=0.0
    _subtotal=0.0

    @api.model
    def _get_report_values(self, docids, data=None):
        loan = self.env['res.partner'].browse(docids)
        docargs = {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'data': data,
            'docs': loan,
            'time': time,
     
        }
       
        return docargs
