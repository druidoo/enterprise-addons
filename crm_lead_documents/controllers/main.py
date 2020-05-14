# Copyright (C) 2020-Today: Druidoo (<https://www.druidoo.io>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64
import json
import logging

from odoo import http
from odoo.addons.documents.controllers.main import ShareRoute
from odoo.http import request
from odoo.tools.translate import _

logger = logging.getLogger(__name__)


class ShareRoute(ShareRoute):
    @http.route('/documents/upload_attachment', type='http', methods=['POST'], auth="user")
    def upload_document(self, folder_id, ufile, document_id=False, partner_id=False, **kw):
        """Completely Overwrite this method to set lead id when create new document from any lead / opportunity"""
        files = request.httprequest.files.getlist('ufile')
        result = {'success': _("All files uploaded")}
        if document_id:
            document = request.env['documents.document'].browse(int(document_id))
            ufile = files[0]
            try:
                data = base64.encodestring(ufile.read())
                mimetype = self._neuter_mimetype(ufile.content_type, http.request.env.user)
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
                    mimetype = self._neuter_mimetype(ufile.content_type, http.request.env.user)
                    datas = base64.encodebytes(ufile.read())
                    document_vals = {
                        'name': ufile.filename,
                        'mimetype': mimetype,
                        'datas': datas,
                        'folder_id': int(folder_id),
                        'partner_id': int(partner_id)
                    }
                    # Custom: Set lead id for document when create new document from lead / opportunity
                    if kw.get('lead_id'):
                        document_vals.update({
                            'lead_id': int(kw['lead_id'])
                        })
                    vals_list.append(document_vals)
                except Exception as e:
                    logger.exception("Fail to upload document %s" % ufile.filename)
                    result = {'error': str(e)}
            request.env['documents.document'].create(vals_list)

        return json.dumps(result)