import base64
import json
import logging
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.documents.controllers.main import ShareRoute

logger = logging.getLogger(__name__)


class ShareRouteEvent(ShareRoute):

    @http.route('/documents/upload_attachment_common', type='http',
                methods=['POST'], auth="user")
    def upload_document_common(
            self, folder_id, ufile, document_id=False, partner_id=False,
            owner_id=False, res_id=False, res_model=False):
        files = request.httprequest.files.getlist('ufile')
        result = {'success': _("All files uploaded")}
        if document_id:
            document = request.env['documents.document'].browse(
                int(document_id)
            )
            ufile = files[0]
            try:
                data = base64.encodestring(ufile.read())
                mimetype = self._neuter_mimetype(
                    ufile.content_type,
                    http.request.env.user,
                )
                document.write({
                    'name': ufile.filename,
                    'datas': data,
                    'mimetype': mimetype,
                })
            except Exception as e:
                logger.exception("Fail to upload document %s" % ufile.filename)
                result = {'error': str(e)}
        else:
            vals_list = []
            for ufile in files:
                try:
                    mimetype = self._neuter_mimetype(
                        ufile.content_type,
                        http.request.env.user
                    )
                    datas = base64.encodebytes(ufile.read())
                    vals = {
                        'name': ufile.filename,
                        'mimetype': mimetype,
                        'datas': datas,
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id)
                    }
                    if owner_id:
                        vals['owner_id'] = int(owner_id)
                    vals_list.append(vals)
                except Exception as e:
                    logger.exception(
                        "Fail to upload document %s" % ufile.filename
                    )
                    result = {'error': str(e)}
            request.env['documents.document'].with_context(
                res_id=res_id, res_model=res_model).create(vals_list)
        return json.dumps(result)
