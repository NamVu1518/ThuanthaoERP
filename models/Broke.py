from odoo import fields, models, api


class Broke(models.Model):
    _name = 'worker.broke'
    _description = 'Description'

    name = fields.Char(String="Broke", required=True, translate=True)

