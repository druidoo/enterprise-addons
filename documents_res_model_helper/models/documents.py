from odoo import models, api


class Document(models.Model):
    _inherit = "documents.document"

    @api.model
    def create(self, vals):
        new_record = super(Document, self).create(vals)
        res_id = self._context.get('res_id', False)
        res_model = self._context.get('res_model', False)
        if res_id and res_model and new_record.attachment_id:
            new_record.attachment_id.with_context(no_document=True).write({
                'res_model': res_model,
                'res_id': int(res_id),
            })
        return new_record
