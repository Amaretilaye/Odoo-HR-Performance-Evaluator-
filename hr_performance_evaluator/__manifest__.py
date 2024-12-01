{
    'name': 'HR Performance Evaluator',
    'version': '17.0',
    'category': 'Human Resources',
    'author': 'Amare Tilaye',
    'website': 'https://www.amaretilaye.netlify.app',
    'license': 'LGPL-3',
    'images': ['static/description/cover.png'],
    'summary': 'Manage employee performance evaluations using KPIs.',
    'depends': ['hr', 'base', 'mail', 'contacts', ],
    'description': """

This module is designed to streamline the process of performance evaluation and reporting, providing HR teams with powerful tools to manage and track employee performance.

    """,

    'data': [
        'views/kpi_view.xml',
        'views/performance_evaluation .xml',
        'views/hr_score.xml',
        'views/evaluation_alert_views.xml',
        'views/performance_evaluation_report.xml',

        'data/data.xml',
        'data/kpi.xml',
        'data/email_template_evaluation_alert.xml',

        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
