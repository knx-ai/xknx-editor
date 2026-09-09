"""Pure rendering helpers for the Labels tool: field selection, CSV, and printable HTML sheets.

Kept free of imgui and of the project/service types so it is trivially unit-tested. The caller
(``tools.py``) resolves each device into a ``dict[field_id -> str]`` record and supplies the column
labels (for i18n); everything here operates on those records plus the selected field ids.

Printable output is HTML with a millimetre ``@page`` layout — the native app cannot print, so the
user opens the file in a browser and prints (or saves as PDF) from there. One geometry-verified Avery
preset (L7651) ships; a free ``LabelSheet`` lets the user enter any grid in millimetres.
"""

from __future__ import annotations

import csv
import html
import io
from dataclasses import dataclass

# Canonical field order. Selected fields are always emitted in this order, regardless of the order
# the user toggled them, so columns/label lines stay stable.
FIELD_IDS: tuple[str, ...] = (
    "ia",
    "name",
    "location",
    "description",
    "order",
    "manufacturer",
    "product",
    "hardware",
    "serial",
    "application",
    "gas",
)

# Sensible default selection = the columns the flat CSV always had.
DEFAULT_FIELDS: tuple[str, ...] = ("ia", "name", "order", "manufacturer", "description")


def order_fields(field_ids: set[str]) -> list[str]:
    """Return the selected field ids in canonical order (unknown ids dropped)."""
    return [f for f in FIELD_IDS if f in field_ids]


def build_table(
    records: list[dict[str, str]],
    field_ids: list[str],
    labels: dict[str, str],
) -> tuple[list[str], list[list[str]]]:
    """Build ``(header, rows)`` from per-device ``records`` and the ordered selected ``field_ids``.

    ``labels`` maps a field id to its (localised) column label. Missing values render as "".
    """
    header = [labels.get(f, f) for f in field_ids]
    rows = [[rec.get(f, "") for f in field_ids] for rec in records]
    return header, rows


