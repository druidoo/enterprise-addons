from odoo import fields, models, _


class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = ["crm.lead", "documents.mixin"]

    def _get_document_tags(self):
        return self.company_id.crm_lead_tags

    def _get_document_folder(self):
        return self.company_id.crm_lead_folder

    def _check_create_documents(self):
        return self.company_id.documents_crm_lead_settings \
            and super()._check_create_documents()

    document_count = fields.Integer(compute='_compute_document_count')

    def _compute_document_count(self):
        Attachment = self.env['ir.attachment']
        for crm_lead in self:
            crm_lead.document_count = Attachment.search_count([
                ('res_model', '=', 'crm.lead'), ('res_id', '=', crm_lead.id),
            ])

    def action_see_documents(self):
        self.ensure_one()
        return {
            'name': _('Documents'),
            'res_model': 'documents.document',
            'type': 'ir.actions.act_window',
            'views': [(False, 'kanban')],
            'view_mode': 'tree,kanban',
            'domain': [
                ('res_id', 'in', self.ids),
                ('res_model', '=', 'crm.lead'),
            ],
            'context': {
                "search_default_res_id": self.id,
                "search_default_res_model": "crm.lead",
                "default_res_id": self.id,
                "default_res_model": "crm.lead",
                "searchpanel_default_folder_id":
                    self.company_id.crm_lead_folder.id,
            },
        }
