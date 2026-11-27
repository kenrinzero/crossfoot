"""Self-tests of tools/sourcecheck.py on small fixtures.

None of them needs a PDF library: the HTML fixture is read as it is, and the
PDF route is fed the character dictionaries pdfplumber would give, built here
for a small synthetic page. The checks over the real corpus are run by an
auditor (RUNBOOK-auditor.md), not by pytest."""

import copy
import json
from pathlib import Path

import pytest

import sourcecheck as sc

ROOT = Path(__file__).resolve().parent.parent
MINI = ROOT / "fixtures" / "sourcecheck" / "mini-statement.cells.json"
NO_EXCEPTIONS = {"printed_as": [], "combined_rows": []}


# ---- a synthetic page ------------------------------------------------------

COLUMNS = (300.0, 360.0, 420.0)  # right edges of three printed columns


def glyphs(text, right, top, size=7.0, width=4.0):
    """The characters of one token, right-aligned at x = right."""
    left = right - width * len(text)
    return [
        {"text": ch, "x0": left + i * width, "x1": left + (i + 1) * width, "top": top, "bottom": top + size,
         "size": size, "upright": True}
        for i, ch in enumerate(text)
        if ch != " "
    ]


def page(rows, columns=COLUMNS):
    """rows: (label, [entry per printed column, '' for empty paper])."""
    chars = []
    for n, (label, entries) in enumerate(rows):
        top = 100.0 + 10.0 * n
        chars += glyphs(label, 20.0 + 4.0 * len(label), top)
        for right, entry in zip(columns, entries):
            chars += glyphs(entry, right, top)
    return sc.page_lines(chars, 1, 612.0, 792.0)


def unit(rows, columns=3, name="synthetic/unit", family="synthetic"):
    """rows: {row: {col: value}}."""
    cells = {
        row: [{"id": f"r{row}c{col}", "row": row, "col": col, "value": value, "role": "leaf"}
              for col, value in sorted(values.items())]
        for row, values in rows.items()
    }
    return sc.Unit(Path("unit.cells.json"), name, family, Path("synthetic.pdf"), 1,
                   list(range(1, columns + 1)), {row: f"row {row}" for row in rows}, cells)


def check(u, lines, exceptions=None):
    sources = sc.Sources()
    sources._cache[(str(u.source), False)] = [lines]
    return sc.check_unit(u, sources, sc.Exceptions(exceptions or NO_EXCEPTIONS))


PRINTED = [
    ("Alpha", ["1,234", "......", "56"]),
    ("Beta", ["7", "(**)", "8"]),
    ("Gamma", ["-12", "30", "18"]),
    ("Total", ["1,229", "30", "82"]),
]
ROWS = {
    1: {1: "1234", 3: "56"},
    2: {1: "7", 3: "8"},
    3: {1: "-12", 2: "30", 3: "18"},
    4: {1: "1229", 2: "30", 3: "82"},
}


# ---- reading text ----------------------------------------------------------


def test_numbers_are_read_as_printed():
    assert sc.numbers_in("Net (1,234) and - 5 then 6,789.50 and 1,000-2,000") == [
        "-1234", "-5", "6789.50", "1000", "-2000"]
    assert sc.spellings("0.50") == ["0.50", "0.5", ".50"]
    assert sc.uncovered(["5", "5", "7"], sc.Counter(["5", "7"])) == ["5"]


def test_positioned_tokens_agree_with_the_plain_reading():
    for text in ("Cash 1,234 ...... (56) (**) - 7", "Table 6-D 12-34 2026, 5.0", "x(3)(4) 0.78* Z"):
        tokens = sc.tokens_of(text, lambda a, b, digits: (a, b))
        assert [t.text for t in tokens if t.kind == "num"] == sc.numbers_in(text)
    tokens = sc.tokens_of("Cash ...... (**) 9", lambda a, b, digits: (a, b))
    assert [t.text for t in tokens if t.kind == "blank"] == ["......", "(**)"]


def test_page_lines_drop_superscripts_and_decode_glyph_codes():
    chars = glyphs("Rate", 40.0, 100.0) + glyphs("56", 300.0, 100.0)
    chars += glyphs("2", 304.0, 98.0, size=4.0)  # a footnote marker after the number
    chars.append({"text": "(cid:20)", "x0": 350.0, "x1": 354.0, "top": 100.0, "bottom": 107.0, "size": 7.0,
                  "upright": True})  # glyph code 20 is the digit 1
    (line,) = sc.page_lines(chars, 1, 612.0, 792.0)
    assert line.values == sc.Counter(["56", "1"])


