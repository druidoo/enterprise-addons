# Copyright (C) 2020-Today: Druidoo (<https://www.druidoo.io>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    document_count = fields.Integer('Document', compute='_compute_document_count')

    def _compute_document_count(self):
        read_group_var = self.env['documents.document'].read_group(
            [('lead_id', 'in', self.ids)],
            fields=['lead_id'],
            groupby=['lead_id'])

        document_count_dict = dict((d['lead_id'][0], d['lead_id_count']) for d in read_group_var)
        for record in self:
            record.document_count = document_count_dict.get(record.id, 0)

    def action_view_documents(self):
        self.ensure_one()
        return {
            'name': _('Documents'),
            'res_model': 'documents.document',
            'type': 'ir.actions.act_window',
            'views': [(False, 'kanban')],
            'view_mode': 'kanban',
            'context': {
                "search_default_lead_id": self.id,
                "default_lead_id": self.id,
                "searchpanel_default_folder_id": self.env.ref('crm_lead_documents.documents_lead_folder').id
            },
        }
