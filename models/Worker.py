from docutils.nodes import title
from odoo import api, fields, models
from datetime import date
from docxtpl import DocxTemplate, InlineImage, RichText
from docx.shared import Cm
import base64
from io import BytesIO
import os
from odoo.addons.worker.utils import NoAccentVietnamese
from odoo.addons.worker.utils import FormatDateForTaiwanFormat
from odoo.addons.worker.utils import Var


class Worker(models.Model):
    _name = 'worker.worker'
    _description = 'The table for the worker'
    _order = "create_date desc"

    #image
    image = fields.Binary()

    #Form information
    name = fields.Char(
        string="Name",
        required=True,
        translate=True
    )
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
    source = fields.Many2one(
        "worker.source",
        string="Source",
    )
    code = fields.Char(
        store=True,
        readonly=True,
        compute='_compute_code',
        string="Code"
    )
    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        store=True,
        readonly=True
    )
    gender = fields.Selection(
        [
            ("mal", "male"),
            ("fem", "female")
        ],
        string="Gender",
        default="mal"
    )
    idn = fields.Char(string="Identification Number")
    date_of_issue = fields.Date(string="Date of Issue")
    place_of_issue = fields.Many2one(
        "worker.province",
        string="Place Of Issue"
    )
    religion = fields.Many2one(
        "worker.religion",
        string="Religion"
    )
    dob = fields.Date(string="Date Of Birth")
    pob = fields.Many2one(
        "worker.province",
        string="Place of birth"
    )

    #Contact information
    phone_worker = fields.Char(string="Phone")
    province = fields.Many2one(
        "worker.province",
        string="Province"
    )
    district = fields.Many2one(
        "worker.district",
        domain="[('province_id', '=', province)]",
        string="District"
    )
    address = fields.Char(string="Address")

    #Health information
    height = fields.Integer(string="Height")
    weight = fields.Integer(string="Weight")
    vision = fields.Many2many(
        "worker.vision.condition",
        "worker_vision_rel",
        "worker_id",
        "condition_id",
        string="Vision Condition"
    )
    r_hand = fields.Selection(
        [
            ("rig", "Right"),
            ("lef", "Left")
        ],
        string="Right Hand",
        default="rig"
    )
    is_alcoholic = fields.Boolean(string="Is Drink Alcohol")
    is_smoking = fields.Boolean(string="Is Smoking")
    is_tattoo = fields.Boolean(string="Is Tattoo")
    has_limb_disability = fields.Boolean(string="Limb disability")
    has_cosmetic_surgery = fields.Boolean(string="Cosmetic surgery")

    #Personal Information
    is_demobilized_soldier = fields.Boolean(string="Is Demobilized Soldier")
    marital_status = fields.Selection(
        [
            ("sin", "Single"),
            ("mar", "Married"),
            ("div", "Divorce"),
        ],
        string="Marital Status",
        default="sin"
    )
    year_mar_status = fields.Char(string="Year Married (Divorce, Separated)", default="2000")

    #Educational information
    edu_background = fields.Selection(
        [
            ("non", "None"),
            ("pri", "Primary Education"),
            ("mid", "Middle school"),
            ("hig", "High school"),
            ("vol", "Vocational"),
            ("col", "College"),
            ("uni", "University")
        ],
        string="Education Background",
        default="hig"
    )
    major = fields.Many2one(
        "worker.major",
        string="Major",
    )
    gra_year = fields.Char(string="Graduation year")
    eng_pro = fields.Selection(
        [
            ("low", "Don't Know"),
            ("ave", "Little Bit"),
            ("hig", "Good"),
        ],
        string="English Proficiency",
        default="low",
    )
    chi_pro = fields.Selection(
        [
            ("low", "Don't Know"),
            ("ave", "Little Bit"),
            ("hig", "Good"),
        ],
        string="Chinese Proficiency",
        default="low",
    )

    #Worker Relative
    father_name = fields.Char(string="Father Name")
    father_birth = fields.Integer(string="Birth Year")
    father_age = fields.Integer(
        readonly=True,
        compute="_compute_age_relatives",
        string="Age"
    )
    father_job = fields.Many2one(
        "worker.job",
        string = "Job",
    )
    # ----
    mother_name = fields.Char(string="Mother Name")
    mother_birth = fields.Integer(string="Birth Year")
    mother_age = fields.Integer(
        readonly=True,
        compute="_compute_age_relatives",
        string="Age"
    )
    mother_job = fields.Many2one(
        "worker.job",
        string="Job",
    )
    #---
    partner_name = fields.Char(string="Partner Name")
    partner_birth = fields.Integer(string="Birth Year")
    partner_age = fields.Integer(
        readonly=True,
        compute="_compute_age_relatives",
        string="Age"
    )
    partner_job = fields.Many2one(
        "worker.job",
        string="Job",
    )
    #---
    children_ids = fields.One2many(
        "worker.children",
        "worker_id",
        string="Children Info"
    )
    #---
    relative_in_Taiwan_name = fields.Char(string="Relative In Taiwan Name")
    relationship_with_relative_in_Taiwan = fields.Many2one(
        "worker.relationship",
        string="Relation Ship With Relative In Taiwan",
    )
    relative_in_Taiwan_job = fields.Many2one(
        "worker.job",
        string = "Job",
    )
    num_of_sib = fields.Integer(string="Number of Siblings")
    birth_order = fields.Integer(string="Birth Order")



    #Work experience
    work_in_noise = fields.Boolean(string="Worked in noise before?")
    been_to_taiwan = fields.Boolean(string="Been to Taiwan?")
    work_experience = fields.One2many(
        "worker.experience",
        "worker_id",
        string="Worker Experience Dometic"
    )

    #Procedure progress
    has_passport = fields.Boolean(string="Passport")
    has_judiciary = fields.Boolean(string="Judiciary")
    has_health_certificate = fields.Boolean(string="Health Certificate")

    #Study at the center
    tuition_fees = fields.Integer(string="Tuition Fees")
    enroll_day = fields.Date(string="Enrollment Day")
    evaluation = fields.Text(string="Note", translate=True)

    #Humam Resource
    broke = fields.Many2one(
        "worker.broke",
        string="Broke"
    )
    recruiter = fields.Many2one(
        "worker.recruiter",
        string="Recruiter"
    )

    is_created_this_year = fields.Boolean(
        string="Created This Year",
        compute="_compute_is_created_this_year",
        search="_search_created_this_year"
    )

    is_created_this_month = fields.Boolean(
        string="Created This Month",
        compute="_compute_is_created_this_month",
        search="_search_created_this_month"
    )

    is_created_last_month = fields.Boolean(
        string="Created Last Month",
        compute="_compute_is_created_last_month",
        search="_search_created_last_month"
    )

    process_translate = fields.Char(
        string="Process Translate",
        compute="_compute_process_translate",
    )

    process_trans_store = fields.Float(
        string="Process Translate",
        store=True,
    )


    def has_Taiwan_relative(self):
        if self.relative_in_Taiwan_name or self.relative_in_Taiwan_job or self.relationship_with_relative_in_Taiwan:
            return True
        return False


    @api.depends("dob")
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.dob:
                record.age = today.year - record.dob.year
            else:
                record.age = 0

    def _sub_com_age_relatives(self, bidth_year):
        if bidth_year <= 0:
            return 0
        else:
            return date.today().year - bidth_year

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
            rec.is_created_this_year = rec.create_date and rec.create_date.year == date.today().year

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
            rec.is_created_this_month = rec.create_date and rec.create_date.month == date.today().month

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
            rec.is_created_last_month = rec.create_date and rec.create_date.month == date.today().month - 1

    @api.model
    def _search_created_last_month(self, operator, value):
        if not value:
            return []
        today = date.today()
        start_of_last_month = f"{today.year}-{today.month - 1}-01 00:00:00"
        end_of_last_month = f"{today.year}-{today.month}-01 00:00:00"
        return [('create_date', '>=', start_of_last_month), ('create_date', '<', end_of_last_month)]

    def write(self, vals):
        old_states = {rec.id: rec.state for rec in self}
        res = super().write(vals)

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

        return res

    @api.depends('name',
                 'province',
                 'work_experience',
                 'father_job',
                 'mother_job',
                 'partner_job',
                 'relationship_with_relative_in_Taiwan',
                 'relative_in_Taiwan_job',
                 'major',
                 'broke',
                 'recruiter'
            )
    def _compute_process_translate(self):
        for rec in self:
            fields_to_check = [
                'name',
                'province.name',
                'work_experience.name',
                'father_job.name',
                'mother_job.name',
                'partner_job.name',
                'relationship_with_relative_in_Taiwan.name',
                'relative_in_Taiwan_job.name',
                'major.name',
                'broke.name',
                'recruiter.name'
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

            percent = (count / total) * 100
            rec.process_trans_store = percent

            rec.process_translate = f"{percent:.0f} %" if total > 0 else "0 %"

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
            'name',
            'province.name',
            'work_experience.name',
            'father_job.name',
            'mother_job.name',
            'partner_job.name',
            'relationship_with_relative_in_Taiwan.name',
            'relative_in_Taiwan_job.name',
            'major.name',
            'broke.name',
            'recruiter.name'
        ]

        msg = ""

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
        module_path = os.path.dirname(__file__)
        gender_template = "template_male.docx" if self.gender == "mal" else "template_female.docx"
        template_path = os.path.join(
            module_path, "..", "static", "src", "template", gender_template
        )
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


    def action_download_docx(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/worker/{self.id}/download_docx',
            'target': 'new',
        }



