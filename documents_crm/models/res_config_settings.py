from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    documents_crm_lead_settings = fields.Boolean(
        related="company_id.documents_crm_lead_settings",
        readonly=False,
        string="CRM Lead"
    )
    crm_lead_folder = fields.Many2one(
        "documents.folder",
        related="company_id.crm_lead_folder",
        readonly=False,
        string="CRM Lead default workspace"
    )
    crm_lead_tags = fields.Many2many(
        "documents.tag",
        "crm_lead_tags_table",
        related="company_id.crm_lead_tags",
        readonly=False
    )

    @api.onchange("crm_lead_folder")
    def on_crm_lead_folder_change(self):
        if self.crm_lead_folder != self.crm_lead_tags.mapped("folder_id"):
            self.crm_lead_tags = False
