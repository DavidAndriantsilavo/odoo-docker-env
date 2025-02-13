# -*- coding: utf-8 -*-
{
    'name': "EASY DELIVERY API",

    'summary': "EASY DELIVERY API",

    'description': """
        Module used for API management, used for the API connexion between odoo and easy-delivery.
    """,

    'author': "David.A",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['website_sale', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'data/ir_config_parameters.xml',
        'views/stock_views.xml',
        'views/easy_delivery_api_configuration_views.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
}

