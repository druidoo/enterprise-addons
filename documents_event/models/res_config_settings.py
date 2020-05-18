from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    documents_events_settings = fields.Boolean(
        related='company_id.documents_events_settings',
        readonly=False,
        string="Events")
    events_folder = fields.Many2one('documents.folder',
                                    related='company_id.events_folder',
                                    readonly=False,
                                    string="Events default workspace")
    events_tags = fields.Many2many('documents.tag', 'events_tags_table',
                                   related='company_id.events_tags',
                                   readonly=False)

    @api.onchange('events_folder')
    def on_events_folder_change(self):
        if self.events_folder != self.events_tags.mapped('folder_id'):
            self.events_tags = False
