================================================================
Excel Connector — User Guide
================================================================

.. contents:: Table of Contents
   :depth: 2
   :local:

----

1. Overview
===========

The **Excel Connector** module lets you export data from any Odoo model
directly to **Microsoft Excel** or **LibreOffice Calc** — without any
API, middleware, or coding.

Create reusable export templates, pick the fields you need, apply
domain filters, and publish. Odoo generates a secure URL that
Excel or LibreOffice can fetch automatically at a set interval.

----

2. Installation
===============

1. Drop the ``sm_excel_connector`` folder in your Odoo ``addons`` path.
2. Restart Odoo and update the apps list.
3. Install **Excel Connector** from the Apps menu.
4. The admin user is automatically added to the
   *Excel Connector Manager* group.

----

3. Quick Start
==============

Step 1 — Create a Template
---------------------------

Go to **Excel Connector → Excel Templates** and click **New**.

- **Template Name** — give it a descriptive name
  (e.g. "Active Company Contacts").
- **Model** — pick any Odoo model (Contact, Invoice, Sales Order,
  Product, …).
- **Responsible** — defaults to current user.

Step 2 — Add Fields
--------------------

In the **Fields** tab, click *Add a line* and pick the fields you
want to export. Drag the handle (≡) to reorder. You can set a
**Custom Label** that overrides the default field name in the
exported table header.

Step 3 — Apply Filters (optional)
-----------------------------------

Switch to the **Domain Filter** tab. Use Odoo's domain builder to
filter which records to export. For example:

- ``Is Company = True`` — only companies
- ``State = Confirmed`` — only confirmed sales orders
- ``Create Date >= 2026-01-01`` — only recent records

Step 4 — Publish
-----------------

Click the **Publish** button in the header. This:

- Generates a unique **access token**
- Creates a **shareable URL**

The template moves to *Published* state. The URL is now live.

Step 5 — Connect from Excel / LibreOffice
-------------------------------------------

**LibreOffice Calc:**

1. Open LibreOffice Calc.
2. Go to **Sheet → Link to External Data**.
3. Paste the **Export URL** from the template.
4. Select the table that appears (e.g. *HTML_1*).
5. Check **Update every** and set the interval (e.g. 60 seconds).
6. Click **OK** — data fills in immediately.

**Microsoft Excel:**

1. In Odoo, click **Download ODC File** on the template.
2. Double-click the downloaded ``.odc`` file.
3. Excel opens and imports the data automatically.

----

4. Access & Security
=====================

Access Tokens
-------------

Each template gets a cryptographically random 32-byte token. Only
requests with the correct token can fetch data.

- Click **Generate New Token** to create a new token. This
  **immediately disconnects** all spreadsheets using the old token.

Access History
--------------

Every time a spreadsheet fetches data, the module logs:

- **IP Address** — of the requesting client
- **User Agent** — browser / application string
- **First Access** — when this IP first connected
- **Last Used** — most recent fetch
- **Frequency (sec)** — seconds between the last two fetches
- **Times Used** — total number of fetches

Click **Flush History** to delete all history records.

Wrong Token / Expired Template
------------------------------

- A request with a wrong or missing token returns **HTTP 403**.
- A request to an *Expired* template also returns **HTTP 403**.

----

5. Template Lifecycle
======================

Templates have three states:

- **Draft** — full editing, URL is not active.
- **Published** — URL is live, data can be fetched.
  Click *Expire* to deactivate.
- **Expired** — URL returns 403. Click *Reset to Draft* to
  re-enable editing.

----

6. Security Groups
===================

The module creates two groups:

- **Excel Connector User** — can create, edit and view own templates.
- **Excel Connector Manager** — can view, edit and delete all
  templates; full access to history records.

----

7. Multi-Company
=================

Each template has a **Company** field. In a multi-company environment,
users only see templates belonging to their current company (standard
Odoo record rules apply).

----

8. Compatibility
=================

- Tested on **Odoo 15.0 Community & Enterprise**.
- No external Python dependencies — uses only the standard library.
- Works with LibreOffice Calc and Microsoft Excel.
