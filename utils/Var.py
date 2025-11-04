from enum import Enum, auto
from odoo.tools.misc import file_path

class EnumGender(Enum):
    MALE = auto()
    FEMALE = auto()

class EnumToastType(Enum):
    WARNING = auto()
    SUCCESS = auto()

class EnumVietnamese(Enum):
    NOT_YET_TRANSLATE = auto()
    NAME = auto()
    FATHER_JOB = auto()
    MOTHER_JOB = auto()
    PARTNER_JOB = auto()
    PROVINCE = auto()
    WORK_EXPERIENCE = auto()
    RELATIONSHIP_WITH_RELATIVE_IN_TAIWAN = auto()
    RELATIVE_IN_TAIWAN_JOB = auto()
    MAJOR = auto()
    BROKE = auto()
    RECRUITER = auto()
    TRANSLATE_SUCCESS_ALL = auto()
    APPROVED_SUCCESSFULLY = auto()
    LANGUAGE_CHANGE_ERROR = auto()

vietnamese_dict = {
    EnumVietnamese.NOT_YET_TRANSLATE: "Chưa dịch",
    EnumVietnamese.NAME: "Tên",
    EnumVietnamese.FATHER_JOB: "Công việc của bố",
    EnumVietnamese.MOTHER_JOB: "Công việc của mẹ",
    EnumVietnamese.PARTNER_JOB: "Công việc của bạn đời",
    EnumVietnamese.PROVINCE: "Tỉnh",
    EnumVietnamese.WORK_EXPERIENCE: "Kinh nghiệm",
    EnumVietnamese.RELATIONSHIP_WITH_RELATIVE_IN_TAIWAN: "Mối quan hệ với người thân ở Đài loan",
    EnumVietnamese.RELATIVE_IN_TAIWAN_JOB: "Công việc của người thân ở Đài Loan",
    EnumVietnamese.MAJOR: "Chuyên ngành",
    EnumVietnamese.BROKE: "Mô giới",
    EnumVietnamese.RECRUITER: "Nhà tuyển dụng",
    EnumVietnamese.TRANSLATE_SUCCESS_ALL: "Hoàn thành phiên dịch",
    EnumVietnamese.APPROVED_SUCCESSFULLY: "Duyệt thành công",
    EnumVietnamese.LANGUAGE_CHANGE_ERROR: "Có lỗi trong quá trình chuyển đổi/sử dụng ngôn ngữ, hãy liên hệ quản trị viên"
}

check_process_dict = {
    'name': EnumVietnamese.NAME,
    'province.name': EnumVietnamese.PROVINCE,
    'work_experience.name': EnumVietnamese.WORK_EXPERIENCE,
    'father_job.name': EnumVietnamese.FATHER_JOB,
    'mother_job.name': EnumVietnamese.MOTHER_JOB,
    'partner_job.name': EnumVietnamese.PARTNER_JOB,
    'relationship_with_relative_in_Taiwan.name': EnumVietnamese.RELATIONSHIP_WITH_RELATIVE_IN_TAIWAN,
    'relative_in_Taiwan_job.name': EnumVietnamese.RELATIVE_IN_TAIWAN_JOB,
    'major.name': EnumVietnamese.MAJOR,
    'broke.name': EnumVietnamese.BROKE,
    'recruiter.name': EnumVietnamese.RECRUITER,
}

toast_type_dict = {
    EnumToastType.WARNING: "WARNING",
    EnumToastType.SUCCESS: "SUCCESS",
}

PRESENT = '現在'
CHECKBOX_UNTICK = "☐"
CHECKBOX_TICK = "☑"
YES = "有"
NO = "無"
edu_background_map = {
    'pri': '國小',
    'mid': '國中',
    'hig': '高中',
    'vol': '二專',
    'col': '三專',
    'uni': '大學',
}
taiwan_zone_dict = {
    'twn': '',
    'twc': '',
    'tws': '',
}
vietnam_zone_dict = {
    'nor': '北部',
    'cen': '中部',
    'sou': '南部',
}
eye_condition_dict = {
    "NOR": "正常",
    "MYO": "近視",
    "BLC": "色盲",
}
married_dict = {
    "sin": "未婚",
    "mar": "已婚",
    "div": "離婚",
}
hand_dict = {
    "rig": "右手",
    "lef": "左手",
}
red_color = "EE0000"
blue_color = "000099"
state_code_dict = {
    "ab": "A",
    "nn": "N",
    "tw": "T",
    "cd": "C",
}
year_start = 2000
template_path_dict = {
    EnumGender.MALE: file_path("worker/static/src/template/template_male.docx"),
    EnumGender.FEMALE: file_path("worker/static/src/template/template_female.docx"),
}




