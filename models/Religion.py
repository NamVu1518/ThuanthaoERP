from odoo import fields, models, api


class Religion(models.Model):
    _name = 'worker.religion'
    _description = 'Description'

    name = fields.Char(string="Religion", required=True, translate=True)
    code = fields.Char(string="Code", required=True)
