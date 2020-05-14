odoo.define('crm_lead_documents.DocumentsKanbanController', function (require) {
"use strict";
var core = require('web.core');
var DocumentsKanbanController = require('documents.DocumentsKanbanController');
DocumentsKanbanController.include({
    //Completely Overwrite this method to set lead id in context when upload new document from any lead / opportunity
    async _processFiles(files, documentID) {
        const uploadID = _.uniqueId('uploadID');
        const folderID = this._searchPanel.getSelectedFolderId();
        const context = this.model.get(this.handle, { raw: true }).getContext();

        if (!folderID && !documentID) { return; }
        if (!files.length) { return; }

        const data = new FormData();

        data.append('csrf_token', core.csrf_token);
        data.append('folder_id', folderID);
        if (documentID) {
            if (files.length > 1) {
                // preemptive return as it doesn't make sense to upload multiple files inside one document.
                return;
            }
            data.append('document_id', documentID);
        }
        if (context && context.default_partner_id) {
            data.append('partner_id', context.default_partner_id);
        }
        if (context && context.default_lead_id) {
            data.append('lead_id', context.default_lead_id);
        }
        for (const file of files) {
            data.append('ufile', file);
        }
        let title = files.length + ' Files';
        let type;
        if (files.length === 1) {
            title = files[0].name;
            type = files[0].type;
        }
        const prom = new Promise(resolve => {
            const xhr = this._createXHR();
            xhr.open('POST', '/documents/upload_attachment');
            if (documentID) {
                this._makeReplaceProgress(uploadID, documentID, xhr);
            } else {
                this._makeNewProgress(uploadID, folderID, xhr, title, type);
            }
            const progressPromise = this._attachProgressBars();
            xhr.onload = async () => {
                await progressPromise;
                resolve();
                let result = {error: xhr.status};
                if (xhr.status === 200) {
                    result = JSON.parse(xhr.response);
                }
                if (result.error) {
                    this.do_notify(_t("Error"), result.error, true);
                }
                this._removeProgressBar(uploadID);
            };
            xhr.onerror = async () => {
                await progressPromise;
                resolve();
                this.do_notify(xhr.status, _.str.sprintf(_t('message: %s'), xhr.reponseText), true);
                this._removeProgressBar(uploadID);
            };
            xhr.send(data);
        });
        return prom;
    },
    //Completely Overwrite this method to set lead id in context when upload new document from any lead / opportunity
    _onRequestFile: function (ev) {
        ev.preventDefault();
        var self = this;
        var context = this.model.get(this.handle, {raw: true}).getContext();
        this.do_action('documents.action_request_form', {
            additional_context: {
                default_partner_id: context.default_partner_id || false,
                default_lead_id: context.default_lead_id || false,
                default_folder_id: this._searchPanel.getSelectedFolderId(),
                default_tag_ids: [[6, 0, this._searchPanel.getSelectedTagIds()]],
            },
            on_close: function () {
                self.reload();
            },
        });
    },
    //Completely Overwrite this method to set lead id in context when upload new document url from any lead / opportunity
    _onUploadFromUrl: function (ev) {
        ev.preventDefault();
        var self = this;
        var context = this.model.get(this.handle, {raw: true}).getContext();
        this.do_action('documents.action_url_form', {
            additional_context: {
                default_partner_id: context.default_partner_id || false,
                default_lead_id: context.default_lead_id || false,
                default_folder_id: this._searchPanel.getSelectedFolderId(),
                default_tag_ids: [[6, 0, this._searchPanel.getSelectedTagIds()]],
            },
            on_close: function () {
                self.reload();
            },
        });
    },
});
})