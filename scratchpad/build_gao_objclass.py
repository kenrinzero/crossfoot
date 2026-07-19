# Build omb/budget-appendix-fy2027-leg-gao-salaries-objclass.cells.json
# GAO Salaries and Expenses (005-0107-0-1-801), Object Classification +
# Employment Summary. Source: sources/omb/budget-2027-app-2-3-legislative.pdf,
# PDF p29 (printed 41) LEFT column (right column is US Tax Court 023-0100).
# Values read from the staged render gao-p29-render.png, cross-checked
# against the text layer gao-p29-text.txt.
import json
from decimal import Decimal

ROWS = [
    ("11.1 Full-time permanent", ["479", "458", "482"]),
    ("11.3 Other than full-time permanent", ["19", "18", "17"]),
    ("11.5 Other personnel compensation", ["9", "9", "11"]),
    ("11.9 Total personnel compensation", ["507", "485", "510"]),
    ("12.1 Civilian personnel benefits", ["187", "178", "188"]),
    ("13.0 Benefits for former personnel", ["4", "4", "5"]),
    ("21.0 Travel and transportation of persons", ["5", "5", "5"]),
    ("23.1 Rental payments to GSA", ["6", "6", "5"]),
    ("23.3 Communications, utilities, and miscellaneous charges", ["12", "13", "14"]),
    ("25.1 Advisory and assistance services", ["5", "6", "7"]),
    ("25.2 Other services from non-Federal sources", ["16", "22", "22"]),
    ("25.3 Other goods and services from Federal sources", ["2", "2", "8"]),
    ("25.4 Operation and maintenance of facilities", ["1", "5", "10"]),
    ("25.6 Medical care", ["1", "1", "1"]),
    ("25.7 Operation and maintenance of equipment", ["68", "70", "71"]),
    ("31.0 Equipment", ["8", "8", "7"]),
    ("32.0 Land and structures", ["3", "7", "7"]),
    ("99.0 Direct obligations", ["825", "812", "860"]),
    ("99.0 Reimbursable obligations", ["101", "91", "50"]),
    ("99.9 Total new obligations, unexpired accounts", ["926", "903", "910"]),
    ("1001 Direct civilian full-time equivalent employment", ["3223", "3000", "3034"]),
    ("2001 Reimbursable civilian full-time equivalent employment", ["324", "353", "176"]),
]

# row index by position (two rows share the "99.0" prefix, so index by list order)
R_119 = 4       # 11.9 total personnel compensation
R_990_DIRECT = 18
R_990_REIMB = 19
R_999 = 20
FTE_ROWS = (21, 22)
PARTS_119 = (1, 2, 3)                       # 11.1 + 11.3 + 11.5
PARTS_990 = (4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)  # 11.9 + line items

FTE_WHY = ("Employment Summary line (full-time equivalent employment, a headcount, "
           "not USD millions); participates in no arithmetic on this schedule")

def cid(row, col):
    return f"r{row}c{col}"

VALUES = {}
for i, (label, vals) in enumerate(ROWS, 1):
    for col, v in enumerate(vals, 1):
        VALUES[(i, col)] = v

RELATIONS = []
for col in (1, 2, 3):
    RELATIONS.append((R_119, PARTS_119, col))
    RELATIONS.append((R_990_DIRECT, PARTS_990, col))
    RELATIONS.append((R_999, (R_990_DIRECT, R_990_REIMB), col))

targets = set()
sources = set()
for tgt, srcs, col in RELATIONS:
    total = sum(Decimal(VALUES[(s, col)]) for s in srcs)
    assert total == Decimal(VALUES[(tgt, col)]), \
        f"row {tgt} c{col}: sum {total} != printed {VALUES[(tgt, col)]}"
    targets.add((tgt, col))
    sources.update((s, col) for s in srcs)

cells = []
n_standalone = 0
for i, (label, vals) in enumerate(ROWS, 1):
    for col, v in enumerate(vals, 1):
        if (i, col) in targets:
            cells.append({"id": cid(i, col), "row": i, "col": col, "value": v, "role": "total"})
        elif i in FTE_ROWS:
            cells.append({"id": cid(i, col), "row": i, "col": col, "value": v,
                          "role": "standalone", "why": FTE_WHY})
            n_standalone += 1
        else:
            assert (i, col) in sources, f"row {i} c{col} uncovered"
            cells.append({"id": cid(i, col), "row": i, "col": col, "value": v, "role": "leaf"})

assert len(cells) == 66, f"cell count {len(cells)} != 66"

relations = [{"type": "sum",
              "sources": [cid(s, col) for s in srcs],
              "target": cid(tgt, col)}
             for tgt, srcs, col in RELATIONS]
assert len(relations) == 9, f"relation count {len(relations)} != 9"

doc = {
    "table_id": "omb/budget-appendix-fy2027-leg-gao-salaries-objclass",
    "source": {
        "path": "sources/omb/budget-2027-app-2-3-legislative.pdf",
        "table": "005-0107-0-1-801",
        "page": 29,
        "title": "Government Accountability Office - Salaries and Expenses (Object Classification + Employment Summary)",
        "period": "FY 2027"
    },
    "unit_note": "USD millions except the Employment Summary FTE lines (headcounts). GAO Salaries and Expenses account (id 005-0107-0-1-801), Object Classification and Employment Summary schedules, PDF page 29 (printed page 41) LEFT column - the right column of this two-column page is the separate US Tax Court account 023-0100 (do not cross-contaminate). Unit 2 of the 2-unit by-schedule split of this 195-cell account (sibling: -gao-salaries-pf); each schedule prints its own 005-0107 header, so no cross-unit re-anchoring is needed. 99.0 Direct obligations sums 11.9 Total personnel compensation plus the non-personnel line items (11.1/11.3/11.5 fold in via 11.9, not double-counted). Two rows share the printed code 99.0 (Direct vs Reimbursable) and are distinct rows here. No blank cells in these schedules. Cross-schedule sanity (not encoded; sibling unit re-reads independently): 99.9 = 0900 (926/903/910), 99.0 Direct = 0799 (825/812/860), 99.0 Reimbursable = 0899 (101/91/50).",
    "columns": [
        {"index": 1, "label": "2025 actual"},
        {"index": 2, "label": "2026 est."},
        {"index": 3, "label": "2027 est."}
    ],
    "rows": [{"index": i, "label": label} for i, (label, _) in enumerate(ROWS, 1)],
    "cells": cells,
    "relations": relations
}

out = "tables/omb/budget-appendix-fy2027-leg-gao-salaries-objclass.cells.json"
with open(out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"wrote {out}: {len(cells)} cells, {len(relations)} relations, {n_standalone} standalone")
