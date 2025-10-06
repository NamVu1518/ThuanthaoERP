from odoo import fields, models, api


class Source(models.Model):
    _name = 'worker.source'
    _description = 'Source'

    name = fields.Char(string='Source', required=True)
