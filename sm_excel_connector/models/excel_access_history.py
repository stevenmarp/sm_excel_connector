# -*- coding: utf-8 -*-

from odoo import fields, models


class ExcelAccessHistory(models.Model):
    _name = 'excel.access.history'
    _description = 'Excel Access History'
    _order = 'last_used desc'

    template_id = fields.Many2one('excel.template', string='Template', required=True, ondelete='cascade')
    ip_address = fields.Char('IP Address', readonly=True)
    user_agent = fields.Char('User Agent', readonly=True)
    create_date = fields.Datetime('First Access', readonly=True)
    last_used = fields.Datetime('Last Used', readonly=True, default=fields.Datetime.now)
    frequency_sec = fields.Integer('Frequency (sec)', readonly=True, help='Seconds between last two requests from this IP.')
    times_used = fields.Integer('Times Used', readonly=True, default=1)
