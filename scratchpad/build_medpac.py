# Build omb/budget-appendix-fy2027-leg-medpac-salaries-expenses.cells.json
# Medicare Payment Advisory Commission (235-1550-0-1-571), corpus #100.
# P&F + ObjClass: PDF p31 (printed 43) right column; Employment Summary:
# PDF p32 (printed 44) left column top. Values read from boards-p31-render.png
# + boards-p31/p32-text.txt cross-check.
import json
from decimal import Decimal

M2 = "; schema minItems 2 forbids single-source sum"
MEMO = "Memorandum (non-add) entry: does not feed the section arithmetic"

ROWS = [
    ("0801 Medicare Payment Advisory Commission (Reimbursable)", ["14", "15", "15"]),
    ("0809 Reimbursable program activities, subtotal", ["14", "15", "15"]),
    ("1000 Unobligated balance brought forward, Oct 1", [None, None, "1"]),
    ("1100 Appropriation", [None, "1", None]),
    ("1700 Collected", ["14", "15", "15"]),
    ("1900 Budget authority (total)", ["14", "16", "15"]),
    ("1930 Total budgetary resources available", ["14", "16", "16"]),
    ("1941 Unexpired unobligated balance, end of year", [None, "1", "1"]),
    ("3000 Unpaid obligations, brought forward, Oct 1", ["3", "2", "2"]),
    ("3010 New obligations, unexpired accounts", ["14", "15", "15"]),
    ("3020 Outlays (gross)", ["-15", "-15", "-15"]),
    ("3050 Unpaid obligations, end of year", ["2", "2", "2"]),
    ("3100 Obligated balance, start of year", ["3", "2", "2"]),
    ("3200 Obligated balance, end of year", ["2", "2", "2"]),
    ("4000 Budget authority, gross", ["14", "16", "15"]),
    ("4010 Outlays from new discretionary authority", ["12", "11", "11"]),
    ("4011 Outlays from discretionary balances", ["3", "4", "4"]),
    ("4020 Outlays, gross (total)", ["15", "15", "15"]),
    ("4030 Federal sources", ["-14", "-15", "-15"]),
    ("4040 Offsets against gross budget authority and outlays (total)", ["-14", "-15", "-15"]),
    ("4180 Budget authority, net (total)", [None, "1", None]),
    ("4190 Outlays, net (total)", ["1", None, None]),
    ("11.1 Personnel compensation: Full-time permanent", ["6", "6", "7"]),
    ("12.1 Civilian personnel benefits", ["2", "2", "3"]),
    ("23.3 Communications, utilities, and miscellaneous charges", ["2", "2", "1"]),
    ("25.1 Advisory and assistance services", ["4", "4", "4"]),
    ("99.0 Reimbursable obligations", ["14", "14", "15"]),
    ("99.5 Adjustment for rounding", [None, "1", None]),
    ("99.9 Total new obligations, unexpired accounts", ["14", "15", "15"]),
    ("2001 Reimbursable civilian full-time equivalent employment", ["35", "36", "37"]),
]

RELATIONS = [
    ("1900", ["1100", "1700"], [2]),
    ("1930", ["1000", "1900"], [3]),
    ("3050", ["3000", "3010", "3020"], [1, 2, 3]),
    ("4020", ["4010", "4011"], [1, 2, 3]),
    ("4180", ["4000", "4040"], [2]),
    ("4190", ["4020", "4040"], [1]),
    ("99.0", ["11.1", "12.1", "23.3", "25.1"], [1, 2, 3]),
    ("99.9", ["99.0", "99.5"], [2]),
]

STANDALONE = {
    **{("0801", c): "Single-source into 0809 Reimbursable subtotal (sole program activity)" + M2 for c in (1, 2, 3)},
    **{("0809", c): "Single-source subtotal (equals sole activity 0801); this account prints no 0900 row, so the subtotal feeds nothing downstream" + M2 for c in (1, 2, 3)},
    ("1700", 1): "Single-source into 1900 Budget authority (1100 appropriation blank this column)" + M2,
    ("1700", 3): "Single-source into 1900 Budget authority (1100 appropriation blank this column)" + M2,
    ("1900", 1): "Single-source budget authority total (equals 1700 collected; 1100 blank this column); 1930 this column is also single-source" + M2,
    ("1930", 1): "Single-source total budgetary resources (equals 1900; 1000 unobligated balance blank this column)" + M2,
    ("1930", 2): "Single-source total budgetary resources (equals 1900; 1000 unobligated balance blank this column)" + M2,
    ("1941", 2): MEMO,
    ("1941", 3): MEMO,
    **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
    **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
    ("4000", 1): "Restates 1900 as gross discretionary budget authority; 4180 net prints blank this column (4000+4040 nets to zero, zero-suppressed), so no encodable relation" + M2,
    ("4000", 3): "Restates 1900 as gross discretionary budget authority; 4180 net prints blank this column (4000+4040 nets to zero, zero-suppressed), so no encodable relation" + M2,
    **{("4030", c): "Single-source into 4040 offsets total (only Federal-source collections)" + M2 for c in (1, 2, 3)},
    ("4040", 3): "Feeds 4180/4190 net lines, both of which print blank this column (net to zero, zero-suppressed), so no encodable relation exists",
    ("99.9", 1): "Single-source total new obligations (equals 99.0 Reimbursable; 99.5 rounding adjustment blank this column)" + M2,
    ("99.9", 3): "Single-source total new obligations (equals 99.0 Reimbursable; 99.5 rounding adjustment blank this column)" + M2,
    **{("2001", c): "Employment Summary line (full-time equivalent employment, a headcount, not USD millions); participates in no arithmetic on this schedule" for c in (1, 2, 3)},
}

