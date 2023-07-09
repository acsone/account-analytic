# Copyright 2023 Tecnativa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAccountAnalyticTag(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestAccountAnalyticTag, cls).setUpClass()

        cls.env.user.write(
            {
                "groups_id": [
                    (4, cls.env.ref("analytic.group_analytic_accounting").id),
                    (4, cls.env.ref("account_analytic_tag.group_analytic_tags").id),
                ],
            }
        )
        # ==== For Accounting ====
        cls.default_plan = cls.env["account.analytic.plan"].create(
            {"name": "Default", "company_id": False}
        )
        cls.analytic_account_a = cls.env["account.analytic.account"].create(
            {
                "name": "analytic_account_a",
                "plan_id": cls.default_plan.id,
                "company_id": False,
            }
        )
        # ==== Tags ====
        cls.account_analytic_tag_a = cls.env["account.analytic.tag"].create(
            {
                "name": "Tag Info A",
                "account_analytic_id": cls.analytic_account_a.id,
            }
        )
        cls.account_analytic_tag_b = cls.env["account.analytic.tag"].create(
            {
                "name": "Tag Info B",
                "account_analytic_id": cls.analytic_account_a.id,
            }
        )
        # ==== For Invoices ====
        cls.product_a = cls.env["product.product"].create(
            {
                "name": "product_a",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "lst_price": 100.0,
                "standard_price": 80.0,
                "taxes_id": False,
            }
        )
        cls.product_b = cls.env["product.product"].create(
            {
                "name": "product_a",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "lst_price": 200.0,
                "standard_price": 100.0,
                "taxes_id": False,
            }
        )

        cls.partner_a = cls.env["res.partner"].create(
            {
                "name": "partner_a",
                "company_id": False,
            }
        )

    def test_action_post_analytic_lines(self):
        def get_analytic_lines():
            return (
                self.env["account.analytic.line"]
                .search([("move_line_id", "in", out_invoice.line_ids.ids)])
                .sorted("amount")
            )

        out_invoice = self.env["account.move"].create(
            [
                {
                    "move_type": "out_invoice",
                    "partner_id": self.partner_a.id,
                    "date": "2023-01-01",
                    "invoice_date": "2023-01-01",
                }
            ]
        )
        line_1 = self.env["account.move.line"].create(
            {
                "product_id": self.product_a.id,
                "move_id": out_invoice.id,
                "price_unit": 200.0,
                "analytic_tag_ids": [(4, self.account_analytic_tag_a.id)],
                "analytic_distribution": {
                    self.analytic_account_a.id: 100,
                },
            }
        )
        line_2 = self.env["account.move.line"].create(
            {
                "product_id": self.product_b.id,
                "move_id": out_invoice.id,
                "price_unit": 100.0,
                "analytic_tag_ids": [
                    (
                        6,
                        0,
                        [
                            self.account_analytic_tag_a.id,
                            self.account_analytic_tag_b.id,
                        ],
                    )
                ],
            }
        )
        out_invoice.write({"invoice_line_ids": [(6, 0, [line_1.id, line_2.id])]})
        out_invoice.action_post()
        # Analytic lines are created when posting the invoice
        for analytic_line in get_analytic_lines():
            if analytic_line.move_line_id.id == line_1.id:
                # check one tag
                if analytic_line.tag_ids:
                    self.assertEqual(analytic_line.tag_ids, line_1.analytic_tag_ids)
            if analytic_line.move_line_id.id == line_2.id:
                # check list of tags
                self.assertEqual(analytic_line.tag_ids, line_2.analytic_tag_ids)
