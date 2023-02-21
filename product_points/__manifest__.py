# -*- coding: utf-8 -*-
{
    'name': "Product Points",
    'summary': "Product Points",
    'description': """Product Points.""",
    'author': "Ahmed Elsayed",
    'version': '15.0',
    'category': 'Sales',
    'depends': ['sale'],
    'data': [
        'security/product_points_security.xml',
        'security/ir.model.access.csv',
        'data/product_points_data.xml',
        'views/product_points_view.xml',
        'views/sale_order_view.xml',
        'report/product_points_report.xml',
        'report/product_points_report_template.xml',
    ],
    'installable': True,

}
