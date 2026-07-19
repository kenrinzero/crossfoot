"""Builder for fec/2024-presidential-general-popular-block-3a and -3b.

Grid verified 2026-07-17 (Kimi): positioned pdfplumber extraction (6 x-band
columns) + per-candidate sums re-derived == printed Totals
(4,651 / 650,126 / 2,857 / 12,786 / 44,000 / 862,049, all exact)
+ visual render check (scratchpad/fec-p4-render.png).
Whole p4 block = 141 cells > 140 ceiling -> split by column groups:
  3a = KISHORE, OLIVER, PRESTON   (63 cells, 2 relations)
  3b = SKOUSEN, SONSKI, STEIN     (78 cells, 3 relations)
"""
import json
from pathlib import Path

CANDIDATES = ["KISHORE", "OLIVER", "PRESTON", "SKOUSEN", "SONSKI", "STEIN"]
PCTS = ["0.00", "0.42", "0.00", "0.01", "0.03", "0.56"]
TOTALS = ["4651", "650126", "2857", "12786", "44000", "862049"]

GRID = [
    ("AL", [None, "4930", None, None, None, "4319"]),
    ("AK", [None, "3040", None, None, "702", "2342"]),
    ("AZ", [None, "17898", None, "53", None, "18319"]),
    ("AR", [None, "5715", None, None, "2141", "4275"]),
    ("CA", [None, "66662", None, None, "2939", "167814"]),
    ("CO", [None, "21439", None, None, "910", "17344"]),
    ("CT", [None, "6729", None, None, "162", "14281"]),
    ("DE", [None, "2038", None, None, "98", "914"]),
    ("DC", [None]*6),
    ("FL", [None, "31972", None, None, "7454", "43155"]),
    ("GA", [None, "20684", None, None, "730", "18229"]),
    ("HI", [None, "2733", None, None, "936", "4387"]),
    ("ID", [None, "4462", None, "1577", "242", "2973"]),
    ("IL", ["12", "3510", None, None, "1391", "31023"]),
    ("IN", [None, "20425", None, None, "1347", None]),
    ("IA", [None, "7218", None, None, None, None]),
    ("KS", [None, "7614", None, None, None, None]),
    ("KY", ["8", "6422", None, None, "611", "7566"]),
    ("LA", [None, "6835", "2857", None, "2240", "7138"]),
    ("ME", [None, "5286", None, None, None, "8967"]),
    ("MD", ["12", "15570", None, None, "1012", "33134"]),
    ("MA", [None, "17735", None, None, "280", "26545"]),
    ("MI", ["2330", "22440", None, None, "1212", "44607"]),
    ("MN", ["1", "15155", None, None, "882", "16275"]),
    ("MS", [None, "2536", None, None, "1007", "1873"]),
    ("MO", [None, "23876", None, None, "1069", "17135"]),
    ("MT", [None, "4275", None, None, None, "2878"]),
    ("NE", [None, "6399", None, None, None, "2887"]),
    ("NV", [None, "6059", None, "2754", None, None]),
    ("NH", [None, "4425", None, None, None, "3680"]),
    ("NJ", ["1371", "10500", None, None, None, "39041"]),
    ("NM", [None, "3745", None, None, None, "4611"]),
    ("NY", [None, "5338", None, None, "1544", "46698"]),
    ("NC", [None, "22125", None, None, None, "24762"]),
    ("ND", [None, "6227", None, None, None, None]),
    ("OH", [None, "28200", None, None, "10197", None]),
    ("OK", [None, "9198", None, None, None, None]),
    ("OR", [None, "9061", None, None, None, "19099"]),
    ("PA", [None, "33318", None, None, None, "34538"]),
    ("RI", [None, "1617", None, None, None, "2900"]),
    ("SC", [None, "12669", None, None, None, "8117"]),
    ("SD", [None, "2778", None, None, None, None]),
    ("TN", [None, None, None, None, None, "8967"]),
    ("TX", [None, "68557", None, None, "3780", "82701"]),
    ("UT", [None, "16902", None, "8402", "441", "8222"]),
    ("VT", [None, "1828", None, None, "49", "893"]),
    ("VA", [None, "19802", None, None, None, "34880"]),
    ("WA", ["917", "16428", None, None, None, "29754"]),
    ("WV", [None, "3047", None, None, "63", "2531"]),
    ("WI", [None, "10511", None, None, "561", "12275"]),
    ("WY", [None, "4193", None, None, None, None]),
]

assert len(GRID) == 51
for ci, tot in enumerate(TOTALS):
    s = sum(int(g[1][ci]) for g in GRID if g[1][ci] is not None)
    assert s == int(tot), (CANDIDATES[ci], s, tot)