def test_rotated_page_is_read_in_its_own_direction():
    # text running up the page: the first character is the lowest
    chars = [
        {"text": ch, "x0": 200.0, "x1": 207.0, "top": 500.0 - 4.0 * i, "bottom": 504.0 - 4.0 * i, "size": 4.0,
         "upright": False, "matrix": (0, 7, -7, 0, 0, 0)}
        for i, ch in enumerate("123")
    ]
    (line,) = sc.page_lines(chars, 1, 612.0, 792.0)
    assert line.rotated and line.values == sc.Counter(["123"])


def test_two_text_columns_are_split_and_measured_from_their_own_margin():
    chars = glyphs("Left", 52.0, 100.0) + glyphs("5", 250.0, 100.0)
    chars += glyphs("Right", 356.0, 100.0) + glyphs("6", 550.0, 100.0)
    lines = sc.page_lines(chars, 1, 612.0, 792.0, two_columns=True)
    assert [(l.column, dict(l.values)) for l in lines] == [(0, {"5": 1}), (1, {"6": 1})]
    sc.align_text_columns([lines])
    five = next(t for t in lines[0].tokens if t.kind == "num")
    six = next(t for t in lines[1].tokens if t.kind == "num")
    assert (five.x1, six.x1) == (250.0, 250.0)  # both 214 points from their column's margin


def test_rows_are_kept_in_reading_order():
    at = lambda *tops: [(1, 0, float(t)) for t in tops]  # noqa: E731
    # the first row is printed twice; only its first printing can come before row two
    assert sc.in_reading_order([at(10, 50), at(20), at(30)]) == [at(10), at(20), at(30)]
    # a row out of order (a total taken from higher up the page) keeps all its positions
    assert sc.in_reading_order([at(10), at(20), at(5, 6), at(30), at(40)])[2] == at(5, 6)


# ---- row level -------------------------------------------------------------


def test_html_fixture_matches_at_both_levels():
    mismatches, tally = sc.check_unit(sc.Unit.load(MINI), sc.Sources(), sc.Exceptions(NO_EXCEPTIONS))
    assert mismatches == []
    assert tally["rows-on-one-line"] == 4
    assert tally["column-present"] == 11
    assert tally["column-missing-on-empty"] == 1


def test_wrong_value_fails_the_row_level(tmp_path, capsys):
    doc = json.loads(MINI.read_text(encoding="utf-8"))
    next(c for c in doc["cells"] if c["id"] == "r2c2")["value"] = "501"
    path = tmp_path / "typo.cells.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    assert sc.main([str(path)]) == 1
    out = capsys.readouterr().out
    assert "ROW" in out and "r2" in out and "501" in out
    assert sc.main([str(MINI), "--quiet"]) == 0


def test_cli_wants_units_or_all():
    with pytest.raises(SystemExit) as stop:
        sc.main(["--all", str(MINI)])
    assert stop.value.code == 2
    with pytest.raises(SystemExit):
        sc.main([])


# ---- column level ----------------------------------------------------------


def test_synthetic_page_matches_column_by_column():
    mismatches, tally = check(unit(ROWS), page(PRINTED))
    assert mismatches == []
    assert tally["column-rows-ok"] == 4
    assert tally["column-present"] == 10
    assert tally["column-missing-on-marker"] == 2


def test_value_in_the_wrong_column_is_reported():
    rows = copy.deepcopy(ROWS)
    rows[1] = {1: "1234", 2: "56"}  # 56 belongs in column 3; the row level cannot see this
    mismatches, tally = check(unit(rows), page(PRINTED))
    assert tally["rows-on-one-line"] == 4
    text = {m.cell: m.text for m in mismatches}
    assert set(text) == {"r1c2", "r1c3"}
    assert "prints dots" in text["r1c2"] and "printed in the column of c3" in text["r1c2"]
    assert "the unit has no cell, the page prints 56" in text["r1c3"]


def test_swapped_values_and_dropped_cell_are_reported():
    rows = copy.deepcopy(ROWS)
    rows[4] = {1: "82", 2: "30", 3: "1229"}
    mismatches, _ = check(unit(rows), page(PRINTED))
    assert {m.cell for m in mismatches} == {"r4c1", "r4c3"}
    rows = copy.deepcopy(ROWS)
    del rows[3][2]
    mismatches, _ = check(unit(rows), page(PRINTED))
    assert [(m.level, m.cell) for m in mismatches] == [("column", "r3c2")]
    assert "prints 30" in mismatches[0].text


