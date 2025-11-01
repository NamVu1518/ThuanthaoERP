from odoo import fields, models, api
from datetime import date
from odoo.addons.worker.utils import Var


class WorkerAction(models.Model):
    _inherit = "worker.worker"


    def _sub_com_age_relatives(self, bidth_year):
        if bidth_year <= 0:
            return 0
        else:
            return date.today().year - bidth_year


    @api.depends("dob")
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.dob:
                record.age = today.year - record.dob.year
            else:
                record.age = 0


    @api.depends("father_birth", "mother_birth", "partner_birth")
    def _compute_age_relatives(self):
        for rec in self:
            rec.father_age = rec._sub_com_age_relatives(rec.father_birth)
            rec.mother_age = rec._sub_com_age_relatives(rec.mother_birth)
            rec.partner_age = rec._sub_com_age_relatives(rec.partner_birth)


    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.state:
            state_count = record.env["worker.worker_state_count"].search(
                [("state", "=", record.state)], limit=1
            )
            record.code = state_count.create_new_code()
        return record


    @api.depends('create_date')
    def _compute_is_created_this_year(self):
        for rec in self:
            rec.is_created_this_year = (rec.create_date
                                        and rec.create_date.year == date.today().year)


    @api.model
    def _search_created_this_year(self, operator, value):
        if not value:
            return []
        today = date.today()
        start_of_year = f"{today.year}-01-01 00:00:00"
        return [('create_date', '>=', start_of_year)]


    @api.depends('create_date')
    def _compute_is_created_this_month(self):
        for rec in self:
            rec.is_created_this_month = (rec.create_date
                                         and rec.create_date.month == date.today().month)


    @api.model
    def _search_created_this_month(self, operator, value):
        if not value:
            return []
        today = date.today()
        start_of_this_month = f"{today.year}-{today.month}-01 00:00:00"
        return [('create_date', '>=', start_of_this_month)]


    @api.depends('create_date')
    def _compute_is_created_this_month(self):
        for rec in self:
            rec.is_created_last_month = (rec.create_date
                                         and rec.create_date.month == date.today().month - 1)


    @api.model
    def _search_created_last_month(self, operator, value):
        if not value:
            return []
        today = date.today()
        start_of_last_month = f"{today.year}-{today.month - 1}-01 00:00:00"
        end_of_last_month = f"{today.year}-{today.month}-01 00:00:00"
        return \
            [
                ('create_date', '>=', start_of_last_month),
                ('create_date', '<', end_of_last_month)
            ]


    @api.depends('process_trans_store')
    def _compute_process_translate(self):
        for rec in self:
            rec.process_translate = f"{rec.process_trans_store:.0f} %"


    @api.depends('name', 'province', 'work_experience', 'father_job', 'mother_job',
                 'partner_job', 'relationship_with_relative_in_Taiwan',
                 'relative_in_Taiwan_job', 'major', 'broke', 'recruiter'
            )
    def _compute_process_trans_store(self):
        for rec in self:
            fields_to_check = [
                'name', 'province.name', 'work_experience.name', 'father_job.name',
                'mother_job.name', 'partner_job.name', 'relationship_with_relative_in_Taiwan.name',
                'relative_in_Taiwan_job.name', 'major.name', 'broke.name', 'recruiter.name'
            ]
            total = 0
            count = 0

            for path in fields_to_check:
                root = rec.mapped(path)
                if not root:
                    continue

                trans = rec.with_context(lang='zh_TW').mapped(path)
                total += 1
                if trans and root != trans:
                    count += 1

            rec.process_trans_store = (count / total) * 100 if total > 0 else 0


    def action_check_info(self):
        self.ensure_one()
        self._compute_process_translate()
        if self.process_translate == "100 %":
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': Var.vietnameese_dict.get(Var.EnumVietnamese.TRANSLATE_SUCCESS_ALL),
                    'message': "",
                    'type': Var.toast_type_dict.get(Var.EnumToastType.SUCCESS),
                    'sticky': False,
                }
            }


    def action_download_docx(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/worker/{self.id}/download_docx',
            'target': 'new',
        }


    def action_check_info(self):
        self.ensure_one()
        self._compute_process_translate()
        if self.process_translate == "100 %":
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': Var.vietnameese_dict.get(Var.EnumVietnamese.TRANSLATE_SUCCESS_ALL),
                    'message': "",
                    'type': Var.toast_type_dict.get(Var.EnumToastType.SUCCESS),
                    'sticky': False,
                }
            }

        fields_to_check = [
            'name', 'province.name', 'work_experience.name', 'father_job.name', 'mother_job.name',
            'partner_job.name', 'relationship_with_relative_in_Taiwan.name',
            'relative_in_Taiwan_job.name', 'major.name', 'broke.name', 'recruiter.name'
        ]

        for path in fields_to_check:
            root = self.mapped(path)
            trans = self.with_context(lang='zh_TW').mapped(path)

            if not root:
                continue

            if not trans or (trans and root == trans):
                msg += (str(Var.vietnameese_dict.get(Var.check_process_dict.get(path))) + ", ")

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': Var.vietnameese_dict.get(Var.EnumVietnamese.NOT_YET_TRANSLATE),
                'message': msg,
                'type': Var.toast_type_dict.get(Var.EnumToastType.WARNING),
                'sticky': False,
            }
        }


    def on_change_state_records(self, old_states, vals):
        if 'state' in vals:
            for rec in self:
                old_state = old_states[rec.id]
                new_state = rec.state

                if old_state:
                    old_state_count = rec.env['worker.worker_state_count'].search(
                        [('state', '=', old_state)], limit=1
                    )
                    old_state_count.delete_one()

                if new_state:
                    new_state_count = rec.env['worker.worker_state_count'].search(
                        [('state', '=', new_state)], limit=1
                    )
                    rec.code = new_state_count.create_new_code()
                else:
                    rec.code = ""


    def write(self, vals):
        old_states = {rec.id: rec.state for rec in self}
        res = super().write(vals)
        self.on_change_state_records(old_states, vals)

        return res





