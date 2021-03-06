# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class WooSaleOrderBindingExportListener(Component):
    _name = 'woo.sale.order.binding.export.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['woo.sale.order']

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_create(self, record, fields=None):
        record.with_delay().export_record()

    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        record.with_delay().export_record()

    def on_record_unlink(self, record):
        with record.backend_id.work_on(record._name) as work:
            external_id = work.component(usage='binder').to_external(record)
            if external_id:
                record.with_delay().export_delete_record(record.backend_id,
                                                         external_id)


class WooSaleOrderExportListener(Component):
    _name = 'woo.sale.order.export.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['woo.sale.order']

    # XXX must check record.env!!!
    @skip_if(lambda self, record, **kwargs: self.no_connector_export(record))
    def on_record_write(self, record, fields=None):
        for binding in record.woo_bind_ids:
            binding.with_delay().export_record()
