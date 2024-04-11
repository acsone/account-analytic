# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrExpense(models.Model):

    _inherit = "hr.expense"

    @api.depends("sheet_id.department_id")
    def _compute_analytic_distribution(self):
        """
        modifying analytic account on department shouldn't
        modify every analytic distribution already created
        """
        ret = super()._compute_analytic_distribution()

        for rec in self:
            # add analytic account of department in distribution
            analytic_acc = rec.sheet_id.department_id.account_analytic_id
            if analytic_acc:
                distribution = rec.analytic_distribution or {}
                distribution[str(analytic_acc.id)] = 100.0
                rec.analytic_distribution = distribution

        return ret
