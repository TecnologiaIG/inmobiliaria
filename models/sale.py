# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import uuid

from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    #lead_id = fields.Many2one('crm.lead','Oportunidad')
    banco_id = fields.Many2one('account.journal','Banco')
    fecha_inicio = fields.Date('Fecha de inicio')

    @api.onchange('opportunity_id')
    def check_change(self):
        if self.opportunity_id:
            lineas = []
            for oportunidad in self.opportunity_id:
                lineas.append((0,0,{'product_id': oportunidad.inmueble_id.id,'name': oportunidad.inmueble_id.name,'product_uom':oportunidad.inmueble_id.product_tmpl_id.uom_id ,'product_uom_qty': 1,'price_unit':  oportunidad.inmueble_id.list_price}))
                if oportunidad.parqueo_ids:
                    for parqueo in oportunidad.parqueo_ids:
                        lineas.append((0,0,{'product_id': parqueo.id ,'name': parqueo.name,'product_uom':parqueo.product_tmpl_id.uom_id,'product_uom_qty': 1,'price_unit': parqueo.list_price}))
            self.order_line = lineas
