from odoo import models, fields

class Province(models.Model):
    _name = "worker.province"
    _description = "Province"

    name = fields.Char(string="Province", required=True, translate=True)
    zone = fields.Selection(
        [
            ("nor", "North"),
            ("cen", "Central"),
            ("sou", "South")
        ],
        string="Zone",
        default="nor",
    )
    district_ids = fields.One2many("worker.district", "province_id", string="Districts")


class District(models.Model):
    _name = "worker.district"
    _description = "District"

    name = fields.Char(string="District", required=True, translate=True)
    province_id = fields.Many2one("worker.province", string="Province", required=True)