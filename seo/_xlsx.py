# -*- coding: utf-8 -*-
"""Escriptor minim d'.xlsx sense dependencies (un xlsx es un ZIP d'XML).

L'entorn no te openpyxl ni acces a PyPI, aixi que generem el fitxer a ma.
Suporta: diversos fulls, capcalera fixada, autofiltre, amplada de columna,
ajust de text i uns quants estils. Prou per a fulls de treball.
"""
import zipfile
from xml.sax.saxutils import escape

# estils: 0 normal · 1 capcalera · 2 negreta · 3 ajust de text
#         4 alerta (vermell) · 5 titol gran · 6 ok (verd) · 7 gris petit
STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="8">
<font><sz val="11"/><name val="Calibri"/></font>
<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
<font><b/><sz val="11"/><name val="Calibri"/></font>
<font><sz val="11"/><name val="Calibri"/></font>
<font><b/><sz val="11"/><color rgb="FF9C0006"/><name val="Calibri"/></font>
<font><b/><sz val="16"/><color rgb="FFE20613"/><name val="Calibri"/></font>
<font><b/><sz val="11"/><color rgb="FF006100"/><name val="Calibri"/></font>
<font><sz val="9"/><color rgb="FF808080"/><name val="Calibri"/></font>
</fonts>
<fills count="5">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFE20613"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFFFC7CE"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFC6EFCE"/><bgColor indexed="64"/></patternFill></fill>
</fills>
<borders count="2">
<border><left/><right/><top/><bottom/><diagonal/></border>
<border><left/><right/><top/><bottom style="thin"><color rgb="FFD9D9D9"/></bottom><diagonal/></border>
</borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="8">
<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
<xf numFmtId="0" fontId="2" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="3" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="4" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="5" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment vertical="center"/></xf>
<xf numFmtId="0" fontId="6" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf numFmtId="0" fontId="7" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
</cellXfs>
</styleSheet>"""


def col_letter(n):
    s = ''
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


class Sheet(object):
    def __init__(self, name, widths=None, freeze=True, autofilter=True):
        self.name = name[:31]
        self.rows = []          # llista de llistes de (valor, estil)
        self.widths = widths or []
        self.freeze = freeze
        self.autofilter = autofilter

    def add(self, values, style=0):
        """values: llista de valors o de tuples (valor, estil)."""
        row = []
        for v in values:
            row.append(v if isinstance(v, tuple) else (v, style))
        self.rows.append(row)

    def xml(self):
        ncols_pre = max([len(r) for r in self.rows] or [1])
        dim = 'A1:%s%d' % (col_letter(ncols_pre), max(len(self.rows), 1))
        out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
               '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
               '<dimension ref="%s"/>' % dim]
        if self.freeze:
            out.append('<sheetViews><sheetView workbookViewId="0" showGridLines="0">'
                       '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
                       '</sheetView></sheetViews>')
        else:
            out.append('<sheetViews><sheetView workbookViewId="0" showGridLines="0"/></sheetViews>')
        out.append('<sheetFormatPr defaultRowHeight="15"/>')
        if self.widths:
            out.append('<cols>')
            for i, w in enumerate(self.widths, 1):
                out.append('<col min="%d" max="%d" width="%s" customWidth="1"/>' % (i, i, w))
            out.append('</cols>')
        out.append('<sheetData>')
        ncols = 0
        for r, row in enumerate(self.rows, 1):
            ncols = max(ncols, len(row))
            out.append('<row r="%d">' % r)
            for c, (val, st) in enumerate(row, 1):
                ref = '%s%d' % (col_letter(c), r)
                if val is None or val == '':
                    out.append('<c r="%s" s="%d"/>' % (ref, st))
                elif isinstance(val, (int, float)) and not isinstance(val, bool):
                    out.append('<c r="%s" s="%d"><v>%s</v></c>' % (ref, st, val))
                else:
                    out.append('<c r="%s" s="%d" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>'
                               % (ref, st, escape(str(val))))
            out.append('</row>')
        out.append('</sheetData>')
        if self.autofilter and len(self.rows) > 1 and ncols:
            out.append('<autoFilter ref="A1:%s%d"/>' % (col_letter(ncols), len(self.rows)))
        out.append('</worksheet>')
        return ''.join(out)


def write(path, sheets):
    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
          '<Default Extension="xml" ContentType="application/xml"/>',
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
          '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>']
    for i in range(1, len(sheets) + 1):
        ct.append('<Override PartName="/xl/worksheets/sheet%d.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' % i)
    ct.append('<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>')
    ct.append('<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>')
    ct.append('</Types>')

    wb = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>']
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    for i, sh in enumerate(sheets, 1):
        wb.append('<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (escape(sh.name), i, i))
        rels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet%d.xml"/>' % (i, i))
    wb.append('</sheets></workbook>')
    rels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' % (len(sheets) + 1))
    rels.append('</Relationships>')

    root = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>',
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>',
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>',
            '</Relationships>']

    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>SEO GEO CB Grup Barna</dc:title><dc:creator>CB Grup Barna</dc:creator>'
            '<cp:lastModifiedBy>CB Grup Barna</cp:lastModifiedBy></cp:coreProperties>')
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           '<Application>CB Grup Barna</Application></Properties>')

    z = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)
    z.writestr('[Content_Types].xml', ''.join(ct))
    z.writestr('_rels/.rels', ''.join(root))
    z.writestr('xl/workbook.xml', ''.join(wb))
    z.writestr('xl/_rels/workbook.xml.rels', ''.join(rels))
    z.writestr('xl/styles.xml', STYLES)
    z.writestr('docProps/core.xml', core)
    z.writestr('docProps/app.xml', app)
    for i, sh in enumerate(sheets, 1):
        z.writestr('xl/worksheets/sheet%d.xml' % i, sh.xml())
    z.close()
