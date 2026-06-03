import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    cr.execute("""
        DO $$
        BEGIN
            BEGIN
                ALTER TABLE crm_lead DROP COLUMN IF EXISTS bodega_id;
            EXCEPTION WHEN OTHERS THEN
                RAISE NOTICE 'Error dropping bodega_id: %', SQLERRM;
            END;
        END $$;
    """)
    _logger.info("Campos borrados")
