# Copyright (C) 2020-Today: Druidoo (<https://www.druidoo.io>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models, api


class DocumentsDocument(models.Model):
    _inherit = 'documents.document'

    lead_id = fields.Many2one('crm.lead', string="Lead / Opport.")
