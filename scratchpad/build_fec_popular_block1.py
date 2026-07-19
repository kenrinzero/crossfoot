"""Builder for fec/2024-presidential-general-popular-block-1.cells.json.

Grid verified 2026-07-17 (Kimi): positioned pdfplumber extraction (x-band
column assignment) + per-candidate sums re-derived == printed Totals
(28,437 / 5,975 / 166,175 / 12,805 / 859, all exact) + visual render check
(scratchpad/fec-p2-render.png).
"""
import json
from pathlib import Path

CANDIDATES = ["AYYADURAI", "BOWMAN", "DE LA CRUZ", "DUNCAN", "EBKE"]
PCTS = ["0.02", "0.00", "0.11", "0.01", "0.00"]
TOTALS = ["28437", "5975", "166175", "12805", "859"]

# (code, [ayyadurai, bowman, de_la_cruz, duncan, ebke]) — None = blank (not zero)
GRID = [
    ("AL", [None]*5), ("AK", [None]*5), ("AZ", ["77", None, "689", None, None]),
    ("AR", [None]*5), ("CA", [None, None, "72539", None, None]),
    ("CO", ["15", None, "905", None, None]), ("CT", ["21", None, "264", None, None]),
    ("DE", ["4", None, "87", None, None]), ("DC", [None]*5),
    ("FL", ["199", None, "11969", None, None]), ("GA", ["37", "30", None, None, None]),
    ("HI", [None, None, "1940", None, None]), ("ID", ["514", None, "1230", None, None]),
    ("IL", ["42", None, "2877", None, None]), ("IN", [None, None, "832", None, None]),
    ("IA", ["424", None, "1427", None, None]), ("KS", [None]*5),
    ("KY", ["1015", "10", "391", None, None]), ("LA", [None, None, "1481", None, None]),
    ("ME", [None]*5), ("MD", ["31", None, "1136", None, None]),
    ("MA", ["18418", None, "12889", None, None]), ("MI", [None, "4", "458", None, None]),
    ("MN", ["2885", None, "2996", None, None]), ("MS", ["688", None, "1075", None, None]),
    ("MO", ["34", None, "618", None, None]), ("MT", ["21", None, None, None, None]),
    ("NE", [None]*5), ("NV", [None]*5), ("NH", [None]*5),
    ("NJ", [None, None, "5105", None, None]), ("NM", [None, None, "2442", None, "859"]),
    ("NY", ["134", None, "6327", None, None]), ("NC", ["30", None, "528", None, None]),
    ("ND", [None]*5), ("OH", ["74", "7", "1794", "12805", None]),
    ("OK", [None]*5), ("OR", [None]*5), ("PA", [None]*5),
    ("RI", [None, None, "1176", None, None]), ("SC", [None, None, "3059", None, None]),
    ("SD", [None]*5), ("TN", [None, "5865", "3457", None, None]),
    ("TX", ["433", None, "2374", None, None]), ("UT", [None, "59", "3189", None, None]),
    ("VT", ["8", None, "1710", None, None]), ("VA", [None, None, "8408", None, None]),
    ("WA", ["3323", None, "8695", None, None]), ("WV", ["10", None, "73", None, None]),
    ("WI", [None, None, "2035", None, None]), ("WY", [None]*5),
]

assert len(GRID) == 51
for ci, tot in enumerate(TOTALS):
    s = sum(int(g[1][ci]) for g in GRID if g[1][ci] is not None)
    assert s == int(tot), (CANDIDATES[ci], s, tot)

