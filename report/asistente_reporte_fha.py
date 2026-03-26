# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

class AsistenteReporteFha(models.TransientModel):
    _name = 'inmobiliaria.asistente_reporte_fha'
    _description = "Asistente Reporte FHA"

    # lead_id = fields.Many2one("crm.lead","Oportunidad")
    precio_venta = fields.Float('Precio de venta')
    enganche = fields.Float('Enganche')
    cantidad_cuotas_enganche = fields.Integer('Plazo en meses pagar enganche')
    tasa_interes_conjunta = fields.Float('Tasa de Interes Conjunta')
    prima_contra_incendios = fields.Float('Prima del Seguro Contra Incendios')
    relacion_cuota_ingreso_maxima = fields.Float('Relación Cuota - Ingresos Máxima')
    tipo_escrituracion = fields.Selection([('70', '70-30'),('100', '100%')])
    gasto_escrituracion = fields.Float('Gastos de Escrituración')
    otros = fields.Float('Otros')

    def print_report(self):
        data = {
             'ids': [],
             'model': 'inmobiliaria.asistente_reporte_fha',
             'form': self.read()[0]
        }
        return self.env.ref('inmobiliaria.action_reporte_fha').report_action(self, data=data)
