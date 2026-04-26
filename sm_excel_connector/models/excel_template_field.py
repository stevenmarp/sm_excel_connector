# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ExcelTemplateField(models.Model):
    _name = 'excel.template.field'
    _description = 'Excel Template Field'
    _order = 'sequence, id'

    template_id = fields.Many2one('excel.template', string='Template', required=True, ondelete='cascade')
    model_id = fields.Many2one(related='template_id.model_id', readonly=True, store=True)
    field_id = fields.Many2one(
        'ir.model.fields', string='Field', required=True, ondelete='cascade',
        domain="[('model_id', '=', model_id), ('ttype', 'not in', ['one2many', 'many2many', 'binary'])]",
    )
    label = fields.Char('Custom Label', help='Leave blank to use the default field label.')
    sequence = fields.Integer('Sequence', default=10)

    @api.onchange('field_id')
    def _onchange_field_id(self):
        if self.field_id and not self.label:
            self.label = self.field_id.field_description
