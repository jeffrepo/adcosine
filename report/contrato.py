# -*- encoding: utf-8 -*-

from odoo import api, models, fields
from datetime import date
# import datetime
import time
import dateutil.parser
from dateutil.relativedelta import relativedelta
from dateutil import relativedelta as rdelta
from odoo.fields import Date, Datetime
import logging
from operator import itemgetter
import odoo.addons.hr_gt.a_letras as a_letras
from num2words import num2words
from datetime import date,datetime, timedelta
# import odoo.addons.hr_gt.a_letras

class ReportContrato(models.AbstractModel):
    _name = 'report.adcosine.contrato'

    def fecha_letras(self,fecha):
        # fecha = date.today()
        dia = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%d')
        mes = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%m')
        mes = a_letras.mes_a_letras(int(mes)-1)
        anio = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%Y')
        return {'dia_letras': a_letras.num_a_letras(int(dia),completo=False), 'dia': dia, 'mes_letras': mes, 'anio': anio,'anio_letras': a_letras.num_a_letras(int(anio),completo=False)}

    def sueldo_a_letras(self,sueldo):
        return a_letras.num_a_letras(sueldo,completo=False)

    def fecha_letras_hoy(self):
        fecha = date.today()
        dia = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%d')
        mes = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%m')
        mes = a_letras.mes_a_letras(int(mes)-1)
        anio = datetime.strptime(str(fecha), '%Y-%m-%d').strftime('%Y')
        return  str(a_letras.num_a_letras(int(dia),completo=False)) + ' de ' + str(mes) + ' del ' + str(a_letras.num_a_letras(int(anio),completo=False))

    def dpi_letras(self,dpi):
        numero_letras = ''
        if dpi:
            dpi_split = dpi.split()
            if len(dpi_split) > 1:
                numero_letras += a_letras.num_a_letras(dpi_split[0],completo=False)+' espacio ' + a_letras.num_a_letras(dpi_split[1],completo=False) +' espacio '
                if int(dpi_split[2][0]) == 0:
                    numero = dpi_split[2][1]+''+dpi_split[2][2]+''+dpi_split[2][3]
                    numero_letras += a_letras.num_a_letras(dpi_split[2][0],completo=False)+' '+a_letras.num_a_letras(int(numero),completo=False)
                else:
                    numero_letras +=  a_letras.num_a_letras(dpi_split[2],completo=False)
            else:
                dpi = str(dpi)
                contador = 0
                numero_letras = dpi[0]+dpi[1]+dpi[2]+dpi[3]+' '+dpi[4]+dpi[5]+dpi[6]+dpi[7]+dpi[8]
                numero_split = numero_letras.split()
                numero_letras = ''
                for numero in numero_split:
                    numero_letra = num2words(int(numero), to='currency', lang='es')
                    numero_letras += '' +  numero_letra[:len(numero_letra)-5]
                numero_letras +=  ' '+a_letras.num_a_letras(int(dpi[9]),completo=False) +' ' + a_letras.num_a_letras(int(dpi[10]),completo=False) + ' '+a_letras.num_a_letras(int(dpi[11]),completo=False) + ' '+a_letras.num_a_letras(int(dpi[12]),completo=False)
        return numero_letras

    def edad_letras(self,edad):
        unidad_letras = ''
        decena_letras = ''
        letras = ''
        edad_str = str(edad)
        if len(edad_str) == 2:
            unidad = int(edad_str[1])
            logging.warn(unidad)
            decena = int(edad_str[0])*10
            logging.warn(decena)
            decena_letras = a_letras.num_a_letras(decena,completo=False)
            unidad_letras = a_letras.num_a_letras(unidad,completo=False)
            letras = decena_letras
        return letras

    def estado_civil(self,estado):
        estado_civil = False
        if estado == 'single':
            estado_civil = 'SOLTERO (A)'
        elif estado == 'married':
            estado_civil = 'CASADO (A)'
        elif estado == 'divorced':
            estado_civil = 'DIVORCIADO (A)'
        elif estado == 'widower':
            estado_civil = 'VIUDO (A)'
        elif estado == 'separado':
            estado_civil = 'SEPARADO (A)'
        else:
            estado_civil = 'UNIDO (A)'
        return estado_civil

    def mes_letras(self,datos):
        nomina_id = self.env['hr.payslip.run'].search([('id','in',datos['nomina_ids'])])
        mes_nomina = int(datetime.datetime.strptime(str(nomina_id.date_start), '%Y-%m-%d').date().strftime('%m'))
        anio_nomina = int(datetime.datetime.strptime(str(nomina_id.date_start), '%Y-%m-%d').date().strftime('%Y'))
        anio_hoy =  int(datetime.datetime.strptime(str(date.today()), '%Y-%m-%d').date().strftime('%Y'))
        mes_hoy =  int(datetime.datetime.strptime(str(date.today()), '%Y-%m-%d').date().strftime('%m'))
        dia_hoy =  int(datetime.datetime.strptime(str(date.today()), '%Y-%m-%d').date().strftime('%d'))
        logging.warn(dia_hoy)
        mes =  ''
        if mes_nomina == 1:
            mes = 'ENERO'
        if mes_nomina == 2:
            mes = 'FEBRERO'
        if mes_nomina == 3:
            mes = 'MARZO'
        if mes_nomina == 4:
            mes = 'ABRIL'
        if mes_nomina == 5:
            mes = 'MAYO'
        if mes_nomina == 6:
            mes = 'JUNIO'
        if mes_nomina == 7:
            mes = 'JULIO'
        if mes_nomina == 8:
            mes = 'AGOSTO'
        if mes_nomina == 9:
            mes = 'SEPTIEMBRE'
        if mes_nomina == 10:
            mes = 'OCTUBRE'
        if mes_nomina == 11:
            mes = 'NOVIEMBRE'
        if mes_nomina == 12:
            mes = 'DICIEMBRE'
        return {'mes': mes, 'anio': anio_nomina, 'del':nomina_id.date_start ,'al':nomina_id.date_end,'anio_hoy': anio_hoy,'mes_hoy': mes,'dia_hoy': dia_hoy}

    def _get_recibos(self,datos):
        recibos_lista = []
        nomina_id = self.env['hr.payslip.run'].search([('id','in',datos['nomina_ids'])])
        recibo_pago_id = self.env['hr_gt.recibo_pago'].search([('id','=',datos['formato_recibo_pago_id'][0])])
        ordenado = []
        lista_ordenada = []
        if nomina_id.bono == False and nomina_id.aguinaldo == False:
            for planilla in nomina_id.slip_ids:
                dic = {
                    'empleado': planilla.employee_id,
                    'recibo_pago': recibo_pago_id,
                    'nomina': planilla,
                    'puesto': planilla.employee_id.job_id.name,
                    'sequence': planilla.employee_id.sequence,
                    'ingresos': {},
                    'deducciones': {},
                    'dias_trabajados': 0,
                    'total_ingresos': 0,
                    'total_deducciones': 0,
                    'liquido_recibir': 0
                }
                ordenado.append(planilla.employee_id.sequence)

                if planilla.line_ids:
                    for dias in planilla.worked_days_line_ids:
                        if dias.code == 'DIAS':
                            dic['dias_trabajados'] = dias.number_of_days


                if recibo_pago_id.ingreso_ids:
                    for ingreso in recibo_pago_id.ingreso_ids:
                        if ingreso.id not in dic['ingresos']:
                            dic['ingresos'][ingreso.id] = {'nombre': ingreso.nombre, 'total': 0}

                        if planilla.line_ids:
                            for linea in planilla.line_ids:
                                if linea.salary_rule_id.id in ingreso.regla_ids.ids:
                                    dic['ingresos'][ingreso.id]['total'] += linea.total
                                    dic['total_ingresos'] += linea.total
                                    dic['liquido_recibir'] += linea.total

                if recibo_pago_id.deduccion_ids:
                    for deduccion in recibo_pago_id.deduccion_ids:
                        if deduccion.id not in dic['deducciones']:
                            dic['deducciones'][deduccion.id] = {'nombre': deduccion.nombre, 'total': 0}

                        if planilla.line_ids:
                            for linea in planilla.line_ids:
                                if linea.salary_rule_id.id in deduccion.regla_ids.ids:
                                    if linea.total < 0:
                                        dic['deducciones'][deduccion.id]['total'] += (linea.total *-1)
                                        dic['total_deducciones'] += (linea.total*-1)
                                        dic['liquido_recibir'] -= (linea.total*-1)
                                    else:
                                        dic['deducciones'][deduccion.id]['total'] += (linea.total)
                                        dic['total_deducciones'] += (linea.total)
                                        dic['liquido_recibir'] -= (linea.total)

                recibos_lista.append(dic)

            # logging.warn(sorted(ordenado))
            # contador = 0
            # for s in sorted(ordenado):
            #     for r in recibos_lista:
            #         # logging.warn(r)
            #         if s == r['sequence']:
            #
            #             lista_ordenada.append(r)
            # #             contador+= 1
            #
            #
            # logging.warn('CONTADOR')
            # logging.warn(contador)
            # logging.warn(lista_ordenada)


            # logging.warn('LISTA ORDENADA')
            # recibos_lista = []
            # recibos_lista = lista_ordenada
            # logging.warn(lista_ordenada)
            # lista_sequencia = recibos_lista.sort(key=lambda item: item.get("sequence"))

            # f = itemgetter('sequence')
            # lis = recibos_lista.sort(key=f)
            # # csv_mapping_list = sorted(recibos_lista, key=lambda item: item("sequence"))
            # # recibos_lista = lista_sequencia
            # logging.warn('ESTA ES LA LISTA')
            # logging.warn(lis)


        if nomina_id.bono == True:
            for planilla in nomina_id.slip_ids:
                dic = {
                    'empleado': planilla.employee_id,
                    'recibo_pago': recibo_pago_id,
                    'nomina': planilla,
                    'puesto': planilla.employee_id.job_id.name,
                    'sequence': planilla.employee_id.sequence,
                    'ingresos': {},
                    'deducciones': {},
                    'dias_trabajados': 0,
                    'total_ingresos': 0,
                    'total_deducciones': 0,
                    'liquido_recibir': 0
                }

                if recibo_pago_id.ingreso_ids:
                    for ingreso in recibo_pago_id.ingreso_ids:
                        if ingreso.id not in dic['ingresos']:
                            dic['ingresos'][ingreso.id] = {'nombre': ingreso.nombre, 'total': 0}

                        if planilla.line_ids:
                            for linea in planilla.line_ids:
                                if linea.salary_rule_id.id in ingreso.regla_ids.ids:
                                    dic['ingresos'][ingreso.id]['total'] += linea.total
                                    dic['total_ingresos'] += linea.total
                                    dic['liquido_recibir'] += linea.total

                if recibo_pago_id.deduccion_ids:
                    for deduccion in recibo_pago_id.deduccion_ids:
                        if deduccion.id not in dic['deducciones']:
                            dic['deducciones'][deduccion.id] = {'nombre': deduccion.nombre, 'total': 0}

                        if planilla.line_ids:
                            for linea in planilla.line_ids:
                                if linea.salary_rule_id.id in deduccion.regla_ids.ids:
                                    if linea.total < 0:
                                        dic['deducciones'][deduccion.id]['total'] += (linea.total *-1)
                                        dic['total_deducciones'] += (linea.total*-1)
                                        dic['liquido_recibir'] -= (linea.total*-1)
                                    else:
                                        dic['deducciones'][deduccion.id]['total'] += (linea.total)
                                        dic['total_deducciones'] += (linea.total)
                                        dic['liquido_recibir'] -= (linea.total)
                recibos_lista.append(dic)
            # for s in sorted(ordenado):
            #     for r in recibos_lista:
            #         if s == r['sequence']:
            #             lista_ordenada.append(r)


        if nomina_id.aguinaldo == True:
            for planilla in nomina_id.slip_ids:
                dic = {
                    'empleado': planilla.employee_id,
                    'recibo_pago': recibo_pago_id,
                    'nomina': planilla,
                    'puesto': planilla.employee_id.job_id.name,
                    'sequence': planilla.employee_id.sequence,
                    'ingresos': {},
                    'deducciones': {},
                    'dias_trabajados': 0,
                    'total_ingresos': 0,
                    'total_deducciones': 0,
                    'liquido_recibir': 0
                }

                if recibo_pago_id.ingreso_ids:
                    for ingreso in recibo_pago_id.ingreso_ids:
                        if ingreso.id not in dic['ingresos']:
                            dic['ingresos'][ingreso.id] = {'nombre': ingreso.nombre, 'total': 0}

                        if planilla.line_ids:
                            for linea in planilla.line_ids:
                                if linea.salary_rule_id.id in ingreso.regla_ids.ids:
                                    dic['ingresos'][ingreso.id]['total'] += linea.total
                                    dic['total_ingresos'] += linea.total
                                    dic['liquido_recibir'] += linea.total

                if recibo_pago_id.deduccion_ids:
                    for deduccion in recibo_pago_id.deduccion_ids:
                        if deduccion.id not in dic['deducciones']:
                            dic['deducciones'][deduccion.id] = {'nombre': deduccion.nombre, 'total': 0}

                        if planilla.line_ids:
                            for linea in planilla.line_ids:
                                if linea.salary_rule_id.id in deduccion.regla_ids.ids:
                                    if linea.total < 0:
                                        dic['deducciones'][deduccion.id]['total'] += (linea.total *-1)
                                        dic['total_deducciones'] += (linea.total*-1)
                                        dic['liquido_recibir'] -= (linea.total*-1)
                                    else:
                                        dic['deducciones'][deduccion.id]['total'] += (linea.total)
                                        dic['total_deducciones'] += (linea.total)
                                        dic['liquido_recibir'] -= (linea.total)

                recibos_lista.append(dic)

            # for s in sorted(ordenado):
            #     for r in recibos_lista:
            #         if s == r['sequence']:
            #             lista_ordenada.append(r)

        # logging.warn(recibos_lista)
        return sorted(recibos_lista, key = lambda i: i['sequence'])


    def tipo_recibo(self,datos):
        tipo = {
            'recibo': False,
            'bono': False,
            'aguinaldo': False
        }
        nomina_id = self.env['hr.payslip.run'].search([('id','in',datos['nomina_ids'])])
        if nomina_id.bono:
            tipo['bono'] = True
        elif nomina_id['aguinaldo']:
            tipo['aguinaldo'] = True
        else:
            tipo['recibo'] = True

        return tipo




    def get_mes(self,mes_nomina):
        if mes_nomina == 1:
            mes = 'Enero'
        if mes_nomina == 2:
            mes = 'Febrero'
        if mes_nomina == 3:
            mes = 'Marzo'
        if mes_nomina == 4:
            mes = 'Abril'
        if mes_nomina == 5:
            mes = 'Mayo'
        if mes_nomina == 6:
            mes = 'Junio'
        if mes_nomina == 7:
            mes = 'Julio'
        if mes_nomina == 8:
            mes = 'Agosto'
        if mes_nomina == 9:
            mes = 'Septiembre'
        if mes_nomina == 10:
            mes = 'Octubre'
        if mes_nomina == 11:
            mes = 'Noviembre'
        if mes_nomina == 12:
            mes = 'Diciembre'


        return mes


    def _get_fecha_bono(self,nomina):

        dia = 0
        mes = 0
        anio = 0
        if nomina.employee_id.contract_id.date_start:
            fecha_final_comparacion = datetime.datetime.strptime(str(nomina.date_to), '%Y-%m-%d').date()
            fecha_inicio_comparacion = datetime.datetime.strptime(str(nomina.employee_id.contract_id.date_start), '%Y-%m-%d').date()
            diferencia_fecha = fecha_final_comparacion - fecha_inicio_comparacion


            dias_bonoc = diferencia_fecha.days + 1
            if dias_bonoc >= 365:
                dias_bonoc = 365
                dia = '01'
                mes = 'Julio'
                anio = int(datetime.datetime.strptime(str(nomina.date_to), '%Y-%m-%d').date().strftime('%Y'))

            else:
                dia = int(datetime.datetime.strptime(str(nomina.employee_id.contract_id.date_start), '%Y-%m-%d').date().strftime('%d'))
                mes_int = int(datetime.datetime.strptime(str(nomina.employee_id.contract_id.date_start), '%Y-%m-%d').date().strftime('%m'))
                mes = self.get_mes(mes_int)
                anio = int(datetime.datetime.strptime(str(nomina.employee_id.contract_id.date_start), '%Y-%m-%d').date().strftime('%Y'))
        return {'dia': dia, 'mes': mes,'anio':anio}


    def fecha_hoy(self):
        return date.today().strftime("%d/%m/%Y")
    # def pagos_deducciones(self,o):
    #     ingresos = 0
    #     descuentos = 0
    #     datos = {'ordinario': 0, 'extra_ordinario':0,'bonificacion':0}
    #     for linea in o.linea_ids:
    #         if linea.salary_rule_id.id in o.company_id.ordinario_ids.ids:
    #             datos['ordinario'] += linea.total
    #         elif linea.salary_rule_id.id in o.company_id.extra_ordinario_ids.ids:
    #             datos['extra_ordinario'] += linea.total
    #         elif linea.salary_rule_id.id in o.company_id.bonificacion_ids.ids:
    #             datos['bonificacion'] += linea.total
    #     return True

    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     return self.get_report_values(docids, data)


