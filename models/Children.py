from odoo import fields, models, api
from datetime import date


class Children(models.Model):
    _name = 'worker.children'
    _description = 'Worker Children'

    birth_year = fields.Integer(string="Birth Year")

    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        store=True
    )

    worker_id = fields.Many2one(
        comodel_name="worker.worker",
        string="Worker",
        ondelete="cascade"
    )

    @api.depends("birth_year")
    def _compute_age(self):
        current_year = date.today().year
        for rec in self:
            if rec.birth_year:
                rec.age = current_year - rec.birth_year
            else:
                rec.age = 0