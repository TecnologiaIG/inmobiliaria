# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    sale_id = fields.Many2one(
        'sale.order',
        'Venta',
        # FIX ticket #3940 (Karen O. 2026-06-23): al seleccionar cliente e intentar
        # "jalar la oportunidad" en el pago, el dropdown mostraba TODAS las
        # ventas de TODOS los clientes — p.ej. para Moisés Simón (cliente de
        # VV-1701/1601/1604) aparecían también VV-1707 de su esposa Mónica.
        # Causa raíz: este override redeclara `sale_id` SIN domain, reemplazando
        # el dominio nativo de Odoo (que filtraba por `commercial_partner_id`).
        # Restauramos un domain equivalente al `_onchange_partner_id_autofill_…
        # sale_order` de `account_payment_receipt`: filtra por comercial partner
        # + child_ids, estados 'sale' o 'draft' (enganche), y multi-company.
        domain=(
            "[('partner_id', 'child_of', commercial_partner_id),"
            " ('state', 'in', ['sale', 'draft']),"
            " ('company_id', 'in', [False, company_id])]"
        ),
        help='Venta (sale.order) asociada a este pago. '
             'Filtrada por el cliente seleccionado y la compañía activa.',
    )
    descripcion = fields.Char('Descripcion')
    fecha_boleta = fields.Date('Fecha boleta')
    cheque = fields.Char('Cheque')
    boleta = fields.Char('Boleta')

    es_anticipo = fields.Boolean(
        string='Es Anticipo',
        default=False,
        help='Marcar si este pago es un anticipo de cliente. '
             'El asiento contable usara la cuenta de Anticipos de Clientes '
             'en lugar de Cuentas por Cobrar.',
    )

    @api.depends('es_anticipo')
    def _compute_destination_account_id(self):
        """Override: usa cuenta de anticipos cuando es_anticipo=True.

        Para pagos marcados como anticipo (inbound/customer), sustituye
        la cuenta por cobrar del partner por la cuenta 2201.01.01
        ANTICIPOS DE CLIENTES.
        """
        anticipos = self.filtered(
            lambda p: p.es_anticipo
            and p.payment_type == 'inbound'
            and p.partner_type == 'customer'
        )
        regular = self - anticipos

        if regular:
            super(AccountPayment, regular)._compute_destination_account_id()

        for payment in anticipos:
            account = self.env['account.account'].search([
                ('code', '=', '2201.01.01'),
                ('company_id', '=', payment.company_id.id),
            ], limit=1)
            if account:
                payment.destination_account_id = account
            else:
                super(AccountPayment, payment)._compute_destination_account_id()

    @api.onchange('es_anticipo')
    def _onchange_es_anticipo(self):
        """Validacion al cambiar el checkbox de anticipo."""
        if self.es_anticipo and self.payment_type != 'inbound':
            raise UserError(_(
                'Los anticipos solo aplican para pagos de clientes (Recibir dinero).'
            ))
