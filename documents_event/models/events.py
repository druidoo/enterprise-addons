from odoo import fields, models, _


class Events(models.Model):
    _name = "event.event"
    _inherit = ['event.event', 'documents.mixin']

    def _get_document_tags(self):
        return self.company_id.events_tags

    def _get_document_folder(self):
        return self.company_id.events_folder

    def _check_create_documents(self):
        return self.company_id.documents_events_settings \
            and super()._check_create_documents()

    document_count = fields.Integer(compute='_compute_document_count')

    def _compute_document_count(self):
        Attachment = self.env['ir.attachment']
        for event in self:
            event.document_count = Attachment.search_count([
                ('res_model', '=', 'event.event'), ('res_id', '=', event.id),
            ])

    def action_see_documents(self):
        self.ensure_one()
        return {
            'name': _('Documents'),
            'res_model': 'documents.document',
            'type': 'ir.actions.act_window',
            'views': [(False, 'kanban')],
            'view_mode': 'kanban',
            'domain': [
                ('res_id', 'in', self.ids),
                ('res_model', '=', 'event.event'),
            ],
            'context': {
                "searchpanel_default_folder_id": self.company_id.events_folder,
            },
        }
