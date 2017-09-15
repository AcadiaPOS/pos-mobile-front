# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Ebmerchant Posfront',
    'version': '1.0',
    'category': 'Point of Sale',
    'sequence': 6,
    'summary': 'POS Front Mobile App Module',
    'description': """
        A module providing functionality for the POS front mobile app
    """,
    'depends': ['web', 'point_of_sale', 'bus'],
    'website': '',
    'data': [
        'views/posfront_templates.xml',
        'views/posfront_views.xml'
    ],
    'installable': True,
    'auto_install': False,
}