def build(suffix, col_idxs, page_note):
    names = [CANDIDATES[i] for i in col_idxs]
    single = {i for i in col_idxs if sum(1 for g in GRID if g[1][i] is not None) == 1}
    lines = []
    add = lines.append
    add("{")
    add(f'  "table_id": "fec/2024-presidential-general-popular-block-3{suffix}",')
    add('  "source": {')
    add('    "path": "sources/fec/2024presgeresults.pdf",')
    add(f'    "table": "OFFICIAL 2024 PRESIDENTIAL GENERAL ELECTION RESULTS — page 4, popular vote block 3{suffix} (candidates {", ".join(names)})",')
    add(f'    "title": "FEC official 2024 presidential general election results — popular vote, candidates {"–".join([names[0], names[-1]])}",')
    add('    "period": "General Election Date: 11/05/2024 (source: State Elections Offices)"')
    add("  },")
    add(f'  "unit_note": "{page_note} Blank cells are not transcribed (blank is not zero). Candidate columns carry surnames only, as printed. The Percentage row is each candidate\'s share of the national total popular vote; the denominator (national TOTAL VOTES) prints on the final block and is re-anchored by the planned cross-page capstone unit, so the percentage cells are standalone here. Column assignment verified from the positioned text layer plus the page-4 render.",')
    add('  "columns": [')
    for j, i in enumerate(col_idxs, 1):
        comma = "," if j < len(col_idxs) else ""
        add(f'    {{ "index": {j}, "label": "{CANDIDATES[i]}" }}{comma}')
    add("  ],")
    add('  "rows": [')
    for i, g in enumerate(GRID, 1):
        add(f'    {{ "index": {i}, "label": "{g[0]}" }},')
    add('    { "index": 52, "label": "Total:" },')
    add('    { "index": 53, "label": "Percentage: (share of national total popular vote)" }')
    add("  ],")
    add('  "cells": [')

    cell_lines = []
    for ri, (code, vals) in enumerate(GRID, 1):
        for j, i in enumerate(col_idxs, 1):
            v = vals[i]
            if v is None:
                continue
            if i in single:
                cell_lines.append(f'    {{ "id": "r{ri}c{j}", "row": {ri}, "col": {j}, "value": "{v}", "role": "standalone", "why": "{CANDIDATES[i]} appears on the ballot in this single jurisdiction only, so the printed state cell equals the printed national total; the frozen schema requires >=2 sources for a sum relation — no honest in-schema relation exists." }}')
            else:
                cell_lines.append(f'    {{ "id": "r{ri}c{j}", "row": {ri}, "col": {j}, "value": "{v}", "role": "leaf" }}')
    for j, i in enumerate(col_idxs, 1):
        if i in single:
            cell_lines.append(f'    {{ "id": "r52c{j}", "row": 52, "col": {j}, "value": "{TOTALS[i]}", "role": "standalone", "why": "{CANDIDATES[i]} national total equals its single jurisdiction cell (single-source column); the frozen schema requires >=2 sources for a sum relation — no honest in-schema relation exists." }}')
        else:
            cell_lines.append(f'    {{ "id": "r52c{j}", "row": 52, "col": {j}, "value": "{TOTALS[i]}", "role": "total" }}')
    for j, i in enumerate(col_idxs, 1):
        cell_lines.append(f'    {{ "id": "r53c{j}", "row": 53, "col": {j}, "value": "{PCTS[i]}", "role": "standalone", "unit": "%", "why": "Share of the national total popular vote; the denominator (national TOTAL VOTES) prints on the final popular-vote block and is re-anchored by the planned cross-page capstone unit — no honest relation exists within this block." }}')
    add(",\n".join(cell_lines))
    add("  ],")

    rel_lines = []
    for j, i in enumerate(col_idxs, 1):
        if i in single:
            continue
        srcs = [f'"r{ri}c{j}"' for ri, g in enumerate(GRID, 1) if g[1][i] is not None]
        rel_lines.append(f'    {{ "type": "sum", "sources": [{", ".join(srcs)}], "target": "r52c{j}", "note": "jurisdiction popular-vote cells for {CANDIDATES[i]} sum to the printed national Total {TOTALS[i]}" }}')
    add('  "relations": [')
    add(",\n".join(rel_lines))
    add("  ]")
    add("}")

    out = Path(f"tables/fec/2024-presidential-general-popular-block-3{suffix}.cells.json")
    text = "\n".join(lines) + "\n"
    out.write_text(text, encoding="utf-8", newline="\n")
    json.loads(text)
    print(f"wrote {out} — {len(cell_lines)} cells, {len(rel_lines)} relations")


build("a", [0, 1, 2],
      "Page-4 block split at the 140-cell ceiling (whole block = 141 cells): this sub-unit carries KISHORE, OLIVER, PRESTON. PRESTON (LA only) is a single-jurisdiction candidate whose printed state cell equals the printed national total — standalone per the schema >=2-source rule. OLIVER is near-dense (49/51).")
build("b", [3, 4, 5],
      "Page-4 block split at the 140-cell ceiling (whole block = 141 cells): this sub-unit carries SKOUSEN, SONSKI, STEIN. STEIN is dense (41/51), SONSKI broad (27), SKOUSEN sparse (4).")
