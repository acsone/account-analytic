# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrderLine(models.Model):

    _inherit = "purchase.order.line"

    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        for line in self:
            aa = line.account_analytic_id
            at = line.analytic_tag_ids
            if aa:
                res[0].update({"analytic_account_id": aa.id})
            if at:
                res[0].update({"analytic_tag_ids": [(6, 0, at.ids)]})
        return res
