
from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    _inherit = 'product.product'

    quantity = fields.Integer(string="Quantity", default=1.0)

    def action_add_product_to_owner_line(self):
        """
        Add the selected product and quantity to the owner line.
        """
        owner_id = self.env.context.get('default_owner_id')
        if not owner_id:
            raise UserError("Owner not found in context.")

        owner = self.env['owner.line'].browse(owner_id)
        if not owner:
            raise UserError("Owner not found.")

        # Create a line in owner.line
        self.env['owner.line'].create({
            'owner_id': owner.id,
            'product_id': self.id,
            'quantity': self.quantity,
            'price_unit': self.list_price,
        })
