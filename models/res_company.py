# -*- coding: utf-8 -*-

from odoo import models, fields, api

class res_company(models.Model):
    _inherit = 'res.company'

    encargado_contrato_id = fields.Many2one('hr.employee','Encargado contrato')
    numero_registro_mercantil = fields.Char('Número de registro mercantil')
    folio = fields.Char('Folio')
    libro = fields.Char('Libro')
    nombre_notario = fields.Char('Nombre notario')
    # SI es colegio otro formato
    colegio = fields.Boolean('Colegio')
    direccion_letras = fields.Char('Direccion letras')
    nombre_encargado = fields.Char('Nombre encargado')
    edad_encargado = fields.Integer('Edad')
    estado_civil_encargado = fields.Char('Estado civil')
    dpi_encargado = fields.Char('DPI')
    direccion_encargado = fields.Char('Direccion encargado')
