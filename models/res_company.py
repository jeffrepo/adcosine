# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_company(models.Model):
    _inherit = 'res.company'

    encargado_contrato_id = fields.Many2one('hr.employee','Encargado contrato')
    numero_registro_mercantil = fields.Char('Número de registro mercantil')
    folio = fields.Char('Folio')
    libro = fields.Char('Libro')
    nombre_notario = fields.Char('Nombre notario')