code_row = {}
values = {}
for i, (label, vals) in enumerate(ROWS, 1):
    code = label.split()[0]
    code_row[code] = i
    for col, v in enumerate(vals, 1):
        if v is not None:
            values[(code, col)] = v

targets, sources, rels = set(), set(), []
for tgt, srcs, cols in RELATIONS:
    for col in cols:
        total = Decimal(0)
        for s in srcs:
            assert (s, col) in values, f"source {s} c{col} missing"
            total += Decimal(values[(s, col)])
            sources.add((s, col))
        assert total == Decimal(values[(tgt, col)]), \
            f"{tgt} c{col}: sum {total} != printed {values[(tgt, col)]}"
        targets.add((tgt, col))
        rels.append({"type": "sum",
                     "sources": [f"r{code_row[s]}c{col}" for s in srcs],
                     "target": f"r{code_row[tgt]}c{col}"})

cells, n_sa = [], 0
for i, (label, vals) in enumerate(ROWS, 1):
    code = label.split()[0]
    for col, v in enumerate(vals, 1):
        if v is None:
            continue
        key = (code, col)
        cell = {"id": f"r{i}c{col}", "row": i, "col": col, "value": v}
        if key in targets:
            cell["role"] = "total"
        elif key in STANDALONE:
            assert key not in sources, f"{key} standalone but is a source"
            cell["role"] = "standalone"
            cell["why"] = STANDALONE[key]
            n_sa += 1
        else:
            assert key in sources, f"{key} uncovered"
            cell["role"] = "leaf"
        cells.append(cell)

assert (len(cells), len(rels), n_sa) == (79, 14, 30), (len(cells), len(rels), n_sa)

doc = {
    "table_id": "omb/budget-appendix-fy2027-leg-medpac-salaries-expenses",
    "source": {
        "path": "sources/omb/budget-2027-app-2-3-legislative.pdf",
        "table": "235-1550-0-1-571",
        "page": 31,
        "title": "Medicare Payment Advisory Commission - Salaries and Expenses (Program and Financing + Object Classification + Employment Summary)",
        "period": "FY 2027"
    },
    "unit_note": "USD millions except the Employment Summary FTE line (headcount). Medicare Payment Advisory Commission (id 235-1550-0-1-571), first transcribed account of the Legislative Branch Boards and Commissions department: Program and Financing + Object Classification on PDF page 31 (printed page 43) RIGHT column (the left column is the separate US Commission on Security and Cooperation in Europe, 009-0110); Employment Summary on PDF page 32 (printed page 44) left column top. Fully reimbursable account (trust-fund transfer financing): prints no 0900 row, so the 0809 subtotal feeds nothing downstream. Blank (dotted-leader) cells not transcribed per convention (blank != zero) - notably 4180 c1/c3 and 4190 c2/c3, where gross and offsets net to zero and the print zero-suppresses the row, leaving the printed net lines encodable only in the columns where they appear (4180 c2 = 4000+4040, 4190 c1 = 4020+4040). 99.5 'Adjustment for rounding' is a printed source line (c2 only) and 99.9 c2 = 99.0 + 99.5 sums EXACTLY as printed - no tolerance involved. Negatives as printed (3020, 4030, 4040).",
    "columns": [
        {"index": 1, "label": "2025 actual"},
        {"index": 2, "label": "2026 est."},
        {"index": 3, "label": "2027 est."}
    ],
    "rows": [{"index": i, "label": label} for i, (label, _) in enumerate(ROWS, 1)],
    "cells": cells,
    "relations": rels,
}

out = "tables/omb/budget-appendix-fy2027-leg-medpac-salaries-expenses.cells.json"
with open(out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"wrote {out}: {len(cells)} cells, {len(rels)} relations, {n_sa} standalone")
