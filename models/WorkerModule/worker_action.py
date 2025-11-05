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
        self._compute_process_trans_store()
        for rec in self:
            rec.process_translate = f"{rec.process_trans_store:.0f} %"


    def _is_install_lang(self):
        Lang = self.env['res.lang']
        lang_vi = Lang.search([('code', '=', 'vi_VN')], limit=1)
        lang_zh = Lang.search([('code', '=', 'zh_TW')], limit=1)

        if not (lang_vi and lang_zh):
            return False
        return True


    @api.depends(
        'name', 'province', 'work_experience', 'father_job', 'mother_job',
        'partner_job', 'relationship_with_relative_in_Taiwan',
        'relative_in_Taiwan_job', 'major', 'broke', 'recruiter'
    )
    def _compute_process_trans_store(self):
        if not self._is_install_lang():
            return

        fields_to_check = [
            'name', 'province.name', 'work_experience.name', 'father_job.name',
            'mother_job.name', 'partner_job.name', 'relationship_with_relative_in_Taiwan.name',
            'relative_in_Taiwan_job.name', 'major.name', 'broke.name', 'recruiter.name'
        ]

        for rec in self:
            total = 0
            count = 0

            for path in fields_to_check:
                root = rec.with_context(lang='vi_VN').mapped(path)
                trans = rec.with_context(lang='zh_TW').mapped(path)

                if not root:
                    continue

                total += 1
                root_str = str(root)
                trans_str = str(trans)

                if trans_str and root_str != trans_str:
                    count += 1

            rec.process_trans_store = (count / total) * 100 if total > 0 else 0


    def action_download_docx(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/worker/{self.id}/download_docx',
            'target': 'new',
        }


    def _send_client_msg(self, title, msg, type):
        return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': title,
                    'message': msg,
                    'type': type,
                    'sticky': False,
                }
            }


    def action_check_info(self):
        self.ensure_one()

        if not self._is_install_lang():
            return self._send_client_msg(
                Var.vietnamese_dict.get(Var.EnumVietnamese.LANGUAGE_CHANGE_ERROR),
                "",
                Var.toast_type_dict.get(Var.EnumToastType.WARNING)
            )

        self._compute_process_trans_store()
        self._compute_process_translate()
        if self.process_translate == "100 %":
            return self._send_client_msg(
                Var.vietnamese_dict.get(Var.EnumVietnamese.TRANSLATE_SUCCESS_ALL),
                "",
                Var.toast_type_dict.get(Var.EnumToastType.SUCCESS)
            )

        fields_to_check = [
            'name', 'province.name', 'work_experience.name', 'father_job.name', 'mother_job.name',
            'partner_job.name', 'relationship_with_relative_in_Taiwan.name',
            'relative_in_Taiwan_job.name', 'major.name', 'broke.name', 'recruiter.name'
        ]

        msg = ""
        for path in fields_to_check:
            root = self.with_context(lang='vi_VN').mapped(path)
            trans = self.with_context(lang='zh_TW').mapped(path)

            if not root:
                continue

            if not trans or (trans and str(root) == str(trans)):
                msg += (str(Var.vietnamese_dict.get(Var.check_process_dict.get(path))) + ", ")

        return self._send_client_msg(
            Var.vietnamese_dict.get(Var.EnumVietnamese.NOT_YET_TRANSLATE),
            msg,
            Var.toast_type_dict.get(Var.EnumToastType.WARNING)
        )


    def action_approve_form(self):
        self.ensure_one()
        new_rec = self.copy()
        self.unlink()

        return self._send_client_msg(
            Var.vietnamese_dict.get(Var.EnumVietnamese.APPROVED_SUCCESSFULLY),
            "",
            Var.toast_type_dict.get(Var.EnumToastType.SUCCESS)
        )


    def action_change_lang(self):
        user = self.env.user

        if not self._is_install_lang():
            return self._send_client_msg(
                Var.vietnamese_dict.get(Var.EnumVietnamese.LANGUAGE_CHANGE_ERROR),
                "",
                Var.toast_type_dict.get(Var.EnumToastType.WARNING)
            )

        user.lang = 'vi_VN' if user.lang == 'zh_TW' else 'zh_TW'

        return {
            'type': 'ir.actions.client',
            'tag': 'reload_context',  # reload toàn webclient, không redirect
        }


    def write(self, vals):
        old_states = {rec.id: rec.state for rec in self}
        res = super().write(vals)
        self.on_change_state_records(old_states, vals)
        return res





