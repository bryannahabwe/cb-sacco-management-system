# -*- coding: utf-8 -*-
{
    'name': "cbs",
    'summary': """Church Billionaire Sacco System""",
    'description': """Church Billionaire Sacco System""",
    'author': "CBS",
    'sequence': 1,
    'website': "",
    'category': 'Other',
    'version': '17.0',
    'depends': ['base'],
    'license': "LGPL-3",
    # always loaded
    'data': [
        'security/cbs_security.xml',
        'security/ir.model.access.csv',
        'views/member_view.xml',
        'views/beneficiary_view.xml',
        'views/monthly_saving_view.xml',
        'views/loan_application_view.xml',
        'views/loan_payment_view.xml',
        'views/report_monthly_savings.xml',
        'report/cbs_report.xml',
        'menu/cbs_menu.xml',
    ],
    'installable': True,
    'application': True,
}
