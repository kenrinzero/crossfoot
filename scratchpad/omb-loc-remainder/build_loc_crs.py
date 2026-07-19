import json
from pathlib import Path

rows = [
    (1, "0001 Congressional Research Service, Salaries and Expenses (Direct)"),
    (2, "1100 Appropriation"),
    (3, "1930 Total budgetary resources available"),
    (4, "3000 Unpaid obligations, brought forward, Oct 1"),
    (5, "3010 New obligations, unexpired accounts"),
    (6, "3020 Outlays (gross)"),
    (7, "3050 Unpaid obligations, end of year"),
    (8, "3100 Obligated balance, start of year"),
    (9, "3200 Obligated balance, end of year"),
    (10, "4000 Budget authority, gross"),
    (11, "4010 Outlays from new discretionary authority"),
    (12, "4011 Outlays from discretionary balances"),
    (13, "4020 Outlays, gross (total)"),
    (14, "4180 Budget authority, net (total)"),
    (15, "4190 Outlays, net (total)"),
    (16, "11.1 Full-time permanent"),
    (17, "11.3 Other than full-time permanent"),
    (18, "11.5 Other personnel compensation"),
    (19, "11.9 Total personnel compensation"),
    (20, "12.1 Civilian personnel benefits"),
    (21, "23.3 Communications, utilities, and miscellaneous charges"),
    (22, "25.1 Advisory and assistance services"),
    (23, "25.2 Other services from non-Federal sources"),
    (24, "26.0 Supplies and materials"),
    (25, "31.0 Equipment"),
    (26, "99.0 Direct obligations"),
    (27, "99.5 Adjustment for rounding"),
    (28, "99.9 Total new obligations, unexpired accounts"),
    (29, "1001 Direct civilian full-time equivalent employment"),
]

columns = [(1, "2025 actual"), (2, "2026 est."), (3, "2027 est.")]

# row -> {col: value}; missing col = omitted (blank in source, not zero)
values = {
    1: {1: "136", 2: "136", 3: "140"},
    2: {1: "136", 2: "136", 3: "140"},
    3: {1: "136", 2: "136", 3: "140"},
    4: {1: "15", 2: "9", 3: "10"},
    5: {1: "136", 2: "136", 3: "140"},
    6: {1: "-142", 2: "-135", 3: "-139"},
    7: {1: "9", 2: "10", 3: "11"},
    8: {1: "15", 2: "9", 3: "10"},
    9: {1: "9", 2: "10", 3: "11"},
    10: {1: "136", 2: "136", 3: "140"},
    11: {1: "128", 2: "125", 3: "129"},
    12: {1: "14", 2: "10", 3: "10"},
    13: {1: "142", 2: "135", 3: "139"},
    14: {1: "136", 2: "136", 3: "140"},
    15: {1: "142", 2: "135", 3: "139"},
    16: {1: "91", 2: "88", 3: "94"},
    17: {1: "1", 2: "1", 3: "1"},
    18: {1: "1", 2: "1", 3: "1"},
    19: {1: "93", 2: "90", 3: "96"},
    20: {1: "33", 2: "31", 3: "34"},
    21: {1: "1", 2: "1", 3: "1"},
    22: {1: "2", 2: "3", 3: "2"},
    23: {1: "2", 2: "3", 3: "2"},
    24: {1: "5", 2: "6", 3: "5"},
    25: {2: "1"},  # 31.0 Equipment -- 2025/2027 blank in source
    26: {1: "136", 2: "135", 3: "140"},
    27: {2: "1"},  # 99.5 Adjustment for rounding -- 2025/2027 blank in source
    28: {1: "136", 2: "136", 3: "140"},
    29: {1: "609", 2: "641", 3: "646"},
}

