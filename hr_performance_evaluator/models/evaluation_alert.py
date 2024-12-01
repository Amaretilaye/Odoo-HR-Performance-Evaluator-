from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class EvaluationAlert(models.Model):
    _name = 'evaluation.alert'
    _description = 'Evaluation Alert'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    period = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half_yearly', 'Half-Yearly'),
        ('yearly', 'Yearly'),
    ], string="Evaluation Period", required=True)

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    deadline = fields.Date(string="Deadline", required=True)
    active = fields.Boolean(string="Active", default=True)
    evaluation_id = fields.Many2one('hr.performance.evaluation', string="Performance Evaluation", readonly=True)

    employee_id = fields.Many2one('hr.employee', string="Employee")

    def action_send_email(self):
        for record in self:
            try:
                employees = self.env['hr.employee'].search([('work_email', '!=', False)])
                if not employees:
                    raise UserError("No employees with a work email found.")

                # Get the email template
                template = self.env.ref('performance_evaluator.email_template_evaluation_alert')
                if not template:
                    raise UserError("Email template for alert notification not found.")

                for employee in employees:
                    if not employee.work_email:
                        _logger.warning(f"Employee {employee.name} does not have a work email.")
                        continue

                    # Debug: Log sending email attempt
                    _logger.debug(f"Preparing to send email to {employee.work_email} using template {template.id}")

                    # Force send the email
                    template.with_context(
                        email_to=employee.work_email  # Send to individual employee
                    ).send_mail(record.id, force_send=True, raise_exception=True)

                    _logger.info(f"Email successfully sent to {employee.work_email} for alert {record.id}.")

                # Log a success message
                _logger.info("Emails sent successfully to all employees.")

            except UserError as e:
                _logger.error(f"UserError: {str(e)}")
                raise e
            except Exception as e:
                _logger.error(f"An error occurred: {str(e)}")
                raise UserError(f"An error occurred: {str(e)}")
