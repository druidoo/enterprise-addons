from odoo import fields, models, _


class FleetVehicle(models.Model):
    _name = "fleet.vehicle"
    _inherit = ["fleet.vehicle", "documents.mixin"]

    def _get_document_tags(self):
        return self.company_id.vehicle_tags

    def _get_document_folder(self):
        return self.company_id.vehicle_folder

    def _check_create_documents(self):
        return self.company_id.documents_vehicle_settings \
            and super()._check_create_documents()

    document_count = fields.Integer(compute='_compute_document_count')

    def _compute_document_count(self):
        Attachment = self.env['ir.attachment']
        for fleet_vehicle in self:
            fleet_vehicle.document_count = Attachment.search_count([
                ('res_model', '=', 'fleet.vehicle'),
                ('res_id', '=', fleet_vehicle.id),
            ])

    def action_see_documents(self):
        self.ensure_one()
        return {
            'name': _('Documents'),
            'res_model': 'documents.document',
            'type': 'ir.actions.act_window',
            'views': [(False, 'kanban')],
            'view_mode': 'kanban',
            'context': {
                "search_default_res_id": self.id,
                "search_default_res_model": "fleet.vehicle",
                "default_res_id": self.id,
                "default_res_model": "fleet.vehicle",
                "searchpanel_default_folder_id":
                    self.company_id.vehicle_folder.id,
            },
        }
