from odoo import fields, models, api


class Major(models.Model):
    _name = 'worker.major'
    _description = 'Description'

    name = fields.Char(String="Major", required=True, translate=True)

