# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RFQComparison(models.TransientModel):
	_name='rfq.comparison'
	_description = 'RFQ Comparison'

	# product_id = fields.Many2one('product.product','Product')
	# partner_id = fields.Many2one('res.partner','Vendor')
	# product_qty = fields.Float('Product Quantity')
	# price_unit = fields.Float('Unit Price')
	# price_subtotal = fields.Float('Subtotal')
	line_ids = fields.Many2many('purchase.order.line')

	def update(self):
		if self._context.get('active_ids'):
			order_lines=[]
			for line in self.env['purchase.order.line'].browse(self._context.get('active_ids')):
				if line.status == 'confirmed':
					order_lines.append(line.id)

			self.line_ids = order_lines
			return { 
			 'context': self.env.context, 
			 'view_type': 'form', 
			 'view_mode': 'form', 
			 'res_model': 'rfq.comparison', 
			 'res_id': self.id, 
			 'view_id': self.env.ref('purchase_custom.view_rfq_comparison_wizard_form').id, 
			 'type': 'ir.actions.act_window', 
			 'target': 'new', 
				}
	def po_create(self):
		for vendor in set(self.line_ids.mapped('partner_id.id')):
			order_lines = self.line_ids.filtered(lambda r:r.partner_id.id==vendor)
			products=[]
			for line in order_lines:
				products.append((0,0,{
					'name':line.product_id.name,
					'product_id':line.product_id.id,
					'partner_id':vendor,
					'product_qty':line.confirmed_qty,
					'price_unit':line.price_unit,
					'price_subtotal':line.price_subtotal_confirmed,
					'date_planned':fields.Date.today(),
					'product_uom':line.product_uom.id,
					}))
			po = self.env['purchase.order'].create({
				'partner_id':vendor,
				'order_line':products
				})

			po.button_confirm()



class PurchaseOrderLine(models.Model):
	_inherit = 'purchase.order.line'

	status = fields.Selection([('draft','Draft'),('added','Added'),('confirmed','Confimed'),('cancelled','Canceled')],default='draft',string="State")
	confirmed_qty = fields.Float()
	price_subtotal_confirmed = fields.Float('Subtotal Price ',compute='get_subtotal_price_confirmed')

	@api.depends('price_unit','confirmed_qty')
	def get_subtotal_price_confirmed(self):
		for rec in self:
			rec.price_subtotal_confirmed = rec.confirmed_qty*rec.price_unit

	def add(self):
		for rec in self:
			rec.confirmed_qty+=rec.product_qty
			rec.status='added'

	def reset(self):
		for rec in self:
			rec.confirmed_qty-=rec.product_qty
			rec.status='draft'

	def confirm(self):
		for rec in self:
			rec.status='confirmed'

	def cancel(self):
		for rec in self:
			rec.status='cancelled'



class PurchaseRequisition(models.Model):
	_inherit = 'purchase.requisition'

	def compare(self):
		view_id = self.env.ref('purchase_custom.view_rfq_comparison_tree')
		domain = [('order_id.requisition_id','=',self.id),('order_id.state','=','draft')]
		return {
		'name':self.type_id and self.type_id.name or '/',
		'type':'ir.actions.act_window',
		'res_model':'purchase.order.line',
		'view_id':view_id.id,
		'view_mode':'tree',
		'context':{'search_default_group_product':1},
		'domain':domain
		}
class PurchaseRequisitionLine(models.Model):
	_inherit = 'purchase.requisition.line'

	name = fields.Char('Description')
	purchase_category_ids = fields.Many2many('purchase.category',string="Purchase Categories")
	image = fields.Binary(related="product_id.image_small",string="Image")

	@api.onchange('product_id')
	def onchange_product(self):
		if self.product_id:
			self.name = self.product_id.name


class PurchaseCategory(models.Model):
	_name = 'purchase.category'
	_description = 'Purchase Category'

	name = fields.Char('Name',required=True)
	code = fields.Char('Code')
	product_category_ids = fields.Many2many('product.category',string='Product Categories')



class AgreementWizard(models.Model):
	_name = 'agreement.wizard'
	_description = 'Agreement Wizard'
