import json
from pathlib import Path

rows = [
    (1, "0100 Balance, start of year"),
    (2, "0198 Reconciliation adjustment"),
    (3, "0199 Balance, start of year"),
    (4, "1130 Contributions, Library of Congress Gift Fund"),
    (5, "1130 Contributions, Library of Congress Permanent Loan Account"),
    (6, "1130 Income from Donated Securities, Library of Congress"),
    (7, "1140 Earnings on Investments, Library of Congress Gift Fund"),
    (8, "1140 Interest, Library of Congress Permanent Loan Account"),
    (9, "1140 Foreign Service National Separation Liability Trust Fund"),
    (10, "1199 Total current law receipts"),
    (11, "1999 Total receipts"),
    (12, "2000 Total: Balances and receipts"),
    (13, "2101 Gift and Trust Fund Accounts"),
    (14, "5098 Reconciliation adjustment"),
    (15, "5099 Balance, end of year"),
    (16, "0001 Office of the Librarian"),
    (17, "0002 Office of the Chief Information Officer"),
    (18, "0003 Office of the Chief Operating Officer"),
    (19, "0004 Library Collections and Services Group"),
    (20, "0900 Total new obligations, unexpired accounts"),
    (21, "1000 Unobligated balance brought forward, Oct 1"),
    (22, "1201 Appropriation (special or trust fund)"),
    (23, "1930 Total budgetary resources available"),
    (24, "1941 Unexpired unobligated balance, end of year"),
    (25, "3000 Unpaid obligations, brought forward, Oct 1"),
    (26, "3010 New obligations, unexpired accounts"),
    (27, "3020 Outlays (gross)"),
    (28, "3050 Unpaid obligations, end of year"),
    (29, "3100 Obligated balance, start of year"),
    (30, "3200 Obligated balance, end of year"),
    (31, "4090 Budget authority, gross"),
    (32, "4100 Outlays from new mandatory authority"),
    (33, "4101 Outlays from mandatory balances"),
    (34, "4110 Outlays, gross (total)"),
    (35, "4180 Budget authority, net (total)"),
    (36, "4190 Outlays, net (total)"),
    (37, "5000 Total investments, SOY: Federal securities: Par value"),
    (38, "5001 Total investments, EOY: Federal securities: Par value"),
    (39, "5010 Total investments, SOY: non-Fed securities: Market value"),
    (40, "5011 Total investments, EOY: non-Fed securities: Market value"),
    (41, "11.1 Personnel compensation: Full-time permanent"),
    (42, "12.1 Civilian personnel benefits"),
    (43, "25.1 Advisory and assistance services"),
    (44, "25.2 Other services from non-Federal sources"),
    (45, "25.3 Other goods and services from Federal sources"),
    (46, "31.0 Equipment"),
    (47, "33.0 Investments and loans"),
    (48, "41.0 Grants, subsidies, and contributions"),
    (49, "99.0 Direct obligations"),
    (50, "99.5 Adjustment for rounding"),
    (51, "99.9 Total new obligations, unexpired accounts"),
    (52, "1001 Direct civilian full-time equivalent employment"),
]

columns = [(1, "2025 actual"), (2, "2026 est."), (3, "2027 est.")]

