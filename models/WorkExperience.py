from odoo import fields, models, api


class WorkExperience(models.Model):
    _name = 'worker.experience'
    _description = 'Work Experience'

    worker_id = fields.Many2one(
        'worker.worker',
        string='Worker ID',
        required=True,
        ondelete="cascade"
    )
    dom_or_abr = fields.Selection(
        [
            ('dom', 'Dometion'),
            ('abr', 'Abroad'),
        ],
        string='Dom/Abr',
        default='dom',
    )
    name = fields.Text(string="Experience", required=True, translate=True)
    time_range = fields.Char(string="Time Range")
    reason_for_leaving = fields.Text(string="Reason For Leaving", translate=True)
