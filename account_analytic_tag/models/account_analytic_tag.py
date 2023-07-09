from odoo import fields, models


class AccountAnalyticTag(models.Model):
    _name = "account.analytic.tag"
    _description = "Analytic Tags"

    name = fields.Char(string="Analytic Tag", index=True, required=True)
    color = fields.Integer("Color Index")
    active = fields.Boolean(
        default=True,
        help="Set active to false to hide the Analytic Tag without removing it.",
    )
    company_id = fields.Many2one("res.company", string="Company")
    account_analytic_id = fields.Many2one(
        "account.analytic.account", string="Analytic Account"
    )
