# -*- coding: utf-8 -*-
from odoo import http

# class PurchaseAgreementCustom(http.Controller):
#     @http.route('/purchase_agreement_custom/purchase_agreement_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_agreement_custom/purchase_agreement_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_agreement_custom.listing', {
#             'root': '/purchase_agreement_custom/purchase_agreement_custom',
#             'objects': http.request.env['purchase_agreement_custom.purchase_agreement_custom'].search([]),
#         })

#     @http.route('/purchase_agreement_custom/purchase_agreement_custom/objects/<model("purchase_agreement_custom.purchase_agreement_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_agreement_custom.object', {
#             'object': obj
#         })