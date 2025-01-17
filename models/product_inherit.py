
from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    _inherit = 'product.product'

    quantity = fields.Float(string="Quantity", default=1.0, widget="integer_button")

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

        existing_line = self.env['owner.line'].search([
            ('owner_id', '=', owner.id),
            ('product_ids', '=', self.id)
        ], limit=1)

        if existing_line:
            existing_line.quantity_product += self.quantity
        else:
            self.env['owner.line'].create({
                'owner_id': owner.id,
                'product_ids': self.id,
                'quantity_product': self.quantity,
                'price_units': self.lst_price,
            })

    def action_remove_product_from_owner_line(self):
        """
        Remove the selected product from the owner's line.
        """
        owner_id = self.env.context.get('default_owner_id')
        if not owner_id:
            raise UserError("Owner not found in context.")

        owner_line = self.env['owner.line'].search([
            ('owner_id', '=', owner_id),
            ('product_ids', '=', self.id)
        ])
        if owner_line:
            owner_line.unlink()

    def increase_quantity(self):
        owner_id = self.env.context.get('default_owner_id')
        if not owner_id:
            raise UserError("Owner not found in context.")

        owner = self.env['owner.line'].browse(owner_id)
        if not owner:
            raise UserError("Owner not found.")

        existing_line = self.env['owner.line'].search([
            ('owner_id', '=', owner.id),
            ('product_ids', '=', self.id)
        ], limit=1)

        if existing_line:
            existing_line.quantity_product += self.quantity

    def decrease_quantity(self):
        owner_id = self.env.context.get('default_owner_id')
        if not owner_id:
            raise UserError("Owner not found in context.")

        owner = self.env['owner.line'].browse(owner_id)
        if not owner:
            raise UserError("Owner not found.")

        existing_line = self.env['owner.line'].search([
            ('owner_id', '=', owner.id),
            ('product_ids', '=', self.id)
        ], limit=1)

        if existing_line:
            existing_line.quantity_product -= self.quantity

    def action_back_to_owner(self):
        """
        Redirects back to the owner.line view.
        """
        owner_id = self.env.context.get('default_owner_id')
        if not owner_id:
            raise UserError("Owner not found in context.")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Owner Line',
            'view_mode': 'form',
            'res_model': 'owner',
            'domain': [('owner_id', '=', owner_id)],
            'target': 'current',
        }



