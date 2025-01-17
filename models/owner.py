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

    # def action_open_catalog(self):
    #     """
    #     This method opens the product selection window.
    #     """
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Select Products',
    #         'view_mode': 'kanban,form',
    #         'res_model': 'product.template',
    #         'target': 'current',
    #         'context': {
    #             'default_owner_id': self.id,
    #         },
    #     }
    def action_open_catalog(self):
        """
        This method opens the product selection window.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select Products',
            'view_mode': 'kanban,form',
            'res_model': 'product.product',
            'target': 'current',
            'context': {
                'default_owner_id': self.id,
            },
            'views': [
                (self.env.ref('app_one.view_product_template_kanban_owner').id, 'kanban'),
                (self.env.ref('product.product_normal_form_view').id, 'form'),
            ],
        }


class OwnerLine(models.Model):
    _name = 'owner.line'

    owner_id = fields.Many2one('owner', required=True, ondelete='cascade')
    product_ids = fields.Many2one('product.product', string="Product", required=True)
    quantity_product = fields.Integer(string="Quantity")
    price_units = fields.Float(string="Unit Price", related="product_id.list_price", readonly=False)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends('quantity_product', 'price_units')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity_product * line.price_unit

    @api.depends('subtotal')
    def _compute_complete_total(self):
        for line in self:
            line.total = line.subtotal

