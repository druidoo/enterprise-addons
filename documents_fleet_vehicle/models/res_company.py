from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _domain_company(self):
        company = self.env.company
        return ['|', ('company_id', '=', False), ('company_id', '=', company)]

    documents_vehicle_settings = fields.Boolean(default=True)
    vehicle_folder = fields.Many2one(
        "documents.folder",
        string="Vehicle Workspace",
        domain=_domain_company,
        default=lambda self:
            self.env.ref(
                "documents_fleet.documents_fleet_folder",
                raise_if_not_found=False,
            ),
        )
    vehicle_tags = fields.Many2many("documents.tag", "vehicle_tags_table")
