import json
from pathlib import Path

rows = [
    (1, "0801 Fedlink and Federal Research"),
    (2, "1000 Unobligated balance brought forward, Oct 1"),
    (3, "1021 Recoveries of prior year unpaid obligations"),
    (4, "1033 Recoveries of prior year paid obligations"),
    (5, "1070 Unobligated balance (total)"),
    (6, "1700 Collected"),
    (7, "1701 Change in uncollected payments, Federal sources"),
    (8, "1750 Spending authority from offsetting collections, discretionary (total)"),
    (9, "1930 Total budgetary resources available"),
    (10, "1941 Unexpired unobligated balance, end of year"),
    (11, "3000 Unpaid obligations, brought forward, Oct 1"),
    (12, "3010 New obligations, unexpired accounts"),
    (13, "3020 Outlays (gross)"),
    (14, "3040 Recoveries of prior year unpaid obligations, unexpired"),
    (15, "3050 Unpaid obligations, end of year"),
    (16, "3060 Uncollected pymts, Fed sources, brought forward, Oct 1"),
    (17, "3070 Change in uncollected pymts, Fed sources, unexpired"),
    (18, "3090 Uncollected pymts, Fed sources, end of year"),
    (19, "3100 Obligated balance, start of year"),
    (20, "3200 Obligated balance, end of year"),
    (21, "4000 Budget authority, gross"),
    (22, "4010 Outlays from new discretionary authority"),
    (23, "4011 Outlays from discretionary balances"),
    (24, "4020 Outlays, gross (total)"),
    (25, "4030 Federal sources"),
    (26, "4033 Non-Federal sources"),
    (27, "4040 Offsets against gross budget authority and outlays (total)"),
    (28, "4050 Change in uncollected pymts, Fed sources, unexpired"),
    (29, "4053 Recoveries of prior year paid obligations, unexpired accounts"),
    (30, "4060 Additional offsets against budget authority only (total)"),
    (31, "4080 Outlays, net (discretionary)"),
    (32, "4190 Outlays, net (total)"),
    (33, "11.1 Personnel compensation: Full-time permanent"),
    (34, "12.1 Civilian personnel benefits"),
    (35, "25.1 Advisory and assistance services"),
    (36, "25.2 Other services from non-Federal sources"),
    (37, "25.3 Other goods and services from Federal sources"),
    (38, "31.0 Equipment"),
    (39, "44.0 Refunds"),
    (40, "99.0 Reimbursable obligations"),
    (41, "99.5 Adjustment for rounding"),
    (42, "99.9 Total new obligations, unexpired accounts"),
    (43, "2001 Reimbursable civilian full-time equivalent employment"),
]

columns = [(1, "2025 actual"), (2, "2026 est."), (3, "2027 est.")]

values = {
    1: {1: "100", 2: "308", 3: "308"},
    2: {1: "52", 2: "43", 3: "43"},
    3: {1: "2"},
    4: {1: "2"},
    5: {1: "56", 2: "43", 3: "43"},
    6: {1: "88", 2: "308", 3: "308"},
    7: {1: "-1"},
    8: {1: "87", 2: "308", 3: "308"},
    9: {1: "143", 2: "351", 3: "351"},
    10: {1: "43", 2: "43", 3: "43"},
    11: {1: "30", 2: "29", 3: "80"},
    12: {1: "100", 2: "308", 3: "308"},
    13: {1: "-99", 2: "-257", 3: "-305"},
    14: {1: "-2"},
    15: {1: "29", 2: "80", 3: "83"},
    16: {1: "-2", 2: "-1", 3: "-1"},
    17: {1: "1"},
    18: {1: "-1", 2: "-1", 3: "-1"},
    19: {1: "28", 2: "28", 3: "79"},
    20: {1: "28", 2: "79", 3: "82"},
    21: {1: "87", 2: "308", 3: "308"},
    22: {1: "54", 2: "194", 3: "194"},
    23: {1: "45", 2: "63", 3: "111"},
    24: {1: "99", 2: "257", 3: "305"},
    25: {1: "-88", 2: "-308", 3: "-308"},
    26: {1: "-2"},
    27: {1: "-90", 2: "-308", 3: "-308"},
    28: {1: "1"},
    29: {1: "2"},
    30: {1: "3"},
    31: {1: "9", 2: "-51", 3: "-3"},
    32: {1: "9", 2: "-51", 3: "-3"},
    33: {1: "8", 2: "8", 3: "8"},
    34: {1: "3", 2: "3", 3: "3"},
    35: {2: "1", 3: "1"},
    36: {1: "59", 2: "250", 3: "250"},
    37: {1: "2", 2: "3", 3: "3"},
    38: {1: "24", 2: "42", 3: "42"},
    39: {1: "4"},
    40: {1: "100", 2: "307", 3: "307"},
    41: {2: "1", 3: "1"},
    42: {1: "100", 2: "308", 3: "308"},
    43: {1: "86", 2: "99", 3: "99"},
}

