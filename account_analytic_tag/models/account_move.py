from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    # Transfer the tags to the analytical entries created when publishing the invoices.
    def action_post(self):
        res = super(AccountMove, self).action_post()
        if self.invoice_line_ids:
            for line in self.invoice_line_ids:
                line._transfer_tags()
        return res


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    analytic_tag_ids = fields.Many2many(
        comodel_name="account.analytic.tag",
        store=True,
        string="Analytic Tags",
        readonly=False,
    )

    def _transfer_tags(self):
        # analytic_line_ids  ('account.analytic.line')
        if self.analytic_tag_ids and self.analytic_line_ids:
            for item in self.analytic_line_ids:
                item.tag_ids = self.analytic_tag_ids

    def _prepare_analytic_lines(self):
        analytic_line_vals = super(AccountMoveLine, self)._prepare_analytic_lines()
        if not self.analytic_distribution and len(self.analytic_tag_ids) > 0:
            for tag_id in self.analytic_tag_ids:
                line_values = self._prepare_analytic_tag_line(
                    tag_id.account_analytic_id
                )
                if not self.currency_id.is_zero(line_values.get("amount")):
                    analytic_line_vals.append(line_values)
        return analytic_line_vals

    def _prepare_analytic_tag_line(self, account_id):
        self.ensure_one()
        default_name = self.name or (
            self.ref or "/" + " -- " + (self.partner_id and self.partner_id.name or "/")
        )
        return {
            "name": default_name,
            "date": self.date,
            "partner_id": self.partner_id.id,
            "account_id": account_id.id,
            "unit_amount": self.quantity,
            "product_id": self.product_id and self.product_id.id or False,
            "product_uom_id": self.product_uom_id and self.product_uom_id.id or False,
            "amount": -self.balance,
            "general_account_id": self.account_id.id,
            "ref": self.ref,
            "move_line_id": self.id,
            "user_id": self.move_id.invoice_user_id.id or self._uid,
            "company_id": self.company_id.id or self.env.company.id,
            "category": "invoice"
            if self.move_id.is_sale_document()
            else "vendor_bill"
            if self.move_id.is_purchase_document()
            else "other",
        }
