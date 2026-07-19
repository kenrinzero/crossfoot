"""Builder for fec/2024-presidential-general-electoral.cells.json.

Grid verified 2026-07-17 (Kimi): positioned pdfplumber extraction (x-band
column assignment) + column sums re-derived == printed Total (538/312/226)
+ visual render check (scratchpad/fec-p1-render.png).
"""
import json
from pathlib import Path

# (code, ev, trump, harris) — exactly as printed; None = blank (not zero)
GRID = [
    ("AL", 9, 9, None), ("AK", 3, 3, None), ("AZ", 11, 11, None),
    ("AR", 6, 6, None), ("CA", 54, None, 54), ("CO", 10, None, 10),
    ("CT", 7, None, 7), ("DE", 3, None, 3), ("DC", 3, None, 3),
    ("FL", 30, 30, None), ("GA", 16, 16, None), ("HI", 4, None, 4),
    ("ID", 4, 4, None), ("IL", 19, None, 19), ("IN", 11, 11, None),
    ("IA", 6, 6, None), ("KS", 6, 6, None), ("KY", 8, 8, None),
    ("LA", 8, 8, None), ("ME", 4, 1, 3), ("MD", 10, None, 10),
    ("MA", 11, None, 11), ("MI", 15, 15, None), ("MN", 10, None, 10),
    ("MS", 6, 6, None), ("MO", 10, 10, None), ("MT", 4, 4, None),
    ("NE", 5, 4, 1), ("NV", 6, 6, None), ("NH", 4, None, 4),
    ("NJ", 14, None, 14), ("NM", 5, None, 5), ("NY", 28, None, 28),
    ("NC", 16, 16, None), ("ND", 3, 3, None), ("OH", 17, 17, None),
    ("OK", 7, 7, None), ("OR", 8, None, 8), ("PA", 19, 19, None),
    ("RI", 4, None, 4), ("SC", 9, 9, None), ("SD", 3, 3, None),
    ("TN", 11, 11, None), ("TX", 40, 40, None), ("UT", 6, 6, None),
    ("VT", 3, None, 3), ("VA", 13, None, 13), ("WA", 12, None, 12),
    ("WV", 4, 4, None), ("WI", 10, 10, None), ("WY", 3, 3, None),
]
TOTAL = (538, 312, 226)

assert len(GRID) == 51
assert sum(g[1] for g in GRID) == TOTAL[0]
assert sum(g[2] for g in GRID if g[2] is not None) == TOTAL[1]
assert sum(g[3] for g in GRID if g[3] is not None) == TOTAL[2]
for code, ev, t, h in GRID:
    assert ev == (t or 0) + (h or 0), code  # per-row identity incl. ME/NE

lines = []
add = lines.append
add("{")
add('  "table_id": "fec/2024-presidential-general-electoral",')
add('  "source": {')
add('    "path": "sources/fec/2024presgeresults.pdf",')
add('    "table": "OFFICIAL 2024 PRESIDENTIAL GENERAL ELECTION RESULTS — page 1, electoral votes by state",')
add('    "title": "FEC official 2024 presidential general election results — electoral votes cast",')
add('    "period": "General Election Date: 11/05/2024 (source: State Elections Offices)"')
add("  },")
add('  "unit_note": "Winner-take-all: for 49 jurisdictions only the winning candidate\'s electoral-vote cell is printed — blank loser cells are not transcribed (blank is not zero). Maine (ME 1 Trump / 3 Harris) and Nebraska (NE 4 Trump / 1 Harris) split their votes and print both cells. Column assignment verified from the positioned text layer plus the page-1 render.",')
add('  "columns": [')
add('    { "index": 1, "label": "ELECTORAL VOTES" },')
add('    { "index": 2, "label": "ELECTORAL VOTES CAST FOR DONALD J. TRUMP (R)" },')
add('    { "index": 3, "label": "ELECTORAL VOTES CAST FOR KAMALA D. HARRIS (D)" }')
add("  ],")
add('  "rows": [')
for i, g in enumerate(GRID, 1):
    comma = "," if True else ""
    add(f'    {{ "index": {i}, "label": "{g[0]}" }},')
