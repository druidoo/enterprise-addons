odoo.define('crm_lead_documents.DocumentsKanbanView', function (require) {
"use strict";
var DocumentsKanbanView = require('documents.DocumentsKanbanView');
DocumentsKanbanView.include({
    init: function () {
        this._super.apply(this, arguments);
        // add the fields used in the DocumentsInspector to the list of fields to fetch
        var inspectorFields = [
            'lead_id'
        ];
        _.defaults(this.fieldsInfo[this.viewType], _.pick(this.fields, inspectorFields));

        // force fetch of relational data (display_name and tooltip) for related
        // rules to display in the DocumentsInspector
        this.fieldsInfo[this.viewType].available_rule_ids = _.extend({}, {
            fieldsInfo: {
                default: {
                    display_name: {},
                    note: {},
                    limited_to_single_record: {},
                },
            },
            relatedFields: {
                display_name: {type: 'string'},
                note: {type: 'string'},
                limited_to_single_record: {type: 'boolean'},
            },
            viewType: 'default',
        }, this.fieldsInfo[this.viewType].available_rule_ids);
    },
})
});
