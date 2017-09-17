# -*- coding: utf-8 -*-

import werkzeug

from odoo import http
from odoo.http import request
from odoo.http import Controller
from odoo.addons.bus.controllers.main import BusController


class POSFront(BusController):
    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            new_channel = (request.db, 'ebmerchant_posfront', '1')
            channels.append(new_channel)
        return super(POSFront, self)._poll(dbname, channels, last, options)

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

    @http.route('/posfront/send', type='json', auth='none')
    def posfront_send(self, api_key, event, data):
        config = request.env['posfront.configuration'].sudo().search([('api_key','=',api_key)])
        if config:
            request.env['bus.bus'].sendone((request.session.db, 'ebmerchant_posfront', '1'), (event,data))
            return 'pong'
        else:
            return ''
    

