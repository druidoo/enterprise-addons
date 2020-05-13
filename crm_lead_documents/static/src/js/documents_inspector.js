odoo.define('crm_lead_documents.DocumentsInspector', function (require) {
"use strict";
var DocumentsInspector = require('documents.DocumentsInspector');
DocumentsInspector.include({
    _renderFields: function () {
        var res = this._super.apply(this, arguments);
        var options = {mode: 'edit'};
        var proms_lead_id = [];
        if (this.records.length === 1) {
            proms_lead_id.push(this._renderField('lead_id', options));
        }
        Promise.all(proms_lead_id);
        return res;
    },
})
});
