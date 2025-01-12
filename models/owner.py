from odoo import models, fields, api

class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(required=1, default='New', size=15)
    phone = fields.Char(required=1)
    address = fields.Char()
    property_ids = fields.One2many('property', 'owner_id')
    vendor = fields.Many2one('res.partner')
    user_id = fields.Many2one('res.users')

    @api.onchange('address')
    def _onchange_address_to_uppercase(self):
        if self.address:
            self.address = self.address.upper()

    # validation type  data tier for name
    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!')
    ]
    line_ids = fields.One2many('owner.line', 'owner_id', string="Lines")

    def action_open_catalog(self):
        """
        This method opens the product selection window.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select Products',
            'view_mode': 'kanban',
            'res_model': 'product.template',
            'target': 'current',
            'context': {
                'default_owner_id': self.id,
            },
        }



class OwnerLine(models.Model):
    _name = 'owner.line'

    owner_id = fields.Many2one('owner', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.template', string="Product", required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    price_unit = fields.Float(string="Unit Price", related="product_id.list_price", readonly=False)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit



