from odoo import models, fields, api
import datetime
from datetime import datetime

class KPI(models.Model):
    _name = 'hr.kpi'
    _description = 'KPI for Job Position'

    name = fields.Char(string='KPI Template', required=True)
    kpi_line_ids = fields.One2many('hr.kpi.line', 'kpi_id', invsible=True)
    job_id = fields.Many2one('hr.job', string='Job Position', required=True)



class KPIline(models.Model):
    _name = 'hr.kpi.line'
    _description = 'KPI Line for Job Position'

    key_performance_area = fields.Char(string="Key Performance Area")
    # description = fields.Char(string="Description")
    weight = fields.Float(string='Weight', default=10.0)
    kpi_id = fields.Many2one('hr.kpi', string='KPI', required=True)
    serial_number = fields.Char("SN", compute='_compute_serial_number', store=True)
    name = fields.Char('Description')


    is_monthly = fields.Boolean(string="Monthly", default=False)
    is_quarterly = fields.Boolean(string="Quarterly", default=False)
    is_half_yearly = fields.Boolean(string="Half-Yearly", default=False)
    is_yearly = fields.Boolean(string="Yearly", default=False)


