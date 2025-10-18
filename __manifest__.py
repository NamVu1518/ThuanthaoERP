# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Worker',
    'version': '1.0',
    'summary': 'Manage worker information within the company',
    'sequence': 1,
    'description': """
Maneger Worker
====================
Main Features:
--------------
- Store basic worker information: name, date of birth, gender, and address.
- Gender field defined using Selection type.
- Simple structure, ready to be extended (contracts, training, overseas labor management).
- Easy to integrate with other Odoo HR modules.
    """,

    'category': 'Other',
    'depends': [],
    'data': [
        'security/WorkerSecurityView.xml',
        'security/ir.model.access.csv',
        'views/Worker.xml',
        'views/VisionCondition.xml',
        'views/Source.xml',
        'views/Relationship.xml',
        'views/Job.xml',
        'views/Religion.xml',
        'views/Province.xml',
        'views/District.xml',
        'views/Broke.xml',
        'views/Recruiter.xml',
        'views/Major.xml',
        'views/WorkerStateCount.xml',
        'data/province.xml',
        'data/district.xml',
        'data/vision_condition.xml',
        'data/worker_state_count.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'worker/static/src/css/style.css',
        ],
        'worker.report_assets': [
            'worker/static/src/css/worker_report.css',
        ]
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'author': 'Vu Duc Nam - IT Thuan Thao - 0901586025',
}