# role + why per (row, col); default role is "leaf" if used as a relation source,
# "total" if a relation target, else must be "standalone" with a why.
standalone_why = {
    (1, 1): "Sole program activity line, no 0900 total row printed, not summed elsewhere",
    (1, 2): "Sole program activity line, no 0900 total row printed, not summed elsewhere",
    (1, 3): "Sole program activity line, no 0900 total row printed, not summed elsewhere",
    (2, 1): "Sole appropriation line; no unobligated balance or recoveries lines to sum with",
    (2, 2): "Sole appropriation line; no unobligated balance or recoveries lines to sum with",
    (2, 3): "Sole appropriation line; no unobligated balance or recoveries lines to sum with",
    (3, 1): "Single-source budgetary resources identity (equals 1100 Appropriation exactly)",
    (3, 2): "Single-source budgetary resources identity (equals 1100 Appropriation exactly)",
    (3, 3): "Single-source budgetary resources identity (equals 1100 Appropriation exactly)",
    (8, 1): "Memorandum entry, duplicates 3000 Unpaid obligations brought forward",
    (8, 2): "Memorandum entry, duplicates 3000 Unpaid obligations brought forward",
    (8, 3): "Memorandum entry, duplicates 3000 Unpaid obligations brought forward",
    (9, 1): "Memorandum entry, duplicates 3050 Unpaid obligations end of year",
    (9, 2): "Memorandum entry, duplicates 3050 Unpaid obligations end of year",
    (9, 3): "Memorandum entry, duplicates 3050 Unpaid obligations end of year",
    (10, 1): "Single-source budget authority figure; no offsetting collections lines present",
    (10, 2): "Single-source budget authority figure; no offsetting collections lines present",
    (10, 3): "Single-source budget authority figure; no offsetting collections lines present",
    (14, 1): "Single-source identity (equals 4000 Budget authority gross exactly, no offsets)",
    (14, 2): "Single-source identity (equals 4000 Budget authority gross exactly, no offsets)",
    (14, 3): "Single-source identity (equals 4000 Budget authority gross exactly, no offsets)",
    (15, 1): "Single-source identity (equals 4020 Outlays gross total exactly, no offsets)",
    (15, 2): "Single-source identity (equals 4020 Outlays gross total exactly, no offsets)",
    (15, 3): "Single-source identity (equals 4020 Outlays gross total exactly, no offsets)",
    (28, 1): "Single-source (equals 99.0 Direct obligations exactly, no rounding adjustment this column)",
    (28, 3): "Single-source (equals 99.0 Direct obligations exactly, no rounding adjustment this column)",
    (29, 1): "Employment summary figure, no relation to dollar figures in this schema",
    (29, 2): "Employment summary figure, no relation to dollar figures in this schema",
    (29, 3): "Employment summary figure, no relation to dollar figures in this schema",
}

relations = []
for c in (1, 2, 3):
    relations.append({"target": f"r7c{c}", "sources": [f"r4c{c}", f"r5c{c}", f"r6c{c}"], "type": "sum"})
    relations.append({"target": f"r13c{c}", "sources": [f"r11c{c}", f"r12c{c}"], "type": "sum"})
    relations.append({"target": f"r19c{c}", "sources": [f"r16c{c}", f"r17c{c}", f"r18c{c}"], "type": "sum"})
    obj_sources = [f"r19c{c}", f"r20c{c}", f"r21c{c}", f"r22c{c}", f"r23c{c}", f"r24c{c}"]
    if c == 2:
        obj_sources.append("r25c2")
    relations.append({"target": f"r26c{c}", "sources": obj_sources, "type": "sum"})
relations.append({"target": "r28c2", "sources": ["r26c2", "r27c2"], "type": "sum"})

target_cells = {(int(r["target"][1:r["target"].index("c")]), int(r["target"][r["target"].index("c")+1:])) for r in relations}
source_cells = set()
for r in relations:
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
            raise SystemExit(f"UNRESOLVED cell r{row}c{col} -- not standalone/target/source")
        cell = {"id": f"r{row}c{col}", "row": row, "col": col, "value": values[row][col], "role": role}
        if role == "standalone":
            cell["why"] = standalone_why[key]
        cells.append(cell)

out = {
    "table_id": "budget-appendix-fy2027-leg-loc-crs",
    "source": {
        "path": "sources/omb/budget-2027-app-2-3-legislative.pdf",
        "table": "Library of Congress - Congressional Research Service, Salaries and Expenses",
        "page": 20,
        "title": "Library of Congress - Congressional Research Service",
        "period": "FY 2027",
    },
    "columns": [{"index": i, "label": l} for i, l in columns],
    "rows": [{"index": i, "label": l} for i, l in rows],
    "cells": cells,
    "relations": relations,
}

Path("tables/omb/budget-appendix-fy2027-leg-loc-crs.cells.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
print("cells:", len(cells), "relations:", len(relations))
