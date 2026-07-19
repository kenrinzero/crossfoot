"""Builder for fec/2024-presidential-general-popular-block-4.cells.json.

Grid verified 2026-07-17 (Kimi): positioned pdfplumber extraction (5 x-band
columns) + per-candidate sums re-derived == printed Totals
(364 / 921 / 41,294 / 77,302,580 / 359, all exact)
+ visual render check (scratchpad/fec-p5-render.png).
"""
import json
from pathlib import Path

CANDIDATES = ["STODDEN", "SUPREME", "TERRY", "TRUMP", "WELLS"]
PCTS = ["0.00", "0.00", "0.03", "49.80", "0.00"]
TOTALS = ["364", "921", "41294", "77302580", "359"]

GRID = [
    ("AL", [None, None, None, "1462616", None]),
    ("AK", [None, None, "812", "184458", None]),
    ("AZ", [None, None, None, "1770242", None]),
    ("AR", [None, None, None, "759241", None]),
    ("CA", [None, None, None, "6081697", None]),
    ("CO", [None, None, "3522", "1377441", None]),
    ("CT", [None, None, None, "736918", None]),
    ("DE", [None, "914", None, "214351", None]),
    ("DC", [None, None, None, "21076", None]),
    ("FL", [None, None, "5834", "6110125", None]),
    ("GA", [None, None, None, "2663117", None]),
    ("HI", [None, None, None, "193661", None]),
    ("ID", [None, None, "1026", "605246", None]),
    ("IL", [None, None, None, "2449079", None]),
    ("IN", [None, None, None, "1720347", None]),
    ("IA", ["361", None, None, "927019", None]),
    ("KS", [None, None, None, "758802", None]),
    ("KY", [None, None, None, "1337494", None]),
    ("LA", [None, None, "1424", "1208505", None]),
    ("ME", [None, None, None, "377977", None]),
    ("MD", ["3", None, None, "1035550", None]),
    ("MA", [None, None, None, "1251303", None]),
    ("MI", [None, None, "6509", "2816636", None]),
    ("MN", [None, None, None, "1519032", None]),
    ("MS", [None, None, "1030", "747744", None]),
    ("MO", [None, None, None, "1751986", None]),
    ("MT", [None, None, None, "352079", None]),
    ("NE", [None, None, None, "564816", None]),
    ("NV", [None, None, None, "751205", None]),
    ("NH", [None, None, None, "395523", None]),
    ("NJ", [None, None, "3024", "1968215", None]),
    ("NM", [None, None, None, "423391", None]),
    ("NY", [None, None, None, "3578899", None]),
    ("NC", [None, None, "6863", "2898423", None]),
    ("ND", [None, None, None, "246505", None]),
    ("OH", [None, None, None, "3180116", None]),
    ("OK", [None, None, None, "1036213", None]),
    ("OR", [None, None, "1850", "919480", None]),
    ("PA", [None, None, None, "3543308", None]),
    ("RI", [None, None, None, "214406", "359"]),
    ("SC", [None, None, "5352", "1483747", None]),
    ("SD", [None, None, None, "272081", None]),
    ("TN", [None, None, None, "1966865", None]),
    ("TX", [None, None, None, "6393597", None]),
    ("UT", [None, None, None, "883818", None]),
    ("VT", [None, "7", "4", "119395", None]),
    ("VA", [None, None, None, "2074097", None]),
    ("WA", [None, None, None, "1530923", None]),
    ("WV", [None, None, None, "533556", None]),
    ("WI", [None, None, "4044", "1697626", None]),
    ("WY", [None, None, None, "192633", None]),
]

assert len(GRID) == 51
for ci, tot in enumerate(TOTALS):
    s = sum(int(g[1][ci]) for g in GRID if g[1][ci] is not None)
    assert s == int(tot), (CANDIDATES[ci], s, tot)

SINGLE = {ci for ci in range(5) if sum(1 for g in GRID if g[1][ci] is not None) == 1}
assert SINGLE == {4}, SINGLE  # WELLS (RI)

