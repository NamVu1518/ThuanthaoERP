from odoo import api, fields, models

class VisionCondition(models.Model):
    _name = 'worker.vision.condition'
    _description = 'The table for the vision condition'

    name = fields.Char(string='Vision Condition Name', required=True, translate=True)
    code = fields.Char(string='Code', required=True)



