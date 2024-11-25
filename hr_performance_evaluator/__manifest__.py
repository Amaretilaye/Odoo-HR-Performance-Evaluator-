{
    'name': 'Performance Evaluator',
    'version': '17.0',
    'category': 'Human Resources',
    'author': 'Arif Pay',
    'website': 'https://www.amaretilaye.netlify.app',
    'license': 'LGPL-3',
    'images': ['static/description/cover.png'],
    'summary': 'Manage employee performance evaluations using KPIs.',
    'depends': ['hr', 'base','mail', 'contacts',],
    'description': """
Performance Evaluator for Odoo

Overview:
This module allows HR departments to manage and evaluate employee performance based on KPIs linked to their job positions. It includes features for automatic email alerts, performance evaluation by both employees and managers, and reporting.

Key Features:
1. **KPI Setup in Odoo**:
    - Link KPIs to job positions.
    - Define Key Performance Areas (KPAs) with descriptions.
    - Set evaluation periods (monthly, quarterly, half-yearly, yearly).
    - Adjustable weights for each KPA.
    <img src="/hr_performance_evaluator/static/description/kpi.png" alt="Module Cover Image" style="max-width:100%;"/>


2. **Evaluation Alerts**:
    - **Automatic Email Alerts**: Notifications for the start and end of evaluation periods.
    - **Automatic Deactivation**: Evaluation periods are automatically deactivated after the deadline.
    <img src="/hr_performance_evaluator/static/description/alert.png" alt="Module Cover Image" style="max-width:100%;"/>


3. **Performance Evaluation**:
    - Employees can self-evaluate based on KPIs.
    - Managers can evaluate employees, with both evaluations contributing to the final score.
    - Final scores are calculated as the average of employee and manager marks.
    - Admin approval is required for final scores.
    <img src="/hr_performance_evaluator/static/description/evaluation.png" alt="Module Cover Image" style="max-width:100%;"/>


4. **Performance Report**:
    - **Pivot Report**: View performance data in a pivot table format, summarizing scores by employee or department.
    - **Average Score Calculation**: Calculate and display average scores for employees or departments based on the evaluation period.
    - **Dynamic Filtering**: Filter reports by evaluation period, employee, or department.
    <img src="/hr_performance_evaluator/static/description/report.png" alt="Module Cover Image" style="max-width:100%;"/>

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