lines = []
add = lines.append
add("{")
add('  "table_id": "fec/2024-presidential-general-popular-block-1",')
add('  "source": {')
add('    "path": "sources/fec/2024presgeresults.pdf",')
add('    "table": "OFFICIAL 2024 PRESIDENTIAL GENERAL ELECTION RESULTS — page 2, popular vote block 1 (candidates AYYADURAI through EBKE)",')
add('    "title": "FEC official 2024 presidential general election results — popular vote, candidates AYYADURAI–EBKE",')
add('    "period": "General Election Date: 11/05/2024 (source: State Elections Offices)"')
add("  },")
add('  "unit_note": "Sparsely populated fringe-candidate block: most jurisdictions print no votes for most candidates — blank cells are not transcribed (blank is not zero). Candidate columns carry surnames only, as printed (DE LA CRUZ prints on two header lines). DUNCAN (OH only) and EBKE (NM only) are single-jurisdiction candidates whose printed state cell equals the printed national total; since the schema requires at least two relation sources, their cells are standalone with the equality stated in why. The Percentage row is each candidate\'s share of the national total popular vote; the denominator (national TOTAL VOTES) prints on the final block and is re-anchored by the planned cross-page capstone unit, so the percentage cells are standalone here. Column assignment verified from the positioned text layer plus the page-2 render.",')
add('  "columns": [')
for i, name in enumerate(CANDIDATES, 1):
    comma = "," if i < len(CANDIDATES) else ""
    add(f'    {{ "index": {i}, "label": "{name}" }}{comma}')
add("  ],")
add('  "rows": [')
for i, g in enumerate(GRID, 1):
    add(f'    {{ "index": {i}, "label": "{g[0]}" }},')
add('    { "index": 52, "label": "Total:" },')
add('    { "index": 53, "label": "Percentage: (share of national total popular vote)" }')
add("  ],")
add('  "cells": [')

cell_lines = []
for i, (code, vals) in enumerate(GRID, 1):
    for ci, v in enumerate(vals, 1):
        if v is None:
            continue
        if ci >= 4:
            cell_lines.append(f'    {{ "id": "r{i}c{ci}", "row": {i}, "col": {ci}, "value": "{v}", "role": "standalone", "why": "{CANDIDATES[ci-1]} appears on the ballot in this single jurisdiction only, so the printed state cell equals the printed national total; the frozen schema requires >=2 sources for a sum relation — no honest in-schema relation exists." }}')
        else:
            cell_lines.append(f'    {{ "id": "r{i}c{ci}", "row": {i}, "col": {ci}, "value": "{v}", "role": "leaf" }}')
for ci, tot in enumerate(TOTALS, 1):
    if ci >= 4:
        cell_lines.append(f'    {{ "id": "r52c{ci}", "row": 52, "col": {ci}, "value": "{tot}", "role": "standalone", "why": "{CANDIDATES[ci-1]} national total equals its single jurisdiction cell (single-source column); the frozen schema requires >=2 sources for a sum relation — no honest in-schema relation exists." }}')
    else:
        cell_lines.append(f'    {{ "id": "r52c{ci}", "row": 52, "col": {ci}, "value": "{tot}", "role": "total" }}')
for ci, pct in enumerate(PCTS, 1):
    cell_lines.append(f'    {{ "id": "r53c{ci}", "row": 53, "col": {ci}, "value": "{pct}", "role": "standalone", "unit": "%", "why": "Share of the national total popular vote; the denominator (national TOTAL VOTES) prints on the final popular-vote block and is re-anchored by the planned cross-page capstone unit — no honest relation exists within this block." }}')
add(",\n".join(cell_lines))
add("  ],")

rel_lines = []
for ci, name in enumerate(CANDIDATES[:3], 1):
    srcs = [f'"r{i}c{ci}"' for i, g in enumerate(GRID, 1) if g[1][ci-1] is not None]
    rel_lines.append(f'    {{ "type": "sum", "sources": [{", ".join(srcs)}], "target": "r52c{ci}", "note": "jurisdiction popular-vote cells for {name} sum to the printed national Total {TOTALS[ci-1]}" }}')
add('  "relations": [')
add(",\n".join(rel_lines))
add("  ]")
add("}")

out = Path("tables/fec/2024-presidential-general-popular-block-1.cells.json")
text = "\n".join(lines) + "\n"
out.write_text(text, encoding="utf-8", newline="\n")
json.loads(text)
print(f"wrote {out} — {len(cell_lines)} cells, {len(rel_lines)} relations")