values = {
    1: {1: "6", 2: "8", 3: "59"},
    2: {1: "2"},
    3: {1: "8", 2: "8", 3: "59"},
    4: {1: "29", 2: "52", 3: "54"},
    5: {1: "13", 2: "10", 3: "10"},
    6: {1: "9", 2: "9", 3: "10"},
    7: {1: "2", 2: "4", 3: "4"},
    8: {1: "1", 2: "1", 3: "1"},
    9: {2: "1", 3: "1"},
    10: {1: "54", 2: "77", 3: "80"},
    11: {1: "54", 2: "77", 3: "80"},
    12: {1: "62", 2: "85", 3: "139"},
    13: {1: "-55", 2: "-26", 3: "-27"},
    14: {1: "1"},
    15: {1: "8", 2: "59", 3: "112"},
    16: {1: "12", 2: "12", 3: "12"},
    17: {1: "2", 2: "2", 3: "2"},
    18: {1: "2", 2: "2", 3: "2"},
    19: {1: "35", 2: "15", 3: "15"},
    20: {1: "51", 2: "31", 3: "31"},
    21: {1: "66", 2: "70", 3: "65"},
    22: {1: "55", 2: "26", 3: "27"},
    23: {1: "121", 2: "96", 3: "92"},
    24: {1: "70", 2: "65", 3: "61"},
    25: {1: "13", 2: "12", 3: "15"},
    26: {1: "51", 2: "31", 3: "31"},
    27: {1: "-52", 2: "-28", 3: "-27"},
    28: {1: "12", 2: "15", 3: "19"},
    29: {1: "13", 2: "12", 3: "15"},
    30: {1: "12", 2: "15", 3: "19"},
    31: {1: "55", 2: "26", 3: "27"},
    32: {1: "47", 2: "21", 3: "21"},
    33: {1: "5", 2: "7", 3: "6"},
    34: {1: "52", 2: "28", 3: "27"},
    35: {1: "55", 2: "26", 3: "27"},
    36: {1: "52", 2: "28", 3: "27"},
    37: {1: "66", 2: "69", 3: "69"},
    38: {1: "69", 2: "69", 3: "69"},
    39: {1: "200", 2: "220"},
    40: {1: "220"},
    41: {1: "3", 2: "2", 3: "2"},
    42: {1: "1", 2: "1", 3: "1"},
    43: {1: "2", 2: "2", 3: "2"},
    44: {1: "5", 2: "3", 3: "3"},
    45: {1: "5", 2: "8", 3: "8"},
    46: {1: "20", 2: "1", 3: "1"},
    47: {1: "13", 2: "8", 3: "8"},
    48: {1: "2", 2: "5", 3: "5"},
    49: {1: "51", 2: "30", 3: "30"},
    50: {2: "1", 3: "1"},
    51: {1: "51", 2: "31", 3: "31"},
    52: {1: "36", 2: "21", 3: "21"},
}

relations = [
    {"target": "r3c1", "sources": ["r1c1", "r2c1"], "type": "sum"},
    {"target": "r10c1", "sources": ["r4c1", "r5c1", "r6c1", "r7c1", "r8c1"], "type": "sum"},
    {"target": "r10c2", "sources": ["r4c2", "r5c2", "r6c2", "r7c2", "r8c2", "r9c2"], "type": "sum"},
    {"target": "r10c3", "sources": ["r4c3", "r5c3", "r6c3", "r7c3", "r8c3", "r9c3"], "type": "sum"},
    {"target": "r12c1", "sources": ["r3c1", "r11c1"], "type": "sum"},
    {"target": "r12c2", "sources": ["r3c2", "r11c2"], "type": "sum"},
    {"target": "r12c3", "sources": ["r3c3", "r11c3"], "type": "sum"},
    {"target": "r15c1", "sources": ["r12c1", "r13c1", "r14c1"], "type": "sum"},
    {"target": "r15c2", "sources": ["r12c2", "r13c2"], "type": "sum"},
    {"target": "r15c3", "sources": ["r12c3", "r13c3"], "type": "sum"},
    {"target": "r20c1", "sources": ["r16c1", "r17c1", "r18c1", "r19c1"], "type": "sum"},
    {"target": "r20c2", "sources": ["r16c2", "r17c2", "r18c2", "r19c2"], "type": "sum"},
    {"target": "r20c3", "sources": ["r16c3", "r17c3", "r18c3", "r19c3"], "type": "sum"},
    {"target": "r23c1", "sources": ["r21c1", "r22c1"], "type": "sum"},
    {"target": "r23c2", "sources": ["r21c2", "r22c2"], "type": "sum"},
    {"target": "r23c3", "sources": ["r21c3", "r22c3"], "type": "sum"},
    {"target": "r28c1", "sources": ["r25c1", "r26c1", "r27c1"], "type": "sum"},
    {"target": "r28c2", "sources": ["r25c2", "r26c2", "r27c2"], "type": "sum"},
    {"target": "r28c3", "sources": ["r25c3", "r26c3", "r27c3"], "type": "sum"},
    {"target": "r34c1", "sources": ["r32c1", "r33c1"], "type": "sum"},
    {"target": "r34c2", "sources": ["r32c2", "r33c2"], "type": "sum"},
    {"target": "r34c3", "sources": ["r32c3", "r33c3"], "type": "sum"},
    {"target": "r49c1", "sources": ["r41c1", "r42c1", "r43c1", "r44c1", "r45c1", "r46c1", "r47c1", "r48c1"], "type": "sum"},
    {"target": "r49c2", "sources": ["r41c2", "r42c2", "r43c2", "r44c2", "r45c2", "r46c2", "r47c2", "r48c2"], "type": "sum"},
    {"target": "r49c3", "sources": ["r41c3", "r42c3", "r43c3", "r44c3", "r45c3", "r46c3", "r47c3", "r48c3"], "type": "sum"},
    {"target": "r51c2", "sources": ["r49c2", "r50c2"], "type": "sum"},
    {"target": "r51c3", "sources": ["r49c3", "r50c3"], "type": "sum"},
]