# {'context': {'tz': False, 'uid': 1, 'params':
# {'action': 473}, 'active_model': 'hr_gt.recibo_pago.wizard', 'active_id': 5, 'active_ids': [5], 'search_disable_custom_filters': True}, 'ids': [], 'model': 'hr_gt.recibo_pago.wizard', 'form': {'id': 5, 'nomina_ids': [17], 'formato_recibo_pago_id': [1, 'RECIBO DE PAGO PLANILLA'], 'fecha_inicio': False, 'fecha_fin': False, 'create_uid': [1, 'Administrator'], 'create_date': '2020-06-22 01:42:19', 'write_uid': [1, 'Administrator'], 'write_date': '2020-06-22 01:42:19', 'display_name': 'hr_gt.recibo_pago.wizard,5', '__last_update': '2020-06-22 01:42:19'}}

    @api.model
    def _get_report_values(self, docids, data=None):
        return self.get_report_values(docids, data)

    @api.model
    def get_report_values(self, docids, data=None):
        self.model = 'hr.contract'
        docs = self.env[self.model].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': self.model,
            'docs': docs,
            'edad_letras': self.edad_letras,
            'dpi_letras': self.dpi_letras,
            'estado_civil': self.estado_civil,
            'fecha_letras': self.fecha_letras,
            'sueldo_a_letras': self.sueldo_a_letras,
            'fecha_letras_hoy': self.fecha_letras_hoy,
            # '_get_recibos': self._get_recibos,
            # 'data': data['form'],
            # 'mes_letras': self.mes_letras,
            # 'tipo_recibo': self.tipo_recibo,
            # '_get_fecha_bono': self._get_fecha_bono,
            # 'mes_letras': self.mes_letras,
            # 'fecha_hoy': self.fecha_hoy,
            # 'a_letras': odoo.addons.hr_gt.a_letras,
            # 'datos_recibo': self.datos_recibo,
            # 'lineas': self.lineas,
            # 'horas_extras': self.horas_extras,
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
