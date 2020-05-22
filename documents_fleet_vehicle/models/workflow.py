from odoo import models, fields


class WorkflowActionRulevehicle(models.Model):
    _inherit = ["documents.workflow.rule"]

    has_business_option = fields.Boolean(
        default=True,
        compute="_get_business",
    )
    create_model = fields.Selection(
        selection_add=[("fleet.vehicle", "vehicle")]
    )

    def create_record(self, documents=None):
        rv = super(WorkflowActionRulevehicle, self).create_record(
            documents=documents)
        if self.create_model == 'fleet.vehicle':
            create_model_obj = self.env[self.create_model]
            fleet_vehicle_obj = self.env['fleet.vehicle']
            for document in documents:
                fleet_vehicle = fleet_vehicle_obj.browse(document.res_id)
                if fleet_vehicle:
                    new_obj = create_model_obj.create({
                        "name": "New Vehicle from Documents",
                        "model_id": fleet_vehicle.model_id.id,
                    })
                    this_document = document
                    if (
                        (document.res_model or document.res_id) and
                        document.res_model != 'documents.document'
                    ):
                        this_document = document.copy()
                        attachment_id_copy = document.attachment_id.\
                            with_context(no_document=True).copy()
                        this_document.write({
                            'attachment_id': attachment_id_copy.id
                        })
                    this_document.attachment_id.with_context(
                        no_document=True).write({
                            'res_model': self.create_model,
                            'res_id': new_obj.id
                        })
            vehicle_action = {
                'type': 'ir.actions.act_window',
                'res_model': self.create_model,
                'res_id': new_obj.id,
                'name': "new %s" % (self.create_model),
                'view_mode': 'form',
                'views': [(False, "form")],
                'context': self._context,
            }
            return vehicle_action
        return rv
