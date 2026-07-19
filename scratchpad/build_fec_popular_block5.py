"""Builder for fec/2024-presidential-general-popular-block-5.cells.json.

Grid verified 2026-07-17 (Kimi): positioned pdfplumber extraction (5 x-band
columns) + per-column sums re-derived == printed Totals
(82,644 / 1,144 / 19,625 / 210,381 / 155,238,302, all exact)
+ visual render check (scratchpad/fec-p6-render.png).
"""
import json
from pathlib import Path

CANDIDATES = ["WEST", "WOOD", "NONE OF THESE CANDIDATES", "WRITE-IN VOTES (SCATTERED)", "TOTAL VOTES"]
PCTS = ["0.05", "0.00", "0.01", "0.14", None]  # TOTAL VOTES pct blank as printed
TOTALS = ["82644", "1144", "19625", "210381", "155238302"]

GRID = [
    ("AL", [None, None, None, "8738", "2265090"]),
    ("AK", ["1127", None, None, None, "338177"]),
    ("AZ", [None, None, None, "23", "3390161"]),
    ("AR", [None, "1144", None, None, "1182676"]),
    ("CA", [None, None, None, None, "15865475"]),
    ("CO", ["5149", None, None, "12", "3192745"]),
    ("CT", ["128", None, None, "6", "1759010"]),
    ("DE", ["96", None, None, "16", "512912"]),
    ("DC", [None, None, None, "7830", "325869"]),
    ("FL", [None, None, None, "6", "10893752"]),
    ("GA", [None, None, None, "61", "5250905"]),
    ("HI", [None, None, None, None, "516701"]),
    ("ID", [None, None, None, "3", "905057"]),
    ("IL", ["1569", None, None, "518", "5633310"]),
    ("IN", ["722", None, None, "76", "2936677"]),
    ("IA", [None, None, None, "6657", "1663506"]),
    ("KS", [None, None, None, None, "1327591"]),
    ("KY", ["177", None, None, "24", "2074530"]),
    ("LA", ["2623", None, None, None, "2006975"]),
    ("ME", ["2912", None, None, "581", "831375"]),
    ("MD", ["918", None, None, "19572", "3038334"]),
    ("MA", ["243", None, None, "19737", "3473668"]),
    ("MI", ["6664", None, None, "8", "5664186"]),
    ("MN", ["3136", None, None, "12118", "3253920"]),
    ("MS", [None, None, None, None, "1228008"]),
    ("MO", [None, None, None, "10", "2995327"]),
    ("MT", [None, None, None, "6", "602990"]),
    ("NE", ["3062", None, None, "5023", "952182"]),
    ("NV", [None, None, "19625", None, "1484840"]),
    ("NH", [None, None, None, "4073", "826189"]),
    ("NJ", [None, None, None, None, "4272725"]),
    ("NM", [None, None, None, None, "923403"]),
    ("NY", ["4152", None, None, "100", "8262495"]),
    ("NC", ["12099", None, None, "18936", "5699141"]),
    ("ND", [None, None, None, "3096", "368155"]),
    ("OH", ["852", None, None, "31", "5767788"]),
    ("OK", [None, None, None, None, "1566173"]),
    ("OR", ["5644", None, None, "15026", "2244493"]),
    ("PA", [None, None, None, "24526", "7058732"]),
    ("RI", [None, None, None, "2727", "513386"]),
    ("SC", ["6744", None, None, None, "2548140"]),
    ("SD", [None, None, None, None, "428922"]),
    ("TN", [None, None, None, None, "3063942"]),
    ("TX", ["1858", None, None, "124", "11388674"]),
    ("UT", ["2199", None, None, "43", "1488494"]),
    ("VT", ["1549", None, None, "2072", "369422"]),
    ("VA", ["8975", None, None, "23348", "4503288"]),
    ("WA", ["7254", None, None, "25408", "3924243"]),
    ("WV", ["39", None, None, "7", "762582"]),
    ("WI", ["2753", None, None, "7144", "3422918"]),
    ("WY", [None, None, None, "2695", "269048"]),
]

assert len(GRID) == 51
for ci, tot in enumerate(TOTALS):
    s = sum(int(g[1][ci]) for g in GRID if g[1][ci] is not None)
    assert s == int(tot), (CANDIDATES[ci], s, tot)

