odoo.define('documents_res_model_helper.EventDocumentsKanbanController', function (require) {
"use strict";

    var DocumentsKanbanController = require('documents.DocumentsKanbanController');
    var core = require('web.core');
    var _t = core._t;

    DocumentsKanbanController.include({
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
            if (context) {
                if (context.default_partner_id) {
                    data.append('partner_id', context.default_partner_id);
                }
                if (context.default_owner_id) {
                    data.append('owner_id', context.default_owner_id);
                }
                if (context.default_res_id) {
                    data.append('res_id', context.default_res_id);
                }
                if (context.default_res_model) {
                    data.append('res_model', context.default_res_model);
                }
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
                xhr.open('POST', '/documents/upload_attachment_common');
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
    });

});
