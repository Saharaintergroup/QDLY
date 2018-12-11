# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RFQComparison(models.TransientModel):
	_name='rfq.comparison'

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

	status = fields.Selection([('draft','Draft'),('added','Added'),('confirmed','Confimed'),('cancelled','Canceled')],default='draft')
	confirmed_qty = fields.Float()
	price_subtotal_confirmed = fields.Float('Subtotal',compute='get_subtotal_price_confirmed')

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



class PurchaseRequisitionLine(models.Model):
	_inherit = 'purchase.requisition.line'

	name = fields.Char('Description')

	@api.onchange('product_id')
	def onchange_product(self):
		if self.product_id:
			self.name = self.product_id.name

class PurchaseRequisition(models.Model):
	_inherit = 'purchase.requisition'

	purchase_category_ids = fields.Many2many('purchase.category',string="Purchase Categories")



class PurchaseCategory(models.Model):
	_name = 'purchase.category'

	name = fields.Char('Name',required=True)
	code = fields.Char('Code')
	product_category_ids = fields.Many2many('product.category',string='Product Categories')




# class PurchaseOrder(models.Model):
# 	_inherit = 'purchase.order'

# 	@api.model
# 	def create(self,vals):
# 		if vals.get('requisition_id'):
# 			if vals.get('order_line'):
# 				for line in vals.get('order_line'):
# 					self.env['rfq.comparison'].create({
# 						'requisition_id':vals.get('requisition_id'),
# 						'product_id':line[2].get('product_id'),
# 						'vendor_id':vals.get('partner_id'),
# 						'product_qty':line[2].get('product_qty'),
# 						'price_unit':line[2].get('price_unit'),
# 						'price_subtotal':line[2].get('price_unit')*line[2].get('product_qty')
# 						})
# 		return super(PurchaseOrder,self).create(vals)
