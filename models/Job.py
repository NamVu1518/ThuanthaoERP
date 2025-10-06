from odoo import fields, models, api


class Job(models.Model):
    _name = 'worker.job'
    _description = 'Description'

    name = fields.Char(string='Job', required=True, translate=True)