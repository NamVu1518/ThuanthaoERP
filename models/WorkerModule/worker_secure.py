from odoo import fields, models, api
from odoo.exceptions import AccessError
from .worker_action import WorkerAction


def check_permission(func, group_xml_id):
    def wrapper(self, *args, **kwargs):
        if not self.env.user.has_group(group_xml_id):
            raise AccessError("You are not allowed to perform this action on approved records.")
        return func(self, *args, **kwargs)
    return wrapper

WorkerAction.action_approve_form = check_permission(WorkerAction.action_approve_form, 'worker.group_worker_manager')


class WorkerSecure(models.Model):
    _inherit = "worker.worker"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if self.env.user.has_group("worker.group_worker_manager"):
                self.create_code(record, True)
                self.change_form_status(record, "app")
            else:
                self.create_code(record, False)
                self.change_form_status(record, "pen")
        return records
