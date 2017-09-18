# -*- coding: utf-8 -*-

import werkzeug
import os
import base64

from odoo import http
from odoo.http import request
from odoo.http import Controller
from odoo.addons.bus.controllers.main import BusController
from odoo.modules import get_module_path


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

    @http.route('/posfront/img/<string:order_id>', type='http', auth='user')
    def posfront_img(self, order_id):
        order = request.env['pos.order'].sudo().search([('id','=',order_id)])
        if order:
            signatures_path = get_module_path('ebmerchant_posfront') + '/signatures/'
            folder = signatures_path + order.pos_reference + '/'
            n = 0
            while os.path.exists(folder + str(n+1)):
                n = n + 1
            print 'Path: ' + folder
            if n == 0 or not os.path.exists(folder + str(n)):
                return ''
            else:
                print folder + str(n)
                f = open(folder + str(n), 'r')
                contents = f.read()
                contents = contents.replace('data:image/png;base64,','')
                contents = base64.b64decode(contents)
                f.close()
                return request.make_response(contents, headers=[('Content-Type', 'image/png')])
        else:
            return ''

    @http.route('/posfront/test', type='http', auth='none')
    def test_posfront(self):
        configs = request.env['posfront.configuration']
        configs.broadcast('my_message_here')
        return ''

    @http.route('/posfront/save_signature', type='json', auth='none')
    def posfront_save_signature(self, api_key, order_id, signature):
        #print 'Saving signature for ' + order_id + ', signature: ' + signature
        config = request.env['posfront.configuration'].sudo().search([('api_key','=',api_key)])
        if not config:
            return ''
        signatures_path = get_module_path('ebmerchant_posfront') + '/signatures/'
        folder = signatures_path + order_id + '/'
        if not os.path.exists(folder):
            os.makedirs(folder)
        n = 1
        while os.path.exists(folder + str(n)):
            n = n + 1
        f = open(folder + str(n), 'w')
        f.write(signature)
        f.close()
        return ''

    @http.route('/posfront/send', type='json', auth='none')
    def posfront_send(self, api_key, event, data):
        config = request.env['posfront.configuration'].sudo().search([('api_key','=',api_key)])
        if config:
            request.env['bus.bus'].sendone((request.session.db, 'ebmerchant_posfront', '1'), (event,data))
            return 'pong'
        else:
            return ''
    