lines = []
add = lines.append
add("{")
add('  "table_id": "fec/2024-presidential-general-popular-block-4",')
add('  "source": {')
add('    "path": "sources/fec/2024presgeresults.pdf",')
add('    "table": "OFFICIAL 2024 PRESIDENTIAL GENERAL ELECTION RESULTS — page 5, popular vote block 4 (candidates STODDEN through WELLS)",')
add('    "title": "FEC official 2024 presidential general election results — popular vote, candidates STODDEN–WELLS",')
add('    "period": "General Election Date: 11/05/2024 (source: State Elections Offices)"')
add("  },")
add('  "unit_note": "The TRUMP block: TRUMP prints in all 51 jurisdictions (77,302,580 total); TERRY is scattered (13); STODDEN (IA, MD) and SUPREME (DE, VT) appear twice each — their two-cell column sums are valid relations at the schema minimum of two sources; WELLS (RI only) is a single-jurisdiction candidate whose printed state cell equals the printed national total, so his cells are standalone with the equality stated in why. Blank cells are not transcribed (blank is not zero). Candidate columns carry surnames only, as printed. The Percentage row is each candidate\'s share of the national total popular vote; the denominator (national TOTAL VOTES) prints on the final block and is re-anchored by the planned cross-page capstone unit, so the percentage cells are standalone here. Column assignment verified from the positioned text layer plus the page-5 render.",')
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
    for ci0, v in enumerate(vals):
        if v is None:
            continue
        ci = ci0 + 1
        if ci0 in SINGLE:
            cell_lines.append(f'    {{ "id": "r{i}c{ci}", "row": {i}, "col": {ci}, "value": "{v}", "role": "standalone", "why": "{CANDIDATES[ci0]} appears on the ballot in this single jurisdiction only, so the printed state cell equals the printed national total; the frozen schema requires >=2 sources for a sum relation — no honest in-schema relation exists." }}')
        else:
            cell_lines.append(f'    {{ "id": "r{i}c{ci}", "row": {i}, "col": {ci}, "value": "{v}", "role": "leaf" }}')
for ci0, tot in enumerate(TOTALS):
    ci = ci0 + 1
    if ci0 in SINGLE:
        cell_lines.append(f'    {{ "id": "r52c{ci}", "row": 52, "col": {ci}, "value": "{tot}", "role": "standalone", "why": "{CANDIDATES[ci0]} national total equals its single jurisdiction cell (single-source column); the frozen schema requires >=2 sources for a sum relation — no honest in-schema relation exists." }}')
    else:
        cell_lines.append(f'    {{ "id": "r52c{ci}", "row": 52, "col": {ci}, "value": "{tot}", "role": "total" }}')
for ci, pct in enumerate(PCTS, 1):
    cell_lines.append(f'    {{ "id": "r53c{ci}", "row": 53, "col": {ci}, "value": "{pct}", "role": "standalone", "unit": "%", "why": "Share of the national total popular vote; the denominator (national TOTAL VOTES) prints on the final popular-vote block and is re-anchored by the planned cross-page capstone unit — no honest relation exists within this block." }}')
add(",\n".join(cell_lines))
add("  ],")

rel_lines = []
for ci0, name in enumerate(CANDIDATES):
    if ci0 in SINGLE:
        continue
    ci = ci0 + 1
    srcs = [f'"r{i}c{ci}"' for i, g in enumerate(GRID, 1) if g[1][ci0] is not None]
    rel_lines.append(f'    {{ "type": "sum", "sources": [{", ".join(srcs)}], "target": "r52c{ci}", "note": "jurisdiction popular-vote cells for {name} sum to the printed national Total {TOTALS[ci0]}" }}')
add('  "relations": [')
add(",\n".join(rel_lines))
add("  ]")
add("}")

out = Path("tables/fec/2024-presidential-general-popular-block-4.cells.json")
text = "\n".join(lines) + "\n"
out.write_text(text, encoding="utf-8", newline="\n")
json.loads(text)
print(f"wrote {out} — {len(cell_lines)} cells, {len(rel_lines)} relations")
