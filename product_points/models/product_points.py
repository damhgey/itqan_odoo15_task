from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductPoints(models.Model):
    _name = 'product.points'
    _description = 'Product Points'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=True, domain=[('sale_ok', '=', True)])
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    points = fields.Float(string="Points",  required=True, digits=(16, 2), tracking=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirmed'),
                              ('end', 'Ended'),
                              ('cancel', 'Cancelled')],
                             string='Status', readonly=True,  copy=False, default='draft', tracking=True)
    write_state_uid = fields.Many2one('res.users', 'Last Change Status By', index=True, readonly=True)

    def name_get(self):
        result = []
        for rec in self:
            product_name = rec.product_id.display_name
            points = rec.points
            name = '%s (%s)' % (product_name, points)
            result.append((rec.id, name))
        return result

    def write(self, vals):
        if 'state' in vals and self.env.user:
            vals['write_state_uid'] = self.env.user
        return super(ProductPoints, self).write(vals)

    @api.constrains('state')
    def _check_same_product_confirm(self):
        for rec in self:
            product_confirmed = self.search_count([('product_id', '=', rec.product_id.id), ('state', '=', 'confirm')])
            if product_confirmed > 1 and rec.state == 'confirm':
                raise ValidationError(_("It's not allowed to be more than one confirmed product points for the same product."))

    @api.onchange('start_date')
    def onchange_date(self):
        self.end_date = None

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_end(self):
        self.write({'state': 'end'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

    def _cron_end_date_product_points(self):
        product_points = self.search([('end_date', '<', fields.Datetime.now()), ('state', '=', 'confirm')])
        for p_points in product_points:
            try:
                p_points.action_end()
            except:
                pass
