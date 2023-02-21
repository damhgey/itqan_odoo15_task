from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    product_points_total = fields.Float(string='Product Points Total', compute='_compute_product_points_total', store=True)

    @api.depends('order_line.product_points')
    def _compute_product_points_total(self):
        for order in self:
            product_points_total = 0
            for line in order.order_line:
                product_points_total += line.product_points
            order.product_points_total = product_points_total


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_points = fields.Float(string="Product Points", compute='_compute_product_points', store=True)

    @api.depends('product_id', 'product_uom_qty')
    def _compute_product_points(self):
        for line in self:
            product_points_subtotal = 0
            product_points_id = self.env['product.points'].search([('product_id', '=', line.product_id.id), ('state', '=', 'confirm')], limit=1, order="end_date DESC")
            if product_points_id:
                product_points_subtotal = product_points_id.points * line.product_uom_qty
            line.product_points = product_points_subtotal