standalone_why = {}
for c in (1, 2, 3):
    standalone_why[(11, c)] = "Single-source, equals 1199 Total current law receipts exactly, no other-law receipts"
    standalone_why[(24, c)] = "Memorandum, non-add"
    standalone_why[(29, c)] = "Memorandum entry, duplicates 3000 Unpaid obligations brought forward"
    standalone_why[(30, c)] = "Memorandum entry, duplicates 3050 Unpaid obligations end of year"
    standalone_why[(31, c)] = "Single-source, equals 1201 Appropriation exactly"
    standalone_why[(35, c)] = "Single-source, equals 4090 Budget authority gross exactly, no offsets"
    standalone_why[(36, c)] = "Single-source, equals 4110 Outlays gross total exactly, no offsets"
    standalone_why[(37, c)] = "Memorandum investment balance, informational only, no relation to obligations figures"
    standalone_why[(38, c)] = "Memorandum investment balance, informational only, no relation to obligations figures"
    standalone_why[(52, c)] = "Employment summary figure, no relation to dollar figures in this schema"
standalone_why[(1, 2)] = "Single-source this column; no reconciliation adjustment (0198) this period, equals 0199 exactly"
standalone_why[(1, 3)] = "Single-source this column; no reconciliation adjustment (0198) this period, equals 0199 exactly"
standalone_why[(3, 2)] = "Single-source this column; no reconciliation adjustment (0198) this period, equals 0100 exactly"
standalone_why[(3, 3)] = "Single-source this column; no reconciliation adjustment (0198) this period, equals 0100 exactly"
standalone_why[(39, 1)] = "Memorandum investment balance, informational only, no relation to obligations figures"
standalone_why[(39, 2)] = "Memorandum investment balance, informational only, no relation to obligations figures"
standalone_why[(40, 1)] = "Memorandum investment balance, informational only, no relation to obligations figures"
standalone_why[(51, 1)] = "Single-source, equals 99.0 Direct obligations exactly, no rounding adjustment this column"

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
    "table_id": "budget-appendix-fy2027-leg-loc-gift-trust",
    "source": {
        "path": "sources/omb/budget-2027-app-2-3-legislative.pdf",
        "table": "Library of Congress - Gift and Trust Fund Accounts",
        "page": 23,
        "title": "Library of Congress - Gift and Trust Fund Accounts",
        "period": "FY 2027",
    },
    "columns": [{"index": i, "label": l} for i, l in columns],
    "rows": [{"index": i, "label": l} for i, l in rows],
    "cells": cells,
    "relations": relations,
}

Path("tables/omb/budget-appendix-fy2027-leg-loc-gift-trust.cells.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
print("cells:", len(cells), "relations:", len(relations))
