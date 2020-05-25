from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _domain_company(self):
        company = self.env.company
        return ['|', ('company_id', '=', False), ('company_id', '=', company)]

    documents_crm_lead_settings = fields.Boolean(default=True)
    crm_lead_folder = fields.Many2one(
        "documents.folder",
        string="CRM Lead Workspace",
        domain=_domain_company,
        default=lambda self:
            self.env.ref(
                "documents_crm_lead_folder",
                raise_if_not_found=False
            )
        )
    crm_lead_tags = fields.Many2many("documents.tag", "crm_lead_tags_table")
