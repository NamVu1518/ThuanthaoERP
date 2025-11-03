from odoo import api, fields, models


class Worker(models.Model):
    _name = 'worker.worker'
    _description = 'The table for the worker'
    _order = "create_date desc"


    form_status = fields.Selection(
        [
            ("pen", "Pending Approval"),
            ("app", "Approval"),
        ],
        readonly=True,
        default='pen',
        string='Form Status'
    )

    #image
    image = fields.Binary()


    #Form information
    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
        index=True
    )
    state = fields.Selection(
        [
            ("ab", "A: New"),
            ("nn", "N: Abroad come back"),
            ("tw", "T: Taiwan come back"),
            ("cd", "C: Designation")
        ],
        string="State",
        default='ab',
        index=True
    )
    source = fields.Many2one(
        "worker.source",
        string="Source",
        index=True,
        ondeleta="set null"
    )
    code = fields.Char(
        store=True,
        readonly=True,
        compute='_compute_code',
        string="Code",
        index=True
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
        string="Place Of Issue",
        ondeleta="set null"
    )
    religion = fields.Many2one(
        "worker.religion",
        string="Religion",
        ondeleta="set null"
    )
    dob = fields.Date(string="Date Of Birth")
    pob = fields.Many2one(
        "worker.province",
        string="Place of birth",
        ondeleta="set null"
    )


    #Contact information
    phone_worker = fields.Char(string="Phone")
    province = fields.Many2one(
        "worker.province",
        string="Province",
        ondelete="set null"
    )
    district = fields.Many2one(
        "worker.district",
        domain="[('province_id', '=', province)]",
        string="District",
        ondeleta="set null"
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
        ondelete="set null"
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
        ondelete="set null"
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
        ondelete="set null"
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
        ondelete="set null"
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
        ondelete="set null"
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
    tuition_fees = fields.Boolean(string="Tuition Fees")
    enroll_day = fields.Date(string="Enrollment Day")
    evaluation = fields.Text(string="Note", translate=True)

    #Humam Resource
    broke = fields.Many2one(
        "worker.broke",
        string="Broke",
        ondelete="set null"
    )
    recruiter = fields.Many2one(
        "worker.recruiter",
        string="Recruiter",
        ondelete="set null"
    )

    #Other
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
        compute="_compute_process_trans_store",
        store=True,
        index=True
    )

