import json
from pathlib import Path

rows = [
    (1, "0801 Cooperative Acquisitions Program"),
    (2, "1000 Unobligated balance brought forward, Oct 1"),
    (3, "1700 Collected"),
    (4, "1930 Total budgetary resources available"),
    (5, "1941 Unexpired unobligated balance, end of year"),
    (6, "3010 New obligations, unexpired accounts"),
    (7, "3020 Outlays (gross)"),
    (8, "4000 Budget authority, gross"),
    (9, "4010 Outlays from new discretionary authority"),
    (10, "4011 Outlays from discretionary balances"),
    (11, "4020 Outlays, gross (total)"),
    (12, "4033 Non-Federal sources"),
    (13, "4040 Offsets against gross budget authority and outlays (total)"),
    (14, "11.1 Personnel compensation: Full-time permanent"),
    (15, "22.0 Transportation of things"),
    (16, "23.3 Communications, utilities, and miscellaneous charges"),
    (17, "25.3 Other goods and services from Federal sources"),
    (18, "31.0 Equipment"),
    (19, "99.0 Reimbursable obligations"),
    (20, "99.5 Adjustment for rounding"),
    (21, "99.9 Total new obligations, unexpired accounts"),
    (22, "2001 Reimbursable civilian full-time equivalent employment"),
]

columns = [(1, "2025 actual"), (2, "2026 est."), (3, "2027 est.")]

values = {
    1: {1: "3", 2: "13", 3: "13"},
    2: {1: "7", 2: "7", 3: "7"},
    3: {1: "3", 2: "13", 3: "13"},
    4: {1: "10", 2: "20", 3: "20"},
    5: {1: "7", 2: "7", 3: "7"},
    6: {1: "3", 2: "13", 3: "13"},
    7: {1: "-3", 2: "-13", 3: "-13"},
    8: {1: "3", 2: "13", 3: "13"},
    9: {1: "3", 2: "12", 3: "12"},
    10: {2: "1", 3: "1"},
    11: {1: "3", 2: "13", 3: "13"},
    12: {1: "-3", 2: "-13", 3: "-13"},
    13: {1: "-3", 2: "-13", 3: "-13"},
    14: {2: "1", 3: "1"},
    15: {1: "1", 2: "1", 3: "1"},
    16: {2: "1", 3: "1"},
    17: {2: "1", 3: "1"},
    18: {1: "1", 2: "7", 3: "7"},
    19: {1: "2", 2: "11", 3: "11"},
    20: {1: "1", 2: "2", 3: "2"},
    21: {1: "3", 2: "13", 3: "13"},
    22: {1: "6", 2: "6", 3: "6"},
}

standalone_why = {}
for c in (1, 2, 3):
    standalone_why[(1, c)] = "Sole program activity line, equals 3010 New obligations exactly, no distinct total line"
    standalone_why[(5, c)] = "Memorandum entry, non-add"
    standalone_why[(6, c)] = "Single-source, equals 0801 exactly; no unpaid-obligations carryover printed (3050 omitted)"
    standalone_why[(7, c)] = "Single-source outlay figure; no unpaid-obligations roll-forward printed for this account (3050 omitted)"
    standalone_why[(8, c)] = "Single-source, equals 1700 Collected exactly"
    standalone_why[(12, c)] = "Single-source Non-Federal offset; no Federal-source (4030) offset line for this account"
    standalone_why[(13, c)] = "Single-source, equals 4033 Non-Federal sources exactly"
    standalone_why[(22, c)] = "Employment summary figure, no relation to dollar figures in this schema"
standalone_why[(9, 1)] = "Single-source this column; no discretionary-balance outlays (4011) in 2025 actual"

relations = []
for c in (1, 2, 3):
    relations.append({"target": f"r4c{c}", "sources": [f"r2c{c}", f"r3c{c}"], "type": "sum"})
    relations.append({"target": f"r21c{c}", "sources": [f"r19c{c}", f"r20c{c}"], "type": "sum"})
    obj_sources = [rid for rid, col in ((15, c), (18, c)) if col in values[rid]]
    for rid in (14, 16, 17):
        if c in values[rid]:
            obj_sources.append((rid, c))
    # build properly ordered source list from whichever rows have this column populated
    src = []
    for rid in (14, 15, 16, 17, 18):
        if c in values[rid]:
            src.append(f"r{rid}c{c}")
    relations.append({"target": f"r19c{c}", "sources": src, "type": "sum"})
for c in (2, 3):
    relations.append({"target": f"r11c{c}", "sources": [f"r9c{c}", f"r10c{c}"], "type": "sum"})
standalone_why[(11, 1)] = "Single-source this column; no discretionary-balance outlays (4011) in 2025 actual"

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
    "table_id": "budget-appendix-fy2027-leg-loc-cooperative-acquisitions",
    "source": {
        "path": "sources/omb/budget-2027-app-2-3-legislative.pdf",
        "table": "Library of Congress - Cooperative Acquisitions Program Revolving Fund",
        "page": 21,
        "title": "Library of Congress - Cooperative Acquisitions Program Revolving Fund",
        "period": "FY 2027",
    },
    "columns": [{"index": i, "label": l} for i, l in columns],
    "rows": [{"index": i, "label": l} for i, l in rows],
    "cells": cells,
    "relations": relations,
}

Path("tables/omb/budget-appendix-fy2027-leg-loc-cooperative-acquisitions.cells.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
print("cells:", len(cells), "relations:", len(relations))
