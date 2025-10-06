from odoo import http
from odoo.http import request
from odoo.addons.worker.utils import NoAccentVietnamese

class WorkerController(http.Controller):
    @http.route('/worker/<int:worker_id>/download_docx', type='http', auth='user')
    def download_worker_docx(self, worker_id, **kwargs):
        worker = request.env['worker.worker'].browse(worker_id)
        if not worker.exists():
            return request.not_found()

        # tạo file bytes
        file_stream = worker.generate_docx_bytes()
        name_file = NoAccentVietnamese.no_accent_vietnamese(worker.name.replace(' ', '')) + "_" + worker.code
        filename = f"{name_file}.docx"

        return request.make_response(
            file_stream.getvalue(),
            headers=[
                ('Content-Typeeee', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
                ('Content-Disposition', f'attachment; filename="{filename}"'),
            ]
        )