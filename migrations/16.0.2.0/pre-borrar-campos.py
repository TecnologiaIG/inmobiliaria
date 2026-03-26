import logging
from odoo.upgrade import util

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    util.remove_field(cr, 'crm.lead', 'bodega_id')
    _logger.info("Campos borrados")
