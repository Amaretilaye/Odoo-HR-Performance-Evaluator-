from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class PerformanceEvaluation(models.Model):
    _name = 'hr.performance.evaluation'
    _description = 'Performance Evaluation'

    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    department_id = fields.Many2one('hr.department', string="Department", readonly=False)
    manager_id = fields.Many2one('hr.employee', string="Manager", readonly=False)
    job_id = fields.Many2one('hr.job', string="Job Position", readonly=False)
    kpi_id = fields.Many2one('hr.kpi', string="KPI", required=True, domain="[('job_id', '=', job_id)]")
    period = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half_yearly', 'Half-Yearly'),
        ('yearly', 'Yearly'),
    ], string="Evaluation Period", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved')
    ], default='draft', string='State')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    deadline = fields.Date(string="Deadline")
    evaluation_line_ids = fields.One2many(
        'hr.performance.evaluation.line', 'evaluation_id', string="Evaluation Lines"
    )
    name = fields.Char(string="Reference", readonly=True)
    performance_score = fields.Float(
        string="Average Score", compute='_compute_performance_score', store=True, group_operator="avg"
    )
    evaluation_alert_id = fields.Many2one(
        'evaluation.alert', string="Evaluation Alert",
        domain=[('active', '=', True)], required=True
    )







    @api.constrains('period', 'evaluation_alert_id')
    def _check_period_active(self):
        """
        Validates that the selected period matches one of the active periods
        in the related evaluation alerts.
        """
        for record in self:
            # Search for active alerts that match the selected period
            matching_alerts = self.env['evaluation.alert'].search([
                ('active', '=', True),
                ('period', '=', record.period)
            ])

            # Raise an error if no matching active alerts are found
            if not matching_alerts:
                raise ValidationError(
                    f"The selected period '{record.period}' is not valid for any active evaluation alert. "
                    f"Please ensure there is at least one active alert with this period."
                )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_alert = self.env['evaluation.alert'].search([('active', '=', True)], limit=1)
        if active_alert:
            defaults.update({
                'evaluation_alert_id': active_alert.id,
                'start_date': active_alert.start_date,
                'end_date': active_alert.end_date,
                'deadline': active_alert.deadline,
                'period': active_alert.period,
            })
        return defaults

    def action_submit(self):
        for record in self:
            if record.state != 'draft':
                raise UserError('You can only submit evaluations in draft state.')
            record.state = 'submitted'

    def action_approve(self):
        for record in self:
            if record.state != 'submitted':
                raise UserError('You can only approve evaluations in submitted state.')
            record.state = 'approved'

    @api.depends('evaluation_line_ids.final_rating', 'evaluation_line_ids.weight')
    def _compute_performance_score(self):
        for record in self:
            total_weighted_score_sum = sum(
                line.final_rating * line.weight for line in record.evaluation_line_ids
            )
            total_weight_sum = sum(
                line.weight for line in record.evaluation_line_ids
            )
            record.performance_score = (
                total_weighted_score_sum / total_weight_sum if total_weight_sum else 0.0
            )

    @api.model
    def create(self, vals):
        year = (
            datetime.strptime(vals['start_date'], "%Y-%m-%d").year
            if 'start_date' in vals and vals['start_date']
            else datetime.now().year
        )
        sequence = self.env['ir.sequence'].next_by_code('performance.evaluation.sequence') or '0001'
        vals['name'] = f"PE/{sequence}/{year}"
        return super().create(vals)

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.job_id = self.employee_id.job_id
            self.manager_id = self.employee_id.parent_id
            self.department_id = self.employee_id.department_id
        else:
            self.manager_id = False
            self.department_id = False
            self.job_id = False



    @api.onchange('kpi_id')
    def _onchange_kpi_id(self):
        if self.kpi_id:
            self.evaluation_line_ids = [(5, 0, 0)]
            evaluation_lines = [
                (0, 0, {
                    'key_performance_area': line.key_performance_area,
                    'name': line.name,
                    'weight': line.weight,

                })
                for line in self.kpi_id.kpi_line_ids.filtered(lambda l: getattr(l, f'is_{self.period}', False))
            ]
            self.evaluation_line_ids = evaluation_lines


class PerformanceEvaluationLine(models.Model):
    _name = 'hr.performance.evaluation.line'
    _description = 'Performance Evaluation Line'

    evaluation_id = fields.Many2one(
        'hr.performance.evaluation', string="Performance Evaluation", ondelete='cascade'
    )
    key_performance_area = fields.Char(string="Key Performance Area")
    weight = fields.Float(string="Weight")
    employee_self_mark = fields.Float(string="Employee Self-Mark")
    manager_mark = fields.Float(string="Manager Mark")
    final_rating = fields.Float(string="Final Rating", compute='_compute_final_rating', store=True)
    name = fields.Text(string="Description")


    @api.depends('employee_self_mark', 'manager_mark')
    def _compute_final_rating(self):
        for line in self:
            if line.employee_self_mark and line.manager_mark:
                line.final_rating = (line.employee_self_mark + line.manager_mark) / 2
            else:
                line.final_rating = 0.0
