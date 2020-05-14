# Copyright (C) 2020-Today: Druidoo (<https://www.druidoo.io>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "CRM Lead Documents",
    "summary": "Add documents management for crm lead.",
    'category': 'Sales/CRM',
    "author": "Druidoo",
    "website": "https://www.druidoo.io/",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["crm", "documents"],
    "data": [
        "data/document_data.xml",
        "views/lead_views.xml",
        "views/documents_document_views.xml",
        "views/assets.xml",
    ],
    "installable": True,
}
