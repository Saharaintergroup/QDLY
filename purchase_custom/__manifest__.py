# -*- coding: utf-8 -*-
{
    'name': "Purchase Agreement Comparison Custom",

    'summary': """
        Aimed to compare between the different RFQs with in specific purchase agreement""",

    'description': """
        Aimed to compare between the different RFQs with in specific purchase agreement
    """,

    'author': "Sami",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','purchase_requisition'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
