#!/usr/bin/env python
# -*- encoding: utf-8 -*-


{
    'name' : 'Loan Management Advance',
    "version" : "12.2",
    'category': 'Finance',
    'summary': "Loan Management",
    "depends" : ['base', 'account', 'account_voucher','crm','mail'],
    "author" : "Pragmatic Techsoft Pvt. Ltd.",
    "description": """Loan Management System
    * Integrated to Accounting System
    * Usefull for any type of Loans - Home, Business, Personal
    * Clean Varification Process for Proofs 
    * Workflow for Loan Approval/Rejection
    * Reports related to the Loans, Documents, Loan Papers
    * Dynamic Interest Rates Calculation
    """,
    "init_xml" : [],
    ],
    "data" : [
        "security/loan_security.xml",
        "security/ir.model.access.csv",
        "data/mail_template.xml",
        "data/loan_classifications_data.xml",
        "data/loan_default_stages.xml",
        "report/loan_report_view.xml",
        "views/loan_extended_view.xml",
        "views/loan_asset.xml",
        "views/loan_payment_view.xml",
        "wizard/payment_receipt_wizard.xml",
        "views/loan_view.xml",
        "views/loan_dashboard.xml",
        "views/loantype_view.xml",
        "views/loan_sequence.xml",
        "views/loan_report.xml",
        "views/loan_scheduler.xml",
        "views/classifications_view.xml",
        "views/aec_loan_asset.xml",
        "views/loan_stages_view.xml",
        "views/main_loan_view.xml",
        "wizard/wiz_download_report_view.xml",
        "views/report_menu.xml",
        "views/loan_portal_template.xml",
        "views/crm_view.xml",
        "wizard/disbursement_wizard_view.xml",
        "report/report_pragtech_payment_receipt.xml",
        "report/payment_receipt_report_view.xml",
        "report/loan_info.xml",
        "report/loan_cust_info.xml",
        "report/merge_letter.xml",
        "wizard/loan_disbursement.xml",
        "report/disbursement_report.xml",
        "report/expected_repayment_report.xml",
        "report/loan_repayment_report.xml",
        "report/active_loan_by_officer.xml",
        "report/loan_ledger_card.xml",

       
    ],
    "installable": True,
    'images': ['images/main_screenshot.png'],
}
