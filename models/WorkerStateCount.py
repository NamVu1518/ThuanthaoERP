from odoo import fields, models, api
from datetime import date
from odoo.addons.worker.utils import Var

class WorkerStateCount(models.Model):
    _name = 'worker.worker_state_count'
    _description = 'Description'

    state = fields.Selection(
        [
            ("ab", "A: New"),
            ("nn", "N: Abroad come back"),
            ("tw", "T: Taiwan come back"),
            ("cd", "C: Designation")
        ],
        string="State",
        default='ab'
    )
    year = fields.Integer()
    count = fields.Integer()
    head_code = fields.Char()


    def reset_zero(self):
        self.count = 0


    def update_last_year(self):
        self.year = date.today().year


    @api.depends("state")
    def set_head_code(self):
        state_code = Var.state_code_dict.get(self.state)
        nth_alphabet = (date.today().year - Var.year_start) % (ord('Z') - ord('A') + 1)
        year_code = nth_alphabet + 65
        self.head_code = str(state_code) + chr(year_code)


    def on_new_year(self):
        self.reset_zero()
        self.update_last_year()
        self.set_head_code()


    def add_count(self):
        self.count = self.count + 1


    def minus_count(self):
        self.count = self.count - 1 if self.count > 0 else 0


    def create_new_code(self):
        if self.year != date.today().year:
            self.on_new_year()
        self.add_count()
        return str(self.head_code) + str(self.count).zfill(4)


    def delete_one(self):
        self.minus_count()

