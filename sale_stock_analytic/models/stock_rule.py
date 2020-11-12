# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockRule(models.Model):

    _inherit = "stock.rule"

    def _get_stock_move_values(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        company_id,
        values,
    ):
        move_values = super(StockRule, self)._get_stock_move_values(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
        )
        sol_id = move_values.get("sale_line_id")
        if sol_id:
            sol_model = self.env["sale.order.line"]
            sol = sol_model.browse(sol_id)
            at = sol.analytic_tag_ids
            aa = sol.order_id.analytic_account_id
            if at:
                move_values.update({"analytic_tag_ids": [(6, 0, at.ids)]})
            if aa:
                move_values.update({"analytic_account_id": aa.id})
        return move_values
