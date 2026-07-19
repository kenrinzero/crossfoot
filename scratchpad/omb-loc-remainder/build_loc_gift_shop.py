import json
from pathlib import Path

rows = [
    (1, "0801 National Library"),
    (2, "1000 Unobligated balance brought forward, Oct 1"),
    (3, "1700 Collected"),
    (4, "1930 Total budgetary resources available"),
    (5, "1941 Unexpired unobligated balance, end of year"),
    (6, "3000 Unpaid obligations, brought forward, Oct 1"),
    (7, "3010 New obligations, unexpired accounts"),
    (8, "3020 Outlays (gross)"),
    (9, "3050 Unpaid obligations, end of year"),
    (10, "3100 Obligated balance, start of year"),
    (11, "3200 Obligated balance, end of year"),
    (12, "4000 Budget authority, gross"),
    (13, "4010 Outlays from new discretionary authority"),
    (14, "4011 Outlays from discretionary balances"),
    (15, "4020 Outlays, gross (total)"),
    (16, "4030 Federal sources"),
    (17, "4033 Non-Federal sources"),
    (18, "4040 Offsets against gross budget authority and outlays (total)"),
    (19, "4080 Outlays, net (discretionary)"),
    (20, "4190 Outlays, net (total)"),
    (21, "11.1 Personnel compensation: Full-time permanent"),
    (22, "12.1 Civilian personnel benefits"),
    (23, "25.1 Advisory and assistance services"),
    (24, "25.2 Other services from non-Federal sources"),
    (25, "25.3 Other goods and services from Federal sources"),
    (26, "26.0 Supplies and materials"),
    (27, "44.0 Refunds"),
    (28, "99.0 Reimbursable obligations"),
    (29, "99.5 Adjustment for rounding"),
    (30, "99.9 Total new obligations, unexpired accounts"),
    (31, "2001 Reimbursable civilian full-time equivalent employment"),
]

columns = [(1, "2025 actual"), (2, "2026 est."), (3, "2027 est.")]

values = {
    1: {1: "8", 2: "12", 3: "12"},
    2: {1: "8", 2: "8", 3: "8"},
    3: {1: "8", 2: "12", 3: "12"},
    4: {1: "16", 2: "20", 3: "20"},
    5: {1: "8", 2: "8", 3: "8"},
    6: {3: "1"},
    7: {1: "8", 2: "12", 3: "12"},
    8: {1: "-8", 2: "-11", 3: "-11"},
    9: {2: "1", 3: "2"},
    10: {3: "1"},
    11: {2: "1", 3: "2"},
    12: {1: "8", 2: "12", 3: "12"},
    13: {1: "8", 2: "10", 3: "10"},
    14: {2: "1", 3: "1"},
    15: {1: "8", 2: "11", 3: "11"},
    16: {1: "-4", 2: "-12", 3: "-12"},
    17: {1: "-4"},
    18: {1: "-8", 2: "-12", 3: "-12"},
    19: {2: "-1", 3: "-1"},
    20: {2: "-1", 3: "-1"},
    21: {1: "1", 2: "2", 3: "2"},
    22: {1: "1", 2: "1", 3: "1"},
    23: {2: "1", 3: "1"},
    24: {1: "3", 2: "5", 3: "5"},
    25: {2: "1", 3: "1"},
    26: {1: "1", 2: "1", 3: "1"},
    27: {1: "1"},
    28: {1: "7", 2: "11", 3: "11"},
    29: {1: "1", 2: "1", 3: "1"},
    30: {1: "8", 2: "12", 3: "12"},
    31: {1: "17", 2: "29", 3: "29"},
}

