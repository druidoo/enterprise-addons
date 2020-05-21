from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _domain_company(self):
        company = self.env.company
        return ['|', ('company_id', '=', False), ('company_id', '=', company)]

    documents_events_settings = fields.Boolean(default=True)
    events_folder = fields.Many2one(
        "documents.folder",
        string="Events Workspace",
        domain=_domain_company,
        default=lambda self:
            self.env.ref(
                "documents_events_folder",
                raise_if_not_found=False,
            ),
        )
    events_tags = fields.Many2many("documents.tag", "events_tags_table")
