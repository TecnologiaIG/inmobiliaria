# -*- encoding: utf-8 -*-

from odoo import api, models, fields
import numpy_financial
import logging

class ReporteFha(models.AbstractModel):
    _name = 'report.inmobiliaria.reporte_fha'

    def cuota_nivelada(self,data):
        cuotas = []
        iusi = 0
        saldo_capital = 0
        monto_financiar = data['precio_venta'] - data['enganche']
        monto_construccion = (data['precio_venta'] * 0.70)
        seguro_contra_incendio = ((monto_construccion * data['prima_contra_incendios']) / 12) /100
        if data['tipo_escrituracion'] == '70':
            iusi = ((((data['precio_venta'] * 0.7) / 1.12) * 0.009) / 12)
        else:
            iusi = ((data['precio_venta'] / 1.12) * 0.09) / 12
        saldo_capital_inicial = monto_financiar
        for i in range(1,data['cantidad_cuotas_enganche'] + 1):
            pago_capital = numpy_financial.ppmt((data['tasa_interes_conjunta']/100) / 12,i,data['cantidad_cuotas_enganche'],-monto_financiar)
            pago_interes = numpy_financial.ipmt((data['tasa_interes_conjunta']/100) / 12,i,data['cantidad_cuotas_enganche'],-monto_financiar)
            total_cuota_mensual = pago_capital + pago_interes + seguro_contra_incendio + iusi
            if i == 1:
                saldo_capital = saldo_capital_inicial - pago_capital
            if i >= 2:
                saldo_capital = saldo_capital - pago_capital

            cuota = {
                'mes': i,
                'pago_capital': pago_capital,
                'pago_interes': pago_interes,
                'seguro_contra_incendio': seguro_contra_incendio,
                'iusi': iusi,
                'total_cuota_mensual': total_cuota_mensual,
                'saldo_capital': saldo_capital,
            }
            cuotas.append(cuota)
        return cuotas


    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_ids', []))

        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
            'cuota_nivelada': self.cuota_nivelada,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:# -*- encoding: utf-8 -*-

from odoo import api, models, fields
import numpy_financial
import logging

class ReporteFha(models.AbstractModel):
    _name = 'report.inmobiliaria.reporte_fha'

    def cuota_nivelada(self,data):
        cuotas = []
        iusi = 0
        saldo_capital = 0
        monto_financiar = data['precio_venta'] - data['enganche']
        monto_construccion = (data['precio_venta'] * 0.70)
        seguro_contra_incendio = ((monto_construccion * data['prima_contra_incendios']) / 12) /100
        if data['tipo_escrituracion'] == '70':
            iusi = ((((data['precio_venta'] * 0.7) / 1.12) * 0.009) / 12)
        else:
            ((data['precio_venta'] / 1.12) * 0.09) / 12
        saldo_capital_inicial = monto_financiar
        for i in range(1,data['cantidad_cuotas_enganche'] + 1):
            pago_capital = numpy_financial.ppmt((data['tasa_interes_conjunta']/100) / 12,i,data['cantidad_cuotas_enganche'],-monto_financiar)
            pago_interes = numpy_financial.ipmt((data['tasa_interes_conjunta']/100) / 12,i,data['cantidad_cuotas_enganche'],-monto_financiar)
            total_cuota_mensual = pago_capital + pago_interes + seguro_contra_incendio + iusi
            if i == 1:
                saldo_capital = saldo_capital_inicial - pago_capital
            if i >= 2:
                saldo_capital = saldo_capital - pago_capital

            cuota = {
                'mes': i,
                'pago_capital': pago_capital,
                'pago_interes': pago_interes,
                'seguro_contra_incendio': seguro_contra_incendio,
                'iusi': iusi,
                'total_cuota_mensual': total_cuota_mensual,
                'saldo_capital': saldo_capital,
            }
            cuotas.append(cuota)
        return cuotas


    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_ids', []))

        return {
            'doc_ids': self.ids,
            'doc_model': model,
            'data': data['form'],
            'docs': docs,
            'cuota_nivelada': self.cuota_nivelada,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
