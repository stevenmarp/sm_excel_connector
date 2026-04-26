# -*- coding: utf-8 -*-
{
    'name': 'Excel Connector — Export Odoo Data to Excel & LibreOffice',
    'version': '17.0.1.0.0',
    'summary': 'Sync Odoo data to Microsoft Excel & LibreOffice Calc via secure URL '
               'or ODC file. Create export templates, filter data, track access history.',
    'description': """
Excel Connector for Odoo 17
============================

Effortlessly sync Odoo data with Microsoft Excel & LibreOffice Calc!

**Export Templates for Any Model**

Create reusable export templates for any Odoo model — contacts, invoices,
sales orders, products, or anything else. Pick the fields you need, arrange
them in order, and save. No coding, no API setup, no external tools.

**Smart Domain Filters**

Apply domain filters to export exactly the data you need. Only confirmed
sales? Only invoices from this month? Only active customers? Use Odoo's
built-in domain builder — no coding required.

**Secure Access Tokens**

Each template gets a unique access token. Only users with the token can
fetch data. Regenerate the token at any time to instantly disconnect all
connected spreadsheets. Your Odoo data stays safe.

**URL & ODC File Export**

- Copy the shareable URL into LibreOffice Calc (Sheet → Link to External
  Data) for auto-refresh.
- Or download an ODC (Office Data Connection) file to connect directly
  from Microsoft Excel.
- Both methods work without any API setup.

**Access History & IP Tracking**

Monitor who is fetching your data. See IP addresses, first access, last
used, frequency and times used. Flush history or regenerate the token if
you spot unauthorized access.

**Template Lifecycle**

Templates follow a clear lifecycle:
- **Draft** — configure freely
- **Published** — URL is active, data can be fetched
- **Expired** — access blocked

Manage the state with one click from the form view header.

**How It Works**

1. Create an Excel Template in Odoo (pick a model, select fields, add filters)
2. Publish the template to generate a secure URL + access token
3. Use the URL in LibreOffice Calc or download the ODC file for MS Excel
4. Data auto-refreshes at the interval you set

**Security**

- Each template gets a unique access token
- Refresh the token at any time to disconnect all spreadsheets
- Full access history with IP tracking
- User & Manager roles with record rules
    """,
    'author': 'Steven Marp',
    'website': 'https://apps.odoo.com/apps/browse?repo_maintainer_id=512936',
    'category': 'Extra Tools',
    'license': 'OPL-1',

    'depends': ['base'],

    'data': [
        # Security
        'security/excel_connector_security.xml',
        'security/ir.model.access.csv',

        # Views
        'views/excel_template_views.xml',
        'views/excel_connector_menus.xml',
    ],

    'images': ['static/description/banner.gif'],
    'price': 39.00,
    'currency': 'USD',
    'installable': True,
    'application': True,
    'auto_install': False,
}
