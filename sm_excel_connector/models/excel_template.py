# -*- coding: utf-8 -*-

import secrets
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ExcelTemplate(models.Model):
    _name = 'excel.template'
    _description = 'Excel Export Template'
    _order = 'name'

    name = fields.Char('Template Name', required=True)
    model_id = fields.Many2one(
        'ir.model', string='Model', required=True, ondelete='cascade',
        domain=[('transient', '=', False)],
    )
    model_name = fields.Char(related='model_id.model', string='Model Name', store=True, readonly=True)
    responsible_id = fields.Many2one(
        'res.users', string='Responsible', default=lambda self: self.env.uid,
    )
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company,
    )
    lang = fields.Selection(
        selection='_get_lang_selection', string='Language',
        default=lambda self: self.env.lang or 'en_US',
    )

    field_ids = fields.One2many('excel.template.field', 'template_id', string='Fields')
    domain = fields.Text('Domain Filter', default='[]')

    access_token = fields.Char('Access Token', copy=False, readonly=True)
    export_url = fields.Char('Export URL', compute='_compute_export_url', store=False)

    access_history_ids = fields.One2many('excel.access.history', 'template_id', string='Access History')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('expired', 'Expired'),
    ], string='Status', default='draft', required=True)

    record_count = fields.Integer('Records', compute='_compute_record_count')
    access_count = fields.Integer('Access Count', compute='_compute_access_count')

    @api.model
    def _get_lang_selection(self):
        return self.env['res.lang'].get_installed()

    @api.depends('access_token', 'model_name')
    def _compute_export_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url', '')
        for rec in self:
            if rec.access_token and rec.id:
                rec.export_url = f'{base_url}/excel/export/{rec.id}?token={rec.access_token}'
            else:
                rec.export_url = False

    @api.depends('model_name', 'domain')
    def _compute_record_count(self):
        for rec in self:
            if rec.model_name and rec.model_name in self.env:
                try:
                    domain = self._parse_domain(rec.domain)
                    rec.record_count = self.env[rec.model_name].search_count(domain)
                except Exception:
                    rec.record_count = 0
            else:
                rec.record_count = 0

    def _compute_access_count(self):
        for rec in self:
            rec.access_count = len(rec.access_history_ids)

    def _parse_domain(self, domain_str):
        """Safely parse a domain string."""
        if not domain_str or domain_str.strip() == '[]':
            return []
        try:
            import ast
            domain = ast.literal_eval(domain_str)
            if not isinstance(domain, list):
                return []
            return domain
        except (ValueError, SyntaxError):
            return []

    def action_generate_token(self):
        """Generate a new access token (disconnects all existing spreadsheets)."""
        for rec in self:
            rec.access_token = secrets.token_urlsafe(32)
        return True

    def action_publish(self):
        for rec in self:
            if not rec.field_ids:
                raise UserError(_('Please add at least one field before publishing.'))
            if not rec.access_token:
                rec.action_generate_token()
            rec.state = 'published'
        return True

    def action_set_draft(self):
        self.write({'state': 'draft'})
        return True

    def action_expire(self):
        self.write({'state': 'expired'})
        return True

    def action_flush_history(self):
        """Delete all access history records."""
        self.mapped('access_history_ids').unlink()
        return True

    def action_download_odc(self):
        """Generate and download an ODC file for MS Excel."""
        self.ensure_one()
        if not self.export_url:
            raise UserError(_('Please generate an access token first.'))
        return {
            'type': 'ir.actions.act_url',
            'url': f'/excel/download_odc/{self.id}?token={self.access_token}',
            'target': 'self',
        }

    def action_preview_data(self):
        """Open the export URL in a new browser tab for preview."""
        self.ensure_one()
        if not self.export_url:
            raise UserError(_('Please generate an access token and publish first.'))
        return {
            'type': 'ir.actions.act_url',
            'url': self.export_url,
            'target': 'new',
        }

    def get_export_data(self):
        """Fetch records and return list of dicts with field labels and values."""
        self.ensure_one()
        if not self.field_ids:
            return [], []

        domain = self._parse_domain(self.domain)
        records = self.env[self.model_name].with_context(lang=self.lang).search(domain, limit=10000)

        headers = []
        field_names = []
        for f in self.field_ids.sorted('sequence'):
            headers.append(f.label or f.field_id.field_description)
            field_names.append(f.field_id.name)

        rows = []
        for rec in records:
            row = []
            for fname in field_names:
                val = rec[fname]
                if isinstance(val, models.BaseModel):
                    val = val.display_name or ''
                elif val is False or val is None:
                    val = ''
                row.append(val)
            rows.append(row)

        return headers, rows
