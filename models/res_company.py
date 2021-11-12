# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_company(models.Model):
    _inherit = 'res.company'

    encargado_contrato_id = fields.Many2one('hr.employee','Encargado contrato')
    nombre_notario = fields.Char('Nombre notario')
