"""Tests for the pure label-rendering helpers (fields, CSV, printable HTML sheets)."""

from __future__ import annotations

from editor_gui.plugins.project.ui import label_render as lr


def _records(n: int) -> list[dict[str, str]]:
    return [
        {"ia": f"1.1.{i}", "name": f"Dev {i}", "order": "ORD", "location": "B / F / R"}
        for i in range(1, n + 1)
    ]


def test_order_fields_canonical_regardless_of_input_order():
    ordered = lr.order_fields({"gas", "ia", "name"})
    assert ordered == ["ia", "name", "gas"]  # canonical FIELD_IDS order


def test_build_table_follows_selected_fields_and_labels():
    labels = {"ia": "Address", "name": "Name", "order": "Order"}
    header, rows = lr.build_table(
        [{"ia": "1.1.1", "name": "A", "order": "X"}], ["ia", "order"], labels
    )
    assert header == ["Address", "Order"]
    assert rows == [["1.1.1", "X"]]  # 'name' excluded, missing values would be ""


def test_build_table_missing_value_is_empty():
    header, rows = lr.build_table([{"ia": "1.1.1"}], ["ia", "name"], {})
    assert header == ["ia", "name"]  # falls back to the field id when no label
    assert rows == [["1.1.1", ""]]


def test_labels_csv_header_and_escaping():
    out = lr.labels_csv(
        ["Address", "Name"], [["1.1.1", "Name, with comma"]]
    ).splitlines()
    assert out[0] == "Address,Name"
    assert out[1] == '1.1.1,"Name, with comma"'


def test_l7651_geometry_is_verified_values():
    s = lr.SHEET_L7651
    assert (s.cols, s.rows, s.per_page) == (5, 13, 65)
    assert (s.label_w_mm, s.label_h_mm) == (38.1, 21.2)
    assert (s.margin_top_mm, s.margin_left_mm) == (10.7, 4.75)
    assert (s.gap_x_mm, s.gap_y_mm) == (2.5, 0.0)


def test_render_labels_html_page_size_and_count_and_position():
    rows = [[f"1.1.{i}", f"Dev {i}"] for i in range(1, 4)]
    html = lr.render_labels_html(rows, lr.SHEET_L7651)
    assert "size: 210mm 297mm" in html
    assert html.count("class='label'") == 3
    # First label sits at the sheet's top-left margin.
    assert "left:4.75mm;top:10.7mm" in html
    # Second label is one column over: 4.75 + (38.1 + 2.5) = 45.35mm.
    assert "left:45.35mm;top:10.7mm" in html


def test_render_labels_html_paginates_beyond_one_sheet():
    rows = [[f"1.1.{i}"] for i in range(lr.SHEET_L7651.per_page + 1)]
    html = lr.render_labels_html(rows, lr.SHEET_L7651)
    assert html.count("class='sheet'") == 2  # 66 labels -> 2 pages


def test_render_labels_html_escapes_and_bolds_first_value():
    html = lr.render_labels_html([["1.1.1", "A & B"]], lr.SHEET_L7651)
    assert "<div class='ia'>1.1.1</div>" in html
    assert "A &amp; B" in html  # HTML-escaped


def test_render_legend_html_one_row_per_device():
    header, rows = lr.build_table(_records(3), ["ia", "name"], {})
    html = lr.render_legend_html(header, rows)
    assert (
        html.count("</tr>\n") == 3
    )  # 3 data rows (the header row ends "</tr></thead>")
    assert "<th>ia</th>" in html
    assert "<td>1.1.2</td>" in html


def test_custom_grid_to_sheet():
    sheet = lr.CustomGrid(cols=2, rows=4, label_w_mm=70.0, label_h_mm=36.0).to_sheet()
    assert (sheet.cols, sheet.rows, sheet.per_page) == (2, 4, 8)
    assert sheet.label_w_mm == 70.0


def test_custom_grid_clamps_zero_dimensions():
    sheet = lr.CustomGrid(cols=0, rows=0).to_sheet()
    assert sheet.cols == 1 and sheet.rows == 1  # never divide-by-zero in pagination