SINGLE = {ci for ci in range(5) if sum(1 for g in GRID if g[1][ci] is not None) == 1}
assert SINGLE == {1, 2}, SINGLE  # WOOD (AR), NONE OF THESE CANDIDATES (NV)

lines = []
add = lines.append
add("{")
add('  "table_id": "fec/2024-presidential-general-popular-block-5",')
add('  "source": {')
add('    "path": "sources/fec/2024presgeresults.pdf",')
add('    "table": "OFFICIAL 2024 PRESIDENTIAL GENERAL ELECTION RESULTS — page 6, popular vote block 5 (WEST, WOOD, NONE OF THESE CANDIDATES, WRITE-IN VOTES (SCATTERED), TOTAL VOTES)",')
add('    "title": "FEC official 2024 presidential general election results — popular vote, final block incl. TOTAL VOTES",')
add('    "period": "General Election Date: 11/05/2024 (source: State Elections Offices)"')
add("  },")
add('  "unit_note": "The final popular-vote block. WEST appears in 26 jurisdictions; WRITE-IN VOTES (SCATTERED) in 37; TOTAL VOTES (per-state all-candidate totals) in all 51 — its full per-row decomposition spans every candidate block, so row-level verification belongs to the planned cross-page capstone (re-anchor pattern); here the column feeds the national column sum (155,238,302). WOOD (AR only) and NONE OF THESE CANDIDATES (NV only — Nevada\'s ballot option) are single-jurisdiction columns whose printed state cell equals the printed national total — standalone per the schema >=2-source rule. The TOTAL VOTES percentage cell is blank as printed. Blank cells are not transcribed (blank is not zero). Candidate columns carry labels as printed (WRITE-IN VOTES (SCATTERED) prints over two header lines; NONE OF THESE CANDIDATES over two). Column assignment verified from the positioned text layer plus the page-6 render.",')
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
            cell_lines.append(f'    {{ "id": "r{i}c{ci}", "row": {i}, "col": {ci}, "value": "{v}", "role": "standalone", "why": "{CANDIDATES[ci0]} appears in this single jurisdiction only, so the printed state cell equals the printed national total; the frozen schema requires >=2 sources for a sum relation — no honest in-schema relation exists." }}')
        else:
            cell_lines.append(f'    {{ "id": "r{i}c{ci}", "row": {i}, "col": {ci}, "value": "{v}", "role": "leaf" }}')
for ci0, tot in enumerate(TOTALS):
    ci = ci0 + 1
    if ci0 in SINGLE:
        cell_lines.append(f'    {{ "id": "r52c{ci}", "row": 52, "col": {ci}, "value": "{tot}", "role": "standalone", "why": "{CANDIDATES[ci0]} national total equals its single jurisdiction cell (single-source column); the frozen schema requires >=2 sources for a sum relation — no honest in-schema relation exists." }}')
    else:
        cell_lines.append(f'    {{ "id": "r52c{ci}", "row": 52, "col": {ci}, "value": "{tot}", "role": "total" }}')
for ci0, pct in enumerate(PCTS):
    if pct is None:
        continue
    ci = ci0 + 1
    cell_lines.append(f'    {{ "id": "r53c{ci}", "row": 53, "col": {ci}, "value": "{pct}", "role": "standalone", "unit": "%", "why": "Share of the national total popular vote (155,238,302, transcribed in this unit as r52c5) — the candidate-column denominators span blocks and the per-state decompositions are the planned capstone\'s; no honest relation exists within this block." }}')
add(",\n".join(cell_lines))
add("  ],")

rel_lines = []
for ci0, name in enumerate(CANDIDATES):
    if ci0 in SINGLE:
        continue
    ci = ci0 + 1
    srcs = [f'"r{i}c{ci}"' for i, g in enumerate(GRID, 1) if g[1][ci0] is not None]
    rel_lines.append(f'    {{ "type": "sum", "sources": [{", ".join(srcs)}], "target": "r52c{ci}", "note": "jurisdiction cells for {name} sum to the printed national Total {TOTALS[ci0]}" }}')
add('  "relations": [')
add(",\n".join(rel_lines))
add("  ]")
add("}")

out = Path("tables/fec/2024-presidential-general-popular-block-5.cells.json")
text = "\n".join(lines) + "\n"
out.write_text(text, encoding="utf-8", newline="\n")
json.loads(text)
print(f"wrote {out} — {len(cell_lines)} cells, {len(rel_lines)} relations")