relations = [
    {"target": "r5c1", "sources": ["r2c1", "r3c1", "r4c1"], "type": "sum"},
    {"target": "r8c1", "sources": ["r6c1", "r7c1"], "type": "sum"},
    {"target": "r9c1", "sources": ["r5c1", "r8c1"], "type": "sum"},
    {"target": "r9c2", "sources": ["r5c2", "r8c2"], "type": "sum"},
    {"target": "r9c3", "sources": ["r5c3", "r8c3"], "type": "sum"},
    {"target": "r15c1", "sources": ["r11c1", "r12c1", "r13c1", "r14c1"], "type": "sum"},
    {"target": "r15c2", "sources": ["r11c2", "r12c2", "r13c2"], "type": "sum"},
    {"target": "r15c3", "sources": ["r11c3", "r12c3", "r13c3"], "type": "sum"},
    {"target": "r18c1", "sources": ["r16c1", "r17c1"], "type": "sum"},
    {"target": "r19c1", "sources": ["r11c1", "r16c1"], "type": "sum"},
    {"target": "r19c2", "sources": ["r11c2", "r16c2"], "type": "sum"},
    {"target": "r19c3", "sources": ["r11c3", "r16c3"], "type": "sum"},
    {"target": "r20c1", "sources": ["r15c1", "r18c1"], "type": "sum"},
    {"target": "r20c2", "sources": ["r15c2", "r18c2"], "type": "sum"},
    {"target": "r20c3", "sources": ["r15c3", "r18c3"], "type": "sum"},
    {"target": "r24c1", "sources": ["r22c1", "r23c1"], "type": "sum"},
    {"target": "r24c2", "sources": ["r22c2", "r23c2"], "type": "sum"},
    {"target": "r24c3", "sources": ["r22c3", "r23c3"], "type": "sum"},
    {"target": "r27c1", "sources": ["r25c1", "r26c1"], "type": "sum"},
    {"target": "r30c1", "sources": ["r28c1", "r29c1"], "type": "sum"},
    {"target": "r31c1", "sources": ["r24c1", "r27c1"], "type": "sum"},
    {"target": "r31c2", "sources": ["r24c2", "r27c2"], "type": "sum"},
    {"target": "r31c3", "sources": ["r24c3", "r27c3"], "type": "sum"},
    {"target": "r40c1", "sources": ["r33c1", "r34c1", "r36c1", "r37c1", "r38c1", "r39c1"], "type": "sum"},
    {"target": "r40c2", "sources": ["r33c2", "r34c2", "r35c2", "r36c2", "r37c2", "r38c2"], "type": "sum"},
    {"target": "r40c3", "sources": ["r33c3", "r34c3", "r35c3", "r36c3", "r37c3", "r38c3"], "type": "sum"},
    {"target": "r42c2", "sources": ["r40c2", "r41c2"], "type": "sum"},
    {"target": "r42c3", "sources": ["r40c3", "r41c3"], "type": "sum"},
]

standalone_why = {}
for c in (1, 2, 3):
    standalone_why[(1, c)] = "Sole program activity line, equals 3010 New obligations exactly, no distinct total line"
    standalone_why[(10, c)] = "Memorandum, non-add"
    standalone_why[(21, c)] = "Single-source, equals 1750 Spending authority from offsetting collections exactly"
    standalone_why[(43, c)] = "Employment summary figure, no relation to dollar figures in this schema"
standalone_why[(2, 2)] = "Single-source this column; no recoveries (1021/1033) this period, equals 1070 exactly"
standalone_why[(2, 3)] = "Single-source this column; no recoveries (1021/1033) this period, equals 1070 exactly"
standalone_why[(6, 2)] = "Single-source this column; no change-in-uncollected-payments (1701) this period, equals 1750 exactly"
standalone_why[(6, 3)] = "Single-source this column; no change-in-uncollected-payments (1701) this period, equals 1750 exactly"
standalone_why[(25, 2)] = "Single-source Federal offset; no Non-Federal (4033) offset this period, equals 4040 exactly"
standalone_why[(25, 3)] = "Single-source Federal offset; no Non-Federal (4033) offset this period, equals 4040 exactly"
standalone_why[(32, 1)] = "Single-source, equals 4080 Outlays net (discretionary) exactly"
standalone_why[(32, 2)] = "Single-source, equals 4080 Outlays net (discretionary) exactly"
standalone_why[(32, 3)] = "Single-source, equals 4080 Outlays net (discretionary) exactly"
standalone_why[(42, 1)] = "Single-source, equals 99.0 Reimbursable obligations exactly, no rounding adjustment this column"

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
    "table_id": "budget-appendix-fy2027-leg-loc-fedlink",
    "source": {
        "path": "sources/omb/budget-2027-app-2-3-legislative.pdf",
        "table": "Library of Congress - FEDLINK Program and Federal Research Program",
        "page": 22,
        "title": "Library of Congress - FEDLINK Program and Federal Research Program",
        "period": "FY 2027",
    },
    "columns": [{"index": i, "label": l} for i, l in columns],
    "rows": [{"index": i, "label": l} for i, l in rows],
    "cells": cells,
    "relations": relations,
}

Path("tables/omb/budget-appendix-fy2027-leg-loc-fedlink.cells.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
print("cells:", len(cells), "relations:", len(relations))
