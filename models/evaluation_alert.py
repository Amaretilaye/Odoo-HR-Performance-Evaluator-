from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class EvaluationAlert(models.Model):
    _name = 'evaluation.alert'
    _description = 'Evaluation Alert'

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

    # We no longer need employee_id linked to evaluation, sending to all employees
    employee_id = fields.Many2one('hr.employee', string="Employee")

    def action_send_email(self):
        for record in self:
            try:
                # Send email to all employees in the system
                employees = self.env['hr.employee'].search([('work_email', '!=', False)])

                if not employees:
                    raise UserError(f"No employees with a work email found.")

                # Get the email template reference for the alert notification
                template = self.env.ref('performance_evaluator.email_template_evaluation_alert')
                if not template:
                    raise UserError("Email template for alert notification not found.")

                # Loop through each employee and send an email
                for employee in employees:
                    if not employee.work_email:
                        _logger.warning(f"Employee {employee.name} does not have a work email.")
                        continue

                    try:
                        # Attempt to send the email
                        template.send_mail(record.id, force_send=True)
                        _logger.info(f"Email successfully sent to {employee.work_email} for alert {record.id}.")
                    except Exception as e:
                        _logger.error(
                            f"An error occurred while sending the email to {employee.work_email} for alert {record.id}: {str(e)}")

                # Send success message to the user in Odoo interface
                record.sudo().env.user.notify_info(message="Emails sent successfully to all employees.")

                # Optionally, send a more detailed success message to the user
                _logger.info("All emails were sent successfully.")

            except UserError as e:
                _logger.error(f"UserError: {str(e)}")
                # Show error notification in the Odoo interface
                record.sudo().env.user.notify_error(message=f"UserError: {str(e)}")
                raise e
            except Exception as e:
                _logger.error(f"An error occurred while sending the email for alert {record.id}: {str(e)}")
                # Show a generic error notification in Odoo interface
                record.sudo().env.user.notify_error(
                    message=f"An error occurred while sending the email for alert {record.id}.")
                raise UserError(f"An error occurred while sending the email for alert {record.id}: {str(e)}")
