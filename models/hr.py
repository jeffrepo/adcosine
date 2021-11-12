# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
import logging
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, AccessError
from dateutil.relativedelta import *
import calendar

class hr_employee(models.Model):
    _inherit = 'hr.employee'

    residencia_letras = fields.Char('Residencia Letras contrato')
