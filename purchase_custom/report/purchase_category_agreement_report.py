from odoo import models,fields,api

class PurchaseCategoryAgreement(models.AbstractModel):
	_name = 'report.purchase_custom.purchase_category_agreement'

	@api.model
	def _get_report_values(self, docids, data=None):
		doc_args={}
		lines=[]
		rec = self.env['purchase.requisition'].browse(docids)
		for category in set(rec.line_ids.mapped('purchase_category_ids')):
			category_lines=rec.line_ids.filtered(lambda r:category.id in r.purchase_category_ids.ids)
			lines.append({'category':category.name,'category_lines':category_lines})
		return {'lines':lines,'rec':rec}
