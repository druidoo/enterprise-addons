from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    documents_vehicle_settings = fields.Boolean(
        related="company_id.documents_vehicle_settings",
        readonly=False,
        string="Vehicle"
    )
    vehicle_folder = fields.Many2one(
        "documents.folder",
        related="company_id.vehicle_folder",
        readonly=False,
        string="Vehicle default workspace",
    )
    vehicle_tags = fields.Many2many(
        "documents.tag",
        "vehicle_tags_table",
        related="company_id.vehicle_tags",
        readonly=False,
    )

    @api.onchange('vehicle_folder')
    def on_vehicle_folder_change(self):
        if self.vehicle_folder != self.vehicle_tags.mapped("folder_id"):
            self.vehicle_tags = False
