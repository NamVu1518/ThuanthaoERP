from odoo import fields, models, api
from io import BytesIO
from odoo.addons.worker.utils import NoAccentVietnamese
from odoo.addons.worker.utils import FormatDateForTaiwanFormat
from odoo.addons.worker.utils import Var
from docxtpl import DocxTemplate, InlineImage, RichText
import base64
from docx.shared import Cm


class WorkerLogic(models.Model):
    _inherit = "worker.worker"

    def has_Taiwan_relative(self):
        if (self.relative_in_Taiwan_name
                or self.relative_in_Taiwan_job
                or self.relationship_with_relative_in_Taiwan):
            return True
        return False


    def image_base64_convert(self, base64_img, doc=None, height_cm=4.0):
        if not base64_img or not doc:
            return None

        image_bytes = BytesIO(base64.b64decode(base64_img))
        return InlineImage(doc, image_bytes, height=Cm(height_cm))


    def print_checkbox(self, bool_val):
        if bool_val:
            return Var.CHECKBOX_TICK
        return Var.CHECKBOX_UNTICK


    def print_color_text(self, text, color):
        rt = RichText()
        rt.add(text, color=color)
        return rt


    def generate_docx_bytes(self):
        """Hàm chính: render template, uncheck checkbox, trả về DOCX BytesIO."""
        self.ensure_one()

        # 1. Load template DOCX
        # module_path = os.path.dirname(__file__)
        # gender_template = "template_male.docx" if self.gender == "mal" else "template_female.docx"
        # template_path = os.path.join(
        #     module_path, "..", "static", "src", "template", gender_template
        # )
        template_path = Var.template_path_dict.get(Var.EnumGender.MALE) \
                            if self.gender == "mal" \
                                else Var.template_path_dict.get(Var.EnumGender.FEMALE)
        doc = DocxTemplate(template_path)

        # 2. Build context
        dom_exps = self.work_experience.filtered(lambda e: e.dom_or_abr == 'dom')
        abr_exps = self.work_experience.filtered(lambda e: e.dom_or_abr == 'abr')

        context = {
            "ENGLISH_NAME": NoAccentVietnamese.no_accent_vietnamese(self.name).upper() if self.name else "",
            "CODE": self.code if self.code else "",
            "TAIWAN_NAME": self.with_context(lang='zh_TW').name or "",
            "ADDRESS": (Var.vietnam_zone_dict.get(self.province.zone) + "/" + self.province.with_context(lang='zh_TW').name) if self.province else "",
            "BIRTH_DATE": self.dob.strftime("%Y/%m/%d") if self.dob else "",
            "AGE": self.age,
            "HEIGHT": self.height,
            "WEIGHT": self.weight,
            "IMAGE": self.image_base64_convert(self.image, doc, height_cm=4.8),
            "sin": self.print_color_text(Var.married_dict.get("sin"), Var.red_color) if self.marital_status == 'sin' else self.print_color_text(Var.married_dict.get("sin"), Var.blue_color),
            "mar": self.print_color_text(Var.married_dict.get("mar"), Var.red_color) if self.marital_status == 'mar' else self.print_color_text(Var.married_dict.get("mar"), Var.blue_color),
            "div": self.print_color_text(Var.married_dict.get("div"), Var.red_color) if self.marital_status == 'div' else self.print_color_text(Var.married_dict.get("div"), Var.blue_color),
            "NOR": self.print_color_text(Var.eye_condition_dict.get("NOR"), Var.blue_color) if any(vis for vis in self.vision) else self.print_color_text(Var.eye_condition_dict.get("NOR"), Var.red_color),
            "MYO": self.print_color_text(Var.eye_condition_dict.get("MYO"), Var.red_color) if any(vis.code == "MYO" for vis in self.vision) else self.print_color_text(Var.eye_condition_dict.get("MYO"), Var.blue_color),
            "BLC": self.print_color_text(Var.eye_condition_dict.get("BLC"), Var.red_color) if any(vis.code == "BLC" for vis in self.vision) else self.print_color_text(Var.eye_condition_dict.get("BLC"), Var.blue_color),
            "o1": self.print_checkbox(self.gender == 'mal'),
            "o2": self.print_checkbox(self.gender == 'fem'),
            "o4": self.print_color_text(Var.CHECKBOX_TICK, Var.red_color) if self.is_smoking else self.print_color_text(Var.CHECKBOX_UNTICK, Var.blue_color),
            "o3": self.print_checkbox(not self.is_smoking),
            "o6": self.print_color_text(Var.CHECKBOX_TICK, Var.red_color) if self.is_alcoholic else self.print_color_text(Var.CHECKBOX_UNTICK, Var.blue_color),
            "o5": self.print_checkbox(not self.is_alcoholic),
            "o8": self.print_color_text(Var.CHECKBOX_TICK, Var.red_color) if self.is_tattoo else self.print_color_text(Var.CHECKBOX_UNTICK, Var.blue_color),
            "o7": self.print_checkbox(not self.is_tattoo),
            "o10": self.print_color_text(Var.CHECKBOX_TICK, Var.red_color) if self.has_cosmetic_surgery else self.print_color_text(Var.CHECKBOX_UNTICK, Var.blue_color),
            "o9": self.print_checkbox(not self.has_cosmetic_surgery),
            "o12": self.print_color_text(Var.CHECKBOX_TICK, Var.red_color) if self.has_limb_disability else self.print_color_text(Var.CHECKBOX_UNTICK, Var.blue_color),
            "o11": self.print_checkbox(not self.has_limb_disability),
            "o14": self.print_color_text(Var.CHECKBOX_TICK, Var.red_color) if self.is_demobilized_soldier else self.print_color_text(Var.CHECKBOX_UNTICK, Var.blue_color),
            "o13": self.print_checkbox(not self.is_demobilized_soldier),
            "o15": self.print_color_text(self.print_checkbox(True), Var.red_color) if self.marital_status == 'sin' else self.print_color_text(self.print_checkbox(False), Var.blue_color),
            "o16": self.print_color_text(self.print_checkbox(True), Var.red_color) if self.marital_status == 'mar' else self.print_color_text(self.print_checkbox(False), Var.blue_color),
            "o17": self.print_color_text(self.print_checkbox(True), Var.red_color) if self.marital_status == 'div' else self.print_color_text(self.print_checkbox(False), Var.blue_color),
            "o18": self.print_color_text(self.print_checkbox(False), Var.blue_color) if any(vis for vis in self.vision) else self.print_color_text(self.print_checkbox(True), Var.red_color),
            "o19": self.print_color_text(self.print_checkbox(True), Var.red_color) if any(vis.code == "MYO" for vis in self.vision) else self.print_color_text(self.print_checkbox(False), Var.blue_color),
            "o20": self.print_color_text(self.print_checkbox(True), Var.red_color) if any(vis.code == "BLC" for vis in self.vision) else self.print_color_text(self.print_checkbox(False), Var.blue_color),
            "o21": self.print_color_text(self.print_checkbox(True), Var.red_color) if self.r_hand == 'rig' else self.print_color_text(self.print_checkbox(False), Var.blue_color),
            "o22": self.print_color_text(self.print_checkbox(True), Var.red_color) if self.r_hand == 'lef' else self.print_color_text(self.print_checkbox(False), Var.blue_color),
            "o25": self.print_color_text(self.print_checkbox(True), Var.red_color) if self.has_Taiwan_relative() else self.print_color_text(self.print_checkbox(False), Var.blue_color),
            "o24": self.print_checkbox(not self.has_Taiwan_relative()),
            "o29": self.print_checkbox(self.eng_pro == 'low'),
            "o30": self.print_checkbox(self.eng_pro == 'ave'),
            "o31": self.print_checkbox(self.eng_pro == 'hig'),
            "o26": self.print_checkbox(self.chi_pro == 'low'),
            "o27": self.print_checkbox(self.chi_pro == 'ave'),
            "o28": self.print_checkbox(self.chi_pro == 'hig'),
            "o33": self.print_color_text(Var.CHECKBOX_TICK, Var.red_color) if self.religion else self.print_color_text(Var.CHECKBOX_UNTICK, Var.blue_color),
            "o32": self.print_checkbox(not self.religion),
            "RH": self.print_color_text(Var.hand_dict.get("rig"), Var.red_color) if self.r_hand == 'rig' else self.print_color_text(Var.hand_dict.get("rig"), Var.blue_color),
            "LH": self.print_color_text(Var.hand_dict.get("lef"), Var.red_color) if self.r_hand == 'lef' else self.print_color_text(Var.hand_dict.get("lef"), Var.blue_color),
            "oy33": self.print_color_text(Var.YES, Var.red_color) if self.religion else self.print_color_text(Var.YES, Var.blue_color),
            "oy4": self.print_color_text(Var.YES, Var.red_color) if self.is_smoking else self.print_color_text(Var.YES, Var.blue_color),
            "oy6": self.print_color_text(Var.YES, Var.red_color) if self.is_alcoholic else self.print_color_text(Var.YES, Var.blue_color),
            "oy8": self.print_color_text(Var.YES, Var.red_color) if self.is_tattoo else self.print_color_text(Var.YES, Var.blue_color),
            "oy10": self.print_color_text(Var.YES, Var.red_color) if self.has_cosmetic_surgery else self.print_color_text(Var.YES, Var.blue_color),
            "oy12": self.print_color_text(Var.YES, Var.red_color) if self.has_limb_disability else self.print_color_text(Var.YES, Var.blue_color),
            "oy14": self.print_color_text(Var.YES, Var.red_color) if self.is_demobilized_soldier else self.print_color_text(Var.YES, Var.blue_color),
            "oy25": self.print_color_text(Var.YES, Var.red_color) if self.has_Taiwan_relative() else self.print_color_text(Var.YES, Var.blue_color),


            "F_A": self.father_age if self.father_age > 0 else '',
            "FAT_JOB": (self.father_job.with_context(lang='zh_TW').name or "") if self.father_job else '',
            "M_A": self.mother_age if self.mother_age > 0 else '',
            "MOT_JOB": (self.mother_job.with_context(lang='zh_TW').name or "") if self.mother_job else '',
            "P_A": self.partner_age if self.partner_age > 0 else '',
            "PAR_JOB": (self.partner_job.with_context(lang='zh_TW').name or "") if self.partner_job else '',
            "RWTWR": (self.relationship_with_relative_in_Taiwan.with_context(lang='zh_TW').name or "") if self.relationship_with_relative_in_Taiwan else '',
            "TWR_JOB": (self.relative_in_Taiwan_job.with_context(lang='zh_TW').name or "") if self.relative_in_Taiwan_job else '',
            "SIB": self.num_of_sib if self.num_of_sib >= 0 else '',
            "BIR_ORD": self.birth_order if self.birth_order >= 0 else '',
            "CHILD_NUM": len(self.children_ids),
            "CH1": self.children_ids[0].age if len(self.children_ids) > 0 else '',
            "CH2": self.children_ids[1].age if len(self.children_ids) > 1 else '',
            "CH3": self.children_ids[2].age if len(self.children_ids) > 2 else '',

            "EDU_BAC": Var.edu_background_map.get(self.edu_background) if self.edu_background else '',
            "GRA_YEAR": self.gra_year if self.gra_year else '',
            "MAJOR": self.major.name if self.major else '',

            "RANGE_1": FormatDateForTaiwanFormat.format_date(dom_exps[0].time_range) if len(dom_exps) > 0 else '',
            "RANGE_2": FormatDateForTaiwanFormat.format_date(dom_exps[1].time_range) if len(dom_exps) > 1 else '',
            "RANGE_3": FormatDateForTaiwanFormat.format_date(dom_exps[2].time_range) if len(dom_exps) > 2 else '',
            "RANGE_4": FormatDateForTaiwanFormat.format_date(dom_exps[3].time_range) if len(dom_exps) > 3 else '',
            "RANGE_5": FormatDateForTaiwanFormat.format_date(abr_exps[0].time_range) if len(abr_exps) > 0 else Var.NO,
            "RANGE_6": FormatDateForTaiwanFormat.format_date(abr_exps[1].time_range) if len(abr_exps) > 1 else '',
            "RANGE_7": FormatDateForTaiwanFormat.format_date(abr_exps[2].time_range) if len(abr_exps) > 2 else '',
            "RANGE_8": FormatDateForTaiwanFormat.format_date(abr_exps[3].time_range) if len(abr_exps) > 3 else '',
            "CONTENT_1": (dom_exps[0].with_context(lang='zh_TW').name or '') if len(dom_exps) > 0 else '',
            "CONTENT_2": (dom_exps[1].with_context(lang='zh_TW').name or '') if len(dom_exps) > 1 else '',
            "CONTENT_3": (dom_exps[2].with_context(lang='zh_TW').name or '') if len(dom_exps) > 2 else '',
            "CONTENT_4": (dom_exps[3].with_context(lang='zh_TW').name or '') if len(dom_exps) > 3 else '',
            "CONTENT_5": (abr_exps[0].with_context(lang='zh_TW').name or '') if len(abr_exps) > 0 else '',
            "CONTENT_6": (abr_exps[1].with_context(lang='zh_TW').name or '') if len(abr_exps) > 1 else '',
            "CONTENT_7": (abr_exps[2].with_context(lang='zh_TW').name or '') if len(abr_exps) > 2 else '',
            "CONTENT_8": (abr_exps[3].with_context(lang='zh_TW').name or '') if len(abr_exps) > 3 else '',
            "REASON_1": (dom_exps[0].with_context(lang='zh_TW').reason_for_leaving or '') if len(dom_exps) > 0 else '',
            "REASON_2": (dom_exps[1].with_context(lang='zh_TW').reason_for_leaving or '') if len(dom_exps) > 1 else '',
            "REASON_3": (dom_exps[2].with_context(lang='zh_TW').reason_for_leaving or '') if len(dom_exps) > 2 else '',
            "REASON_4": (dom_exps[3].with_context(lang='zh_TW').reason_for_leaving or '') if len(dom_exps) > 3 else '',
            "REASON_5": (abr_exps[0].with_context(lang='zh_TW').reason_for_leaving or '') if len(abr_exps) > 0 else '',
            "REASON_6": (abr_exps[1].with_context(lang='zh_TW').reason_for_leaving or '') if len(abr_exps) > 1 else '',
            "REASON_7": (abr_exps[2].with_context(lang='zh_TW').reason_for_leaving or '') if len(abr_exps) > 2 else '',
            "REASON_8": (abr_exps[3].with_context(lang='zh_TW').reason_for_leaving or '') if len(abr_exps) > 3 else '',

            "EVALUATION": self.evaluation if self.evaluation else '',
            "RECRUITER": self.recruiter.name if self.recruiter else '',
            "BROKE": self.broke.name if self.broke else '',
        }

        # 3. Render template
        doc.render(context)

        # 6. Mở lại bằng DocxTemplate để trả BytesIO
        # doc = DocxTemplate(output_path)
        doc_bytes = BytesIO()
        doc.save(doc_bytes)
        doc_bytes.seek(0)
        return doc_bytes


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


    def create_code(self, record, is_create):
        if not is_create:
            record.code = "NOCODE"
            return

        if record.state:
            state_count = self.env["worker.worker_state_count"].search(
                [("state", "=", record.state)], limit=1
            )
            record.code = state_count.create_new_code()


    def change_form_status(self, recordset, form_stat):
        for record in recordset:
            if record.form_status == form_stat:
                continue
            else:
                record.form_status = form_stat






