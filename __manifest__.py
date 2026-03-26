# -*- coding: utf-8 -*-
{
    'name': "Inmobiliaria",

    'summary': """inmobiliaria""",

    'description': """
        Inmobiliaria
    """,

    'author': "aquíH",
    'website': "http://www.aquih.com",

    'category': 'Uncategorized',
    'version': '0.2',

    'depends': ['base','crm','sale','sale_crm'],

    'data': [
        'views/crm_lead_views.xml',
        'views/product_views.xml',
        'views/sale_views.xml',
        'views/res_partner_view.xml',
        'views/account_payment_view.xml',
        'views/report.xml',
        'views/reporte_fha.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'LGPL-3',
}
