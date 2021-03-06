.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================
Product Analytic
================

This module allows to define an analytic account at product or category level
for using it when creating invoices.

This module is an alternative to the official module
*account_analytic_default*. The advantages of this module are:

* it only depends on the *account* module, whereas the
  *account_analytic_default* module depends on *sale_stock* ;

* the analytic account is configured on the product form or the product
  category form, and not on a separate object.

Usage
=====

This module allows you to configure an **income analytic account** and an
**expense analytic account** on products and on product categories. When you
select the product in an invoice line, it will check if this product has an
income analytic account (for customer invoice/refunds) or an expense analytic
account (for supplier invoice/refunds) ; if it doesn't find any, it checks if
the category of the product has an income or expense analytic account ; if an
analytic account is found, it will be set by default on the invoice line.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/87/8.0


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/account-analytic/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed `feedback
<https://github.com/OCA/
account-analytic/issues/new?body=module:%20
product-analytic%0Aversion:%20
8.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Alexis de Lattre <alexis.delattre@akretion.com>
* Javier Iniesta <javieria@antiun.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