add('    { "index": 52, "label": "Total:" },')
add('    { "index": 53, "label": "Total Electoral Votes Needed to Win (italic reference line below the table)" }')
add("  ],")
add('  "cells": [')

cell_lines = []
for i, (code, ev, t, h) in enumerate(GRID, 1):
    cell_lines.append(f'    {{ "id": "r{i}c1", "row": {i}, "col": 1, "value": "{ev}", "role": "leaf" }}')
    if t is not None:
        cell_lines.append(f'    {{ "id": "r{i}c2", "row": {i}, "col": 2, "value": "{t}", "role": "leaf" }}')
    if h is not None:
        cell_lines.append(f'    {{ "id": "r{i}c3", "row": {i}, "col": 3, "value": "{h}", "role": "leaf" }}')
cell_lines.append(f'    {{ "id": "r52c1", "row": 52, "col": 1, "value": "{TOTAL[0]}", "role": "total" }}')
cell_lines.append(f'    {{ "id": "r52c2", "row": 52, "col": 2, "value": "{TOTAL[1]}", "role": "total" }}')
cell_lines.append(f'    {{ "id": "r52c3", "row": 52, "col": 3, "value": "{TOTAL[2]}", "role": "total" }}')
cell_lines.append('    { "id": "r53c1", "row": 53, "col": 1, "value": "270", "role": "standalone", "why": "Reference constant printed below the Total row (\'Total Electoral Votes Needed to Win = 270\'); participates in no table relation — transcribed as printed." }')
add(",\n".join(cell_lines))
add("  ],")

c1_ids = [f'"r{i}c1"' for i in range(1, 52)]
c2_ids = [f'"r{i}c2"' for i, g in enumerate(GRID, 1) if g[2] is not None]
c3_ids = [f'"r{i}c3"' for i, g in enumerate(GRID, 1) if g[3] is not None]
me = next(i for i, g in enumerate(GRID, 1) if g[0] == "ME")
ne = next(i for i, g in enumerate(GRID, 1) if g[0] == "NE")

rels = [
    ("sum", c1_ids, "r52c1", "state electoral-vote allocations sum to the printed Total 538"),
    ("sum", c2_ids, "r52c2", "electoral votes cast for Donald J. Trump (R) sum to the printed Total 312"),
    ("sum", c3_ids, "r52c3", "electoral votes cast for Kamala D. Harris (D) sum to the printed Total 226"),
    ("sum", ['"r52c2"', '"r52c3"'], "r52c1", "capstone identity: 312 + 226 = 538 total electoral votes"),
    ("sum", [f'"r{me}c2"', f'"r{me}c3"'], f'r{me}c1', "Maine split: 1 (Trump) + 3 (Harris) = 4 electoral votes"),
    ("sum", [f'"r{ne}c2"', f'"r{ne}c3"'], f'r{ne}c1', "Nebraska split: 4 (Trump) + 1 (Harris) = 5 electoral votes"),
]
add('  "relations": [')
rel_lines = []
for typ, srcs, tgt, note in rels:
    rel_lines.append(f'    {{ "type": "{typ}", "sources": [{", ".join(srcs)}], "target": "{tgt}", "note": "{note}" }}')
add(",\n".join(rel_lines))
add("  ]")
add("}")

out = Path("tables/fec/2024-presidential-general-electoral.cells.json")
out.parent.mkdir(parents=True, exist_ok=True)
text = "\n".join(lines) + "\n"
out.write_text(text, encoding="utf-8", newline="\n")
json.loads(text)  # well-formedness proof after write
n_cells = len(cell_lines)
print(f"wrote {out} — {n_cells} cells, {len(rels)} relations")