def test_column_the_unit_never_fills_is_located_from_the_dots():
    printed = [("Alpha", ["5", "......", "9"]), ("Beta", ["6", "......", "11"]), ("Gamma", ["7", "(**)", "13"])]
    rows = {1: {1: "5", 3: "9"}, 2: {1: "6", 3: "11"}, 3: {1: "7", 3: "13"}}
    mismatches, tally = check(unit(rows), page(printed))
    assert mismatches == [] and tally["column-missing-on-marker"] == 3
    # same unit, but the page prints a number where the unit has no cell
    printed[1] = ("Beta", ["6", "44", "11"])
    mismatches, _ = check(unit(rows), page(printed))
    assert [(m.cell, "prints 44" in m.text) for m in mismatches] == [("r2c2", True)]


def test_row_printed_apart_from_the_grid_cannot_be_compared():
    printed = PRINTED + [("Needed to win = 270", ["", "", ""])]
    rows = copy.deepcopy(ROWS)
    rows[5] = {1: "270"}
    mismatches, _ = check(unit(rows), page(printed))
    assert [m.cell for m in mismatches] == ["r5c1"]
    assert "printed outside the unit's columns" in mismatches[0].text


# ---- known exceptions ------------------------------------------------------


def test_printed_as_exception_looks_for_the_marker():
    printed = PRINTED + [("Delta", ["Z", "0.78", "4"])]
    rows = copy.deepcopy(ROWS)
    rows[5] = {1: "0", 2: "0.78", 3: "4"}
    entry = {"unit": "synthetic/unit", "cell": "r5c1", "value": "0", "printed": "Z", "reason": "test"}
    known = {"printed_as": [entry], "combined_rows": []}
    assert [m.level for m in check(unit(rows), page(printed))[0]] == ["row"]
    mismatches, tally = check(unit(rows), page(printed), known)
    assert mismatches == [] and tally["known-printed-as"] == 1
    # the exception is a check, not a pass: another marker on the page fails it
    printed[-1] = ("Delta", ["X", "0.78", "4"])
    assert [m.level for m in check(unit(rows), page(printed), known)[0]] == ["row"]


def test_combined_rows_exception_still_wants_every_value_printed():
    rows = {1: {1: "1234", 2: "30", 3: "8"}}  # gathered from three printed lines
    entry = {"unit": "synthetic/unit", "rows": 1, "reason": "test"}
    known = {"printed_as": [], "combined_rows": [entry]}
    assert [m.level for m in check(unit(rows), page(PRINTED))[0]] == ["row"]
    mismatches, tally = check(unit(rows), page(PRINTED), known)
    assert mismatches == [] and tally["combined-rows-in-source"] == 1
    rows[1][3] = "999"
    (mismatch,) = check(unit(rows), page(PRINTED), known)[0]
    assert "999 is not printed anywhere" in mismatch.text


def test_stale_exceptions_are_reported():
    known = sc.Exceptions({
        "printed_as": [{"unit": "synthetic/unit", "cell": "r1c1", "value": "0", "printed": "Z", "reason": "test"}],
        "combined_rows": [{"unit": "synthetic/other", "rows": 3, "reason": "test"}],
    })
    u = unit(ROWS)
    sources = sc.Sources()
    sources._cache[(str(u.source), False)] = [page(PRINTED)]
    sc.check_unit(u, sources, known)
    assert len(known.stale({"synthetic/unit"})) == 1  # r1c1 holds 1234, not 0
    assert len(known.stale({"synthetic/unit", "synthetic/other"})) == 2
    assert known.stale(set()) == []


def test_shipped_exceptions_file_is_well_formed():
    doc = json.loads(sc.EXCEPTIONS_FILE.read_text(encoding="utf-8"))
    assert set(doc) == {"about", "printed_as", "combined_rows"}
    for entry in doc["printed_as"]:
        assert set(entry) == {"unit", "cell", "value", "printed", "reason"} and entry["reason"]
        assert (ROOT / "tables" / (entry["unit"] + ".cells.json")).is_file()
    for entry in doc["combined_rows"]:
        assert set(entry) == {"unit", "rows", "reason"} and entry["reason"]
        assert (ROOT / "tables" / (entry["unit"] + ".cells.json")).is_file()
