# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    sale_id = fields.Many2one('sale.order', 'Venta')
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
            # Odoo 19: account.account ya no tiene company_id (ahora company_ids)
            # y ``code`` es company-dependent; with_company resuelve el código
            # sobre la compañía del pago.
            account = self.env['account.account'].with_company(
                payment.company_id
            ).search([
                ('code', '=', '2201.01.01'),
                ('company_ids', 'in', payment.company_id.id),
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