def labels_csv(header: list[str], rows: list[list[str]]) -> str:
    """Render ``header`` + ``rows`` as CSV text (RFC-4180 quoting via :mod:`csv`)."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(header)
    writer.writerows(rows)
    return buf.getvalue()


@dataclass(frozen=True)
class LabelSheet:
    """Geometry of a printable label sheet, in millimetres (page is A4 by default)."""

    name: str
    cols: int
    rows: int
    label_w_mm: float
    label_h_mm: float
    margin_top_mm: float
    margin_left_mm: float
    gap_x_mm: float
    gap_y_mm: float
    corner_mm: float = 0.0
    page_w_mm: float = 210.0
    page_h_mm: float = 297.0

    @property
    def per_page(self) -> int:
        return self.cols * self.rows


# Geometry verified against Avery's own L7651 template (A4, 5x13 = 65 labels, 38.1x21.2 mm,
# top margin 10.7 mm, left margin 4.75 mm, 2.5 mm horizontal gap, 0 mm vertical gap, r=1.95 mm).
# Additional Avery codes are only added with source-verified geometry — never guessed dimensions.
SHEET_L7651 = LabelSheet(
    name="Avery L7651 (65 / A4)",
    cols=5,
    rows=13,
    label_w_mm=38.1,
    label_h_mm=21.2,
    margin_top_mm=10.7,
    margin_left_mm=4.75,
    gap_x_mm=2.5,
    gap_y_mm=0.0,
    corner_mm=1.95,
)

LABEL_SHEETS: tuple[LabelSheet, ...] = (SHEET_L7651,)


def _num(value: float) -> str:
    """Format a millimetre number compactly (drop trailing ``.0``)."""
    return f"{value:g}"


_HTML_HEAD = (
    "<!DOCTYPE html>\n<html><head><meta charset='utf-8'>\n"
    "<title>{title}</title>\n<style>\n{style}\n</style></head>\n<body>\n"
)
_HTML_TAIL = "</body></html>\n"


def render_labels_html(
    rows: list[list[str]], sheet: LabelSheet, *, title: str = "KNX labels"
) -> str:
    """Render device ``rows`` (each a list of field values) onto ``sheet`` as printable HTML.

    The first value of each row is shown bold (the individual address); remaining non-empty values
    follow as lines. Rows are paginated ``sheet.per_page`` at a time, one absolutely-positioned grid
    per A4 page.
    """
    style = (
        f"@page {{ size: {_num(sheet.page_w_mm)}mm {_num(sheet.page_h_mm)}mm; margin: 0; }}\n"
        "html, body { margin: 0; padding: 0; }\n"
        f".sheet {{ position: relative; width: {_num(sheet.page_w_mm)}mm; "
        f"height: {_num(sheet.page_h_mm)}mm; page-break-after: always; }}\n"
        ".label { position: absolute; overflow: hidden; box-sizing: border-box; "
        "padding: 1mm 1.5mm; font-family: 'DejaVu Sans', Arial, sans-serif; }\n"
        ".ia { font-weight: bold; font-size: 9pt; }\n"
        ".line { font-size: 7pt; line-height: 1.15; }\n"
    )
    out = [_HTML_HEAD.format(title=html.escape(title), style=style)]
    per_page = sheet.per_page or 1
    for start in range(0, len(rows), per_page):
        out.append("<div class='sheet'>\n")
        for i, row in enumerate(rows[start : start + per_page]):
            col = i % sheet.cols
            r = i // sheet.cols
            left = sheet.margin_left_mm + col * (sheet.label_w_mm + sheet.gap_x_mm)
            top = sheet.margin_top_mm + r * (sheet.label_h_mm + sheet.gap_y_mm)
            out.append(
                f"<div class='label' style='left:{_num(left)}mm;top:{_num(top)}mm;"
                f"width:{_num(sheet.label_w_mm)}mm;height:{_num(sheet.label_h_mm)}mm;"
                f"border-radius:{_num(sheet.corner_mm)}mm'>"
            )
            values = [v for v in row if v]
            if values:
                out.append(f"<div class='ia'>{html.escape(values[0])}</div>")
                for v in values[1:]:
                    out.append(f"<div class='line'>{html.escape(v)}</div>")
            out.append("</div>\n")
        out.append("</div>\n")
    out.append(_HTML_TAIL)
    return "".join(out)


def render_legend_html(
    header: list[str], rows: list[list[str]], *, title: str = "KNX legend"
) -> str:
    """Render a full-page A4 legend table (one row per device) for a distribution-board door."""
    style = (
        "@page { size: 210mm 297mm; margin: 12mm; }\n"
        "body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 9pt; }\n"
        "h1 { font-size: 13pt; }\n"
        "table { border-collapse: collapse; width: 100%; }\n"
        "th, td { border: 1px solid #999; padding: 2px 5px; text-align: left; }\n"
        "thead { display: table-header-group; }\n"
        "tr { page-break-inside: avoid; }\n"
    )
    out = [_HTML_HEAD.format(title=html.escape(title), style=style)]
    out.append(f"<h1>{html.escape(title)}</h1>\n<table><thead><tr>")
    out.extend(f"<th>{html.escape(h)}</th>" for h in header)
    out.append("</tr></thead><tbody>\n")
    for row in rows:
        out.append("<tr>")
        out.extend(f"<td>{html.escape(v)}</td>" for v in row)
        out.append("</tr>\n")
    out.append("</tbody></table>\n")
    out.append(_HTML_TAIL)
    return "".join(out)


@dataclass
class CustomGrid:
    """A user-entered free label grid (millimetres); converts to a :class:`LabelSheet`."""

    cols: int = 3
    rows: int = 8
    label_w_mm: float = 63.5
    label_h_mm: float = 33.9
    margin_top_mm: float = 12.9
    margin_left_mm: float = 7.2
    gap_x_mm: float = 2.5
    gap_y_mm: float = 0.0

    def to_sheet(self) -> LabelSheet:
        return LabelSheet(
            name="Custom",
            cols=max(1, self.cols),
            rows=max(1, self.rows),
            label_w_mm=self.label_w_mm,
            label_h_mm=self.label_h_mm,
            margin_top_mm=self.margin_top_mm,
            margin_left_mm=self.margin_left_mm,
            gap_x_mm=self.gap_x_mm,
            gap_y_mm=self.gap_y_mm,
        )
