# -*- coding: utf-8 -*-
# from odoo import http


# class Cbs(http.Controller):
#     @http.route('/cbs/cbs/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cbs/cbs/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cbs.listing', {
#             'root': '/cbs/cbs',
#             'objects': http.request.env['cbs.cbs'].search([]),
#         })

#     @http.route('/cbs/cbs/objects/<model("cbs.cbs"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cbs.object', {
#             'object': obj
#         })
