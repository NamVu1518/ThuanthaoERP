from odoo import fields, models, api


class Relationship(models.Model):
    _name = 'worker.relationship'
    _description = 'Description'

    name = fields.Char(string='Relationship', required=True, translate=True)
