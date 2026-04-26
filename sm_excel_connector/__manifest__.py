# -*- coding: utf-8 -*-
{
    'name': 'Excel Connector — Export Odoo Data to Excel & LibreOffice',
    'version': '19.0.1.0.0',
    'summary': 'Sync Odoo data to Microsoft Excel & LibreOffice Calc via secure URL or ODC file. Create export templates, filter data, track access history.',
    'description': """
Excel Connector for Odoo 19
============================

Effortlessly sync Odoo data with Microsoft Excel & LibreOffice Calc!

**Key Features:**
- Create reusable export templates for any Odoo model
- Select specific fields to export
- Apply domain filters to export only the data you need
- Secure access with auto-generated tokens
- Generate shareable URLs for Excel / LibreOffice Calc
- Download ODC (Office Data Connection) files for MS Excel
- Track access history: IP addresses, frequency, usage count
- Template states: Draft → Published → Expired
- Auto-refresh support in Excel & LibreOffice

**How It Works:**
1. Create an Excel Template in Odoo (pick a model, select fields, add filters)
2. Publish the template to generate a secure URL + access token
3. Use the URL in LibreOffice Calc (Sheet → Link to External Data) or download
   the ODC file for MS Excel
4. Data auto-refreshes at the interval you set

**Security:**
- Each template gets a unique access token
- Refresh the token at any time to disconnect all spreadsheets
- Full access history with IP tracking
""",
    'category': 'Extra Tools',
    'author': 'Steven Marp',
    'website': 'https://github.com/stevenmarp',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/excel_connector_security.xml',
        'security/ir.model.access.csv',
        'views/excel_template_views.xml',
        'views/excel_connector_menus.xml',
    ],
    'assets': {},
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 49.00,
    'currency': 'USD',
}
