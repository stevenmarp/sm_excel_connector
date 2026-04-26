# -*- coding: utf-8 -*-

import html
from datetime import datetime
from odoo import http
from odoo.http import request, Response


class ExcelConnectorController(http.Controller):

    def _validate_token(self, template_id, token):
        """Validate the access token and return the template record or False."""
        if not token or not template_id:
            return False
        template = request.env['excel.template'].sudo().browse(int(template_id))
        if not template.exists() or template.state != 'published':
            return False
        if not template.access_token or template.access_token != token:
            return False
        return template

    def _log_access(self, template, ip_address, user_agent):
        """Record or update access history."""
        History = request.env['excel.access.history'].sudo()
        existing = History.search([
            ('template_id', '=', template.id),
            ('ip_address', '=', ip_address),
        ], limit=1)
        now = datetime.now()
        if existing:
            freq = 0
            if existing.last_used:
                diff = now - existing.last_used
                freq = int(diff.total_seconds())
            existing.write({
                'last_used': now,
                'frequency_sec': freq,
                'times_used': existing.times_used + 1,
                'user_agent': user_agent or existing.user_agent,
            })
        else:
            History.create({
                'template_id': template.id,
                'ip_address': ip_address,
                'user_agent': user_agent,
                'last_used': now,
                'times_used': 1,
            })

    @http.route('/excel/export/<int:template_id>', type='http', auth='public', csrf=False)
    def excel_export(self, template_id, token=None, **kwargs):
        """Serve export data as an HTML table that Excel/LibreOffice can parse."""
        template = self._validate_token(template_id, token)
        if not template:
            return Response('Unauthorized or template not found.', status=403)

        # Log access
        ip = request.httprequest.remote_addr or ''
        ua = request.httprequest.headers.get('User-Agent', '')[:200]
        self._log_access(template, ip, ua)

        # Generate HTML table
        headers, rows = template.get_export_data()

        parts = [
            '<!DOCTYPE html>',
            '<html><head><meta charset="utf-8">',
            f'<title>{html.escape(template.name)}</title>',
            '<style>table{border-collapse:collapse;font-family:Arial,sans-serif;font-size:12px}'
            'th,td{border:1px solid #ccc;padding:6px 10px;text-align:left}'
            'th{background:#4472C4;color:#fff;font-weight:bold}'
            'tr:nth-child(even){background:#f2f6fc}</style>',
            '</head><body>',
            '<table>',
            '<thead><tr>',
        ]
        for h in headers:
            parts.append(f'<th>{html.escape(str(h))}</th>')
        parts.append('</tr></thead><tbody>')

        for row in rows:
            parts.append('<tr>')
            for val in row:
                parts.append(f'<td>{html.escape(str(val))}</td>')
            parts.append('</tr>')

        parts.append('</tbody></table></body></html>')

        return Response(
            '\n'.join(parts),
            content_type='text/html; charset=utf-8',
            status=200,
        )

    @http.route('/excel/download_odc/<int:template_id>', type='http', auth='user', csrf=False)
    def download_odc(self, template_id, token=None, **kwargs):
        """Generate and serve an ODC file for MS Excel."""
        template = self._validate_token(template_id, token)
        if not template:
            return Response('Unauthorized or template not found.', status=403)

        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url', '')
        export_url = f'{base_url}/excel/export/{template.id}?token={template.access_token}'

        odc_content = f"""<html xmlns:o="urn:schemas-microsoft-com:office:office"
xmlns="http://www.w3.org/TR/REC-html40">
<head>
<meta http-equiv="Content-Type" content="text/x-ms-odc; charset=utf-8">
<meta name="ProgId" content="ODC.Table">
<meta name="SourceType" content="OLEDB">
<title>{html.escape(template.name)}</title>
<xml id="docprops"></xml>
<xml id="msodc">
 <odc:OfficeDataConnection
  xmlns:odc="urn:schemas-microsoft-com:office:odc"
  xmlns="http://www.w3.org/TR/REC-html40">
  <odc:Connection odc:Type="HTMLTABLE">
   <odc:Tables odc:Count="1">
    <odc:Table odc:Name="Table1" />
   </odc:Tables>
  </odc:Connection>
  <odc:CommandType>Table</odc:CommandType>
  <odc:CommandText>{html.escape(export_url)}</odc:CommandText>
 </odc:OfficeDataConnection>
</xml>
</head>
</html>"""

        headers = {
            'Content-Type': 'text/x-ms-odc; charset=utf-8',
            'Content-Disposition': f'attachment; filename="{template.name}.odc"',
        }
        return Response(odc_content, headers=headers, status=200)
