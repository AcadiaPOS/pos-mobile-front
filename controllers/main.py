# -*- coding: utf-8 -*-

import werkzeug

from odoo import http
from odoo.http import request
from odoo.http import Controller
from odoo.addons.bus.controllers.main import BusController


class POSFront(BusController):
    @http.route('/posfront/ping/<string:api_key>', type='http', auth='none')
    def posfront_ping(self, api_key):
        config = request.env['posfront.configuration'].sudo().search([('api_key','=',api_key)])
        if config:
            return 'pong'
        else:
            return ''

    @http.route('/posfront/test', type='http', auth='none')
    def test_posfront(self):
        configs = request.env['posfront.configuration']
        configs.broadcast('my_message_here')
        return ''

