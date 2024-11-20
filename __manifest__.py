{
    'name': 'Performance Indicator',
    'version': '17.0',
    'category': 'Human Resources',
    'author': 'Arif Pay',
    'website': 'https://www.arifpay.org',
    'summary': 'Manage employee performance evaluations using KPIs.',
    'depends': ['hr', 'base'],
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
