from odoo import fields, models, api


class Recruiter(models.Model):
    _name = 'worker.recruiter'
    _description = 'Description'

    name = fields.Char(String="Name", required=True, translate=True)