relations = [
    {"target": "r4c1", "sources": ["r2c1", "r3c1"], "type": "sum"},
    {"target": "r4c2", "sources": ["r2c2", "r3c2"], "type": "sum"},
    {"target": "r4c3", "sources": ["r2c3", "r3c3"], "type": "sum"},
    {"target": "r9c2", "sources": ["r7c2", "r8c2"], "type": "sum"},
    {"target": "r9c3", "sources": ["r6c3", "r7c3", "r8c3"], "type": "sum"},
    {"target": "r15c2", "sources": ["r13c2", "r14c2"], "type": "sum"},
    {"target": "r15c3", "sources": ["r13c3", "r14c3"], "type": "sum"},
    {"target": "r18c1", "sources": ["r16c1", "r17c1"], "type": "sum"},
    {"target": "r19c2", "sources": ["r15c2", "r18c2"], "type": "sum"},
    {"target": "r19c3", "sources": ["r15c3", "r18c3"], "type": "sum"},
    {"target": "r28c1", "sources": ["r21c1", "r22c1", "r24c1", "r26c1", "r27c1"], "type": "sum"},
    {"target": "r28c2", "sources": ["r21c2", "r22c2", "r23c2", "r24c2", "r25c2", "r26c2"], "type": "sum"},
    {"target": "r28c3", "sources": ["r21c3", "r22c3", "r23c3", "r24c3", "r25c3", "r26c3"], "type": "sum"},
    {"target": "r30c1", "sources": ["r28c1", "r29c1"], "type": "sum"},
    {"target": "r30c2", "sources": ["r28c2", "r29c2"], "type": "sum"},
    {"target": "r30c3", "sources": ["r28c3", "r29c3"], "type": "sum"},
]

standalone_why = {}
for c in (1, 2, 3):
    standalone_why[(1, c)] = "Sole program activity line, equals 3010 New obligations exactly, no distinct total line"
    standalone_why[(5, c)] = "Memorandum entry, non-add"
    standalone_why[(12, c)] = "Single-source, equals 1700 Collected exactly"
    standalone_why[(31, c)] = "Employment summary figure, no relation to dollar figures in this schema"
standalone_why[(7, 1)] = "Single-source this column; no unpaid-obligations end-of-year line (3050 not printed for 2025)"
standalone_why[(8, 1)] = "Single-source this column; no unpaid-obligations end-of-year line (3050 not printed for 2025)"
standalone_why[(10, 3)] = "Memorandum entry, duplicates 3000 Unpaid obligations brought forward"
standalone_why[(11, 2)] = "Memorandum entry, duplicates 3050 Unpaid obligations end of year"
standalone_why[(11, 3)] = "Memorandum entry, duplicates 3050 Unpaid obligations end of year"
standalone_why[(13, 1)] = "Single-source this column; no discretionary-balance outlays (4011) in 2025 actual"
standalone_why[(15, 1)] = "Single-source, equals 4010 exactly; no discretionary-balance outlays (4011) this column"
standalone_why[(16, 2)] = "Single-source Federal offset; no Non-Federal (4033) offset this column"
standalone_why[(16, 3)] = "Single-source Federal offset; no Non-Federal (4033) offset this column"
standalone_why[(18, 2)] = "Single-source, equals 4030 Federal sources exactly; no Non-Federal offset this column"
standalone_why[(18, 3)] = "Single-source, equals 4030 Federal sources exactly; no Non-Federal offset this column"
standalone_why[(20, 2)] = "Single-source, equals 4080 Outlays net (discretionary) exactly"
standalone_why[(20, 3)] = "Single-source, equals 4080 Outlays net (discretionary) exactly"

target_cells = set()
source_cells = set()
for r in relations:
    t = r["target"]; target_cells.add((int(t[1:t.index("c")]), int(t[t.index("c")+1:])))
    for s in r["sources"]:
        source_cells.add((int(s[1:s.index("c")]), int(s[s.index("c")+1:])))

cells = []
for row, _ in rows:
    for col in (1, 2, 3):
        if col not in values[row]:
            continue
        key = (row, col)
        if key in standalone_why:
            role = "standalone"
        elif key in target_cells:
            role = "total"
        elif key in source_cells:
            role = "leaf"
        else:
            raise SystemExit(f"UNRESOLVED cell r{row}c{col}")
        cell = {"id": f"r{row}c{col}", "row": row, "col": col, "value": values[row][col], "role": role}
        if role == "standalone":
            cell["why"] = standalone_why[key]
        cells.append(cell)

out = {
    "table_id": "budget-appendix-fy2027-leg-loc-gift-shop",
    "source": {
        "path": "sources/omb/budget-2027-app-2-3-legislative.pdf",
        "table": "Library of Congress - Gift Shop, Decimal Classification, Photo Duplication, and Related Services",
        "page": 22,
        "title": "Library of Congress - Gift Shop, Decimal Classification, Photo Duplication, and Related Services",
        "period": "FY 2027",
    },
    "columns": [{"index": i, "label": l} for i, l in columns],
    "rows": [{"index": i, "label": l} for i, l in rows],
    "cells": cells,
    "relations": relations,
}

Path("tables/omb/budget-appendix-fy2027-leg-loc-gift-shop.cells.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
print("cells:", len(cells), "relations:", len(relations))
