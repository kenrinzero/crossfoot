"""Builder for fec/2024-presidential-general-popular-block-2.cells.json.

Grid verified 2026-07-17 (Kimi): positioned pdfplumber extraction (6 x-band
columns) + per-candidate sums re-derived == printed Totals
(2,653 / 4,118 / 5,297 / 75,017,613 / 2,196 / 756,393, all exact)
+ visual render check (scratchpad/fec-p3-render.png).
"""
import json
from pathlib import Path

CANDIDATES = ["EVERYLOVE", "FRUIT", "GARRITY", "HARRIS", "HUBER", "KENNEDY"]
PCTS = ["0.00", "0.00", "0.00", "48.32", "0.00", "0.49"]
TOTALS = ["2653", "4118", "5297", "75017613", "2196", "756393"]

GRID = [
    ("AL", [None, None, None, "772412", None, "12075"]),
    ("AK", [None, None, None, "140026", None, "5670"]),
    ("AZ", [None, None, None, "1582860", None, None]),
    ("AR", [None, None, None, "396905", None, "13255"]),
    ("CA", [None, None, None, "9276179", None, "197645"]),
    ("CO", [None, None, "30", "1728159", "2196", "35623"]),
    ("CT", [None, None, None, "992053", None, "8448"]),
    ("DE", [None, None, None, "289758", None, "4636"]),
    ("DC", [None, None, None, "294185", None, "2778"]),
    ("FL", [None, None, None, "4683038", None, None]),
    ("GA", [None, None, None, "2548017", None, None]),
    ("HI", [None, None, None, "313044", None, None]),
    ("ID", [None, None, None, "274972", None, "12812"]),
    ("IL", [None, None, None, "3062863", None, "80426"]),
    ("IN", [None, None, None, "1163603", None, "29325"]),
    ("IA", [None, None, None, "707278", None, "13122"]),
    ("KS", [None, None, None, "544853", None, "16322"]),
    ("KY", [None, None, None, "704043", None, "16769"]),
    ("LA", [None, "361", None, "766870", None, "6641"]),
    ("ME", [None, None, None, "435652", None, None]),
    ("MD", [None, None, None, "1902577", None, "28819"]),
    ("MA", [None, None, None, "2126518", None, None]),
    ("MI", [None, None, None, "2736533", None, "26785"]),
    ("MN", [None, "457", "3", "1656979", None, "24001"]),
    ("MS", [None, None, None, "466668", None, "5387"]),
    ("MO", [None, None, None, "1200599", None, None]),
    ("MT", [None, None, None, "231906", None, "11825"]),
    ("NE", [None, None, None, "369995", None, None]),
    ("NV", [None, None, None, "705197", None, None]),
    ("NH", [None, None, None, "418488", None, None]),
    ("NJ", [None, "1277", None, "2220713", None, "23479"]),
    ("NM", [None, None, None, "478802", None, "9553"]),
    ("NY", [None, None, "108", "4619195", None, None]),
    ("NC", [None, None, None, "2715375", None, None]),
    ("ND", [None, None, None, "112327", None, None]),
    ("OH", [None, None, "13", "2533699", None, None]),
    ("OK", [None, None, "5143", "499599", None, "16020"]),
    ("OR", [None, None, None, "1240600", None, "33733"]),
    ("PA", [None, None, None, "3423042", None, None]),
    ("RI", [None, None, None, "285156", None, "5045"]),
    ("SC", [None, None, None, "1028452", None, None]),
    ("SD", [None, None, None, "146859", None, "7204"]),
    ("TN", [None, "988", None, "1056265", None, "21535"]),
    ("TX", [None, None, None, "4835250", None, None]),
    ("UT", ["2653", None, None, "562566", None, None]),
    ("VT", [None, "211", None, "235791", None, "5905"]),
    ("VA", [None, None, None, "2333778", None, None]),
    ("WA", [None, "824", None, "2245849", None, "54868"]),
    ("WV", [None, None, None, "214309", None, "8947"]),
    ("WI", [None, None, None, "1668229", None, "17740"]),
    ("WY", [None, None, None, "69527", None, None]),
]

assert len(GRID) == 51
for ci, tot in enumerate(TOTALS):
    s = sum(int(g[1][ci]) for g in GRID if g[1][ci] is not None)
    assert s == int(tot), (CANDIDATES[ci], s, tot)

# columns with a single jurisdiction cell -> standalone (schema minItems: 2)
SINGLE = {ci for ci in range(6) if sum(1 for g in GRID if g[1][ci] is not None) == 1}
assert SINGLE == {0, 4}, SINGLE  # EVERYLOVE (UT), HUBER (CO)

lines = []
add = lines.append
add("{")
add('  "table_id": "fec/2024-presidential-general-popular-block-2",')
add('  "source": {')
add('    "path": "sources/fec/2024presgeresults.pdf",')
add('    "table": "OFFICIAL 2024 PRESIDENTIAL GENERAL ELECTION RESULTS — page 3, popular vote block 2 (candidates EVERYLOVE through KENNEDY)",')
add('    "title": "FEC official 2024 presidential general election results — popular vote, candidates EVERYLOVE–KENNEDY",')
add('    "period": "General Election Date: 11/05/2024 (source: State Elections Offices)"')
add("  },")
add('  "unit_note": "First major-candidate block: HARRIS prints in all 51 jurisdictions; KENNEDY is broadly on-ballot; the remaining four are sparse. Blank cells are not transcribed (blank is not zero). Candidate columns carry surnames only, as printed. EVERYLOVE (UT only) and HUBER (CO only) are single-jurisdiction candidates whose printed state cell equals the printed national total; since the schema requires at least two relation sources, their cells are standalone with the equality stated in why. The Percentage row is each candidate\'s share of the national total popular vote; the denominator (national TOTAL VOTES) prints on the final block and is re-anchored by the planned cross-page capstone unit, so the percentage cells are standalone here. Column assignment verified from the positioned text layer plus the page-3 render.",')
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

out = Path("tables/fec/2024-presidential-general-popular-block-2.cells.json")
text = "\n".join(lines) + "\n"
out.write_text(text, encoding="utf-8", newline="\n")
json.loads(text)
print(f"wrote {out} — {len(cell_lines)} cells, {len(rel_lines)} relations")
