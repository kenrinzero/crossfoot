# Build Boards and Commissions units #101-104 from OMB FY2027 Legislative
# Branch chapter, PDF pp30-33 (printed 42-45). Values read from renders
# boards-p30..p33-render.png, cross-checked against text extracts.
# Run with: csce | macpac | uscc | uscirf
import json, sys
from decimal import Decimal

M2 = "; schema minItems 2 forbids single-source sum"
MEMO = "Memorandum (non-add) entry: does not feed the section arithmetic"
FTE = ("Employment Summary line (full-time equivalent employment, a headcount, "
       "not USD millions); participates in no arithmetic on this schedule")
ZSUP = ("feeds a target that prints blank (nets to zero, zero-suppressed) in this "
        "column, so no encodable relation exists")

def build(table_id, source, unit_note, rows, relations, standalone, expect):
    # A row label may carry an explicit unique key as "key|printed label"
    # (needed when two rows share a printed code, e.g. USCIRF's 1001 memo
    # row vs the 1001 Employment FTE row).
    code_row, values = {}, {}
    rows = [((label.split("|", 1)[0] if "|" in label else label.split()[0]),
             (label.split("|", 1)[1] if "|" in label else label), vals)
            for label, vals in rows]
    for i, (code, label, vals) in enumerate(rows, 1):
        assert code not in code_row, f"{table_id}: duplicate row key {code}"
        code_row[code] = i
        for col, v in enumerate(vals, 1):
            if v is not None:
                values[(code, col)] = v
    targets, sources, rels = set(), set(), []
    for tgt, srcs, cols in relations:
        for col in cols:
            total = Decimal(0)
            for s in srcs:
                assert (s, col) in values, f"{table_id}: source {s} c{col} missing"
                total += Decimal(values[(s, col)])
                sources.add((s, col))
            assert total == Decimal(values[(tgt, col)]), \
                f"{table_id}: {tgt} c{col} sum {total} != printed {values[(tgt, col)]}"
            targets.add((tgt, col))
            rels.append({"type": "sum",
                         "sources": [f"r{code_row[s]}c{col}" for s in srcs],
                         "target": f"r{code_row[tgt]}c{col}"})
    cells, n_sa = [], 0
    for i, (code, label, vals) in enumerate(rows, 1):
        for col, v in enumerate(vals, 1):
            if v is None:
                continue
            key = (code, col)
            cell = {"id": f"r{i}c{col}", "row": i, "col": col, "value": v}
            if key in targets:
                cell["role"] = "total"
            elif key in standalone:
                assert key not in sources, f"{table_id}: {key} standalone but is a source"
                cell["role"] = "standalone"
                cell["why"] = standalone[key]
                n_sa += 1
            else:
                assert key in sources, f"{table_id}: {key} uncovered"
                cell["role"] = "leaf"
            cells.append(cell)
    assert (len(cells), len(rels), n_sa) == expect, \
        f"{table_id}: got {(len(cells), len(rels), n_sa)}, expected {expect}"
    doc = {"table_id": table_id, "source": source, "unit_note": unit_note,
           "columns": [{"index": 1, "label": "2025 actual"},
                       {"index": 2, "label": "2026 est."},
                       {"index": 3, "label": "2027 est."}],
           "rows": [{"index": i, "label": label} for i, (_, label, _) in enumerate(rows, 1)],
           "cells": cells, "relations": rels}
    out = f"tables/omb/{table_id.split('/', 1)[1]}.cells.json"
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {out}: {len(cells)} cells, {len(rels)} relations, {n_sa} standalone")

PDF = "sources/omb/budget-2027-app-2-3-legislative.pdf"

def csce():
    build(
        "omb/budget-appendix-fy2027-leg-csce-salaries-expenses",
        {"path": PDF, "table": "009-0110-0-1-801", "page": 30,
         "title": "Commission on Security and Cooperation in Europe - Salaries and Expenses (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). Commission on Security and Cooperation in Europe (id 009-0110-0-1-801), the first account of the Legislative Branch Boards and Commissions department: P&F starts PDF page 30 (printed 42) bottom right column and continues on PDF page 31 (printed 43) top LEFT column (the right column of p31 is the separate MedPAC account 235-1550); ObjClass + Employment follow on p31 left. No 0900 row printed (sole activity 0001 feeds nothing). Zero-suppressed blanks per convention (blank != zero): 3050 c2 nets to zero (1+3-4) and prints blank, so 3000 c2 has no encodable relation; 4010 blank c1, 4011 blank c3 leave 4020 single-source in those columns. Negatives as printed (3020).",
        [
            ("0001 Direct program activity", ["3", "3", "7"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["3", "3", "3"]),
            ("1100 Appropriation", ["3", "3", "7"]),
            ("1930 Total budgetary resources available", ["6", "6", "10"]),
            ("1941 Unexpired unobligated balance, end of year", ["3", "3", "3"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", [None, "1", None]),
            ("3010 New obligations, unexpired accounts", ["3", "3", "7"]),
            ("3020 Outlays (gross)", ["-2", "-4", "-6"]),
            ("3050 Unpaid obligations, end of year", ["1", None, "1"]),
            ("3100 Obligated balance, start of year", [None, "1", None]),
            ("3200 Obligated balance, end of year", ["1", None, "1"]),
            ("4000 Budget authority, gross", ["3", "3", "7"]),
            ("4010 Outlays from new discretionary authority", [None, "3", "6"]),
            ("4011 Outlays from discretionary balances", ["2", "1", None]),
            ("4020 Outlays, gross (total)", ["2", "4", "6"]),
            ("4180 Budget authority, net (total)", ["3", "3", "7"]),
            ("4190 Outlays, net (total)", ["2", "4", "6"]),
            ("11.1 Personnel compensation: Full-time permanent", ["2", "2", "2"]),
            ("25.1 Advisory and assistance services", ["1", "1", "5"]),
            ("99.9 Total new obligations, unexpired accounts", ["3", "3", "7"]),
            ("1001 Direct civilian full-time equivalent employment", ["13", "13", "13"]),
        ],
        [
            ("1930", ["1000", "1100"], [1, 2, 3]),
            ("3050", ["3010", "3020"], [1, 3]),
            ("4020", ["4010", "4011"], [2]),
            ("99.9", ["11.1", "25.1"], [1, 2, 3]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            **{("1941", c): MEMO for c in (1, 2, 3)},
            ("3000", 2): "Unpaid balance brought forward " + ZSUP + " (3050 c2 = 1+3-4 = 0, printed blank)",
            ("3010", 2): "New obligations " + ZSUP + " (3050 c2 = 1+3-4 = 0, printed blank)",
            ("3020", 2): "Outlays " + ZSUP + " (3050 c2 = 1+3-4 = 0, printed blank)",
            ("3100", 2): MEMO + "; equals 3000 (no uncollected payments in this account)",
            ("3200", 1): MEMO + "; equals 3050 (no uncollected payments in this account)",
            ("3200", 3): MEMO + "; equals 3050 (no uncollected payments in this account)",
            **{("4000", c): "Restates 1100 as gross discretionary budget authority; single-source into 4180" + M2 for c in (1, 2, 3)},
            ("4010", 3): "Single-source into 4020 Outlays gross (4011 blank this column)" + M2,
            ("4011", 1): "Single-source into 4020 Outlays gross (4010 blank this column)" + M2,
            ("4020", 1): "Single-source outlays gross total (equals 4011; 4010 blank this column); 4190 also single-source" + M2,
            ("4020", 3): "Single-source outlays gross total (equals 4010; 4011 blank this column); 4190 also single-source" + M2,
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = 4020 gross (no offsets)" + M2 for c in (1, 2, 3)},
            **{("1001", c): FTE for c in (1, 2, 3)},
        },
        (55, 9, 28),
    )

def macpac():
    build(
        "omb/budget-appendix-fy2027-leg-macpac-salaries-expenses",
        {"path": PDF, "table": "009-1801-0-1-551", "page": 32,
         "title": "Medicaid and CHIP Payment and Access Commission - Salaries and Expenses (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). Medicaid and CHIP Payment and Access Commission (id 009-1801-0-1-551), PDF page 32 (printed 44): P&F left column, ObjClass + Employment right column. No 0900 row and no 1000 unobligated-balance row printed (1930 = 1900 = 1100 single-source chains). Zero-suppressed blanks per convention: 3050 c2 (1+9-10) and c3 (11-11) net to zero and print blank, so 3000/3010/3020 have encodable relations only in c1; 4011 blank c3 leaves 4020 c3 single-source. 99.5 'Adjustment for rounding' prints only in c3 (=2) and 99.9 c3 = 99.0 + 99.5 = 9+2 = 11 sums EXACTLY as printed - no tolerance. Negatives as printed (3020).",
        [
            ("0123 Medicaid and CHIP Payment and Access Commission (Direct)", ["9", "9", "11"]),
            ("1100 Appropriation", ["9", "9", "11"]),
            ("1900 Budget authority (total)", ["9", "9", "11"]),
            ("1930 Total budgetary resources available", ["9", "9", "11"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["2", "1", None]),
            ("3010 New obligations, unexpired accounts", ["9", "9", "11"]),
            ("3020 Outlays (gross)", ["-10", "-10", "-11"]),
            ("3050 Unpaid obligations, end of year", ["1", None, None]),
            ("3100 Obligated balance, start of year", ["2", "1", None]),
            ("3200 Obligated balance, end of year", ["1", None, None]),
            ("4000 Budget authority, gross", ["9", "9", "11"]),
            ("4010 Outlays from new discretionary authority", ["8", "9", "11"]),
            ("4011 Outlays from discretionary balances", ["2", "1", None]),
            ("4020 Outlays, gross (total)", ["10", "10", "11"]),
            ("4180 Budget authority, net (total)", ["9", "9", "11"]),
            ("4190 Outlays, net (total)", ["10", "10", "11"]),
            ("11.1 Personnel compensation: Full-time permanent", ["4", "4", "4"]),
            ("12.1 Civilian personnel benefits", ["2", "2", "2"]),
            ("25.1 Advisory and assistance services", ["3", "3", "3"]),
            ("99.0 Direct obligations", ["9", "9", "9"]),
            ("99.5 Adjustment for rounding", [None, None, "2"]),
            ("99.9 Total new obligations, unexpired accounts", ["9", "9", "11"]),
            ("1001 Direct civilian full-time equivalent employment", ["34", "34", "34"]),
        ],
        [
            ("3050", ["3000", "3010", "3020"], [1]),
            ("4020", ["4010", "4011"], [1, 2]),
            ("99.0", ["11.1", "12.1", "25.1"], [1, 2, 3]),
            ("99.9", ["99.0", "99.5"], [3]),
        ],
        {
            **{("0123", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            **{("1100", c): "Single-source into 1900 Budget authority (no other budget authority)" + M2 for c in (1, 2, 3)},
            **{("1900", c): "Single-source budget authority total (equals 1100 appropriation)" + M2 for c in (1, 2, 3)},
            **{("1930", c): "Single-source total budgetary resources (equals 1900; no unobligated-balance rows printed)" + M2 for c in (1, 2, 3)},
            ("3000", 2): "Unpaid balance brought forward " + ZSUP + " (3050 c2 = 1+9-10 = 0, printed blank)",
            ("3010", 2): "New obligations " + ZSUP + " (3050 c2 = 1+9-10 = 0, printed blank)",
            ("3010", 3): "New obligations " + ZSUP + " (3050 c3 = 11-11 = 0, printed blank)",
            ("3020", 2): "Outlays " + ZSUP + " (3050 c2 = 1+9-10 = 0, printed blank)",
            ("3020", 3): "Outlays " + ZSUP + " (3050 c3 = 11-11 = 0, printed blank)",
            ("3100", 1): MEMO + "; equals 3000 (no uncollected payments in this account)",
            ("3100", 2): MEMO + "; equals 3000 (no uncollected payments in this account)",
            ("3200", 1): MEMO + "; equals 3050 (no uncollected payments in this account)",
            **{("4000", c): "Restates 1900 as gross discretionary budget authority; single-source into 4180" + M2 for c in (1, 2, 3)},
            ("4010", 3): "Single-source into 4020 Outlays gross (4011 blank this column)" + M2,
            ("4020", 3): "Single-source outlays gross total (equals 4010; 4011 blank this column); 4190 also single-source" + M2,
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = 4020 gross (no offsets)" + M2 for c in (1, 2, 3)},
            ("99.9", 1): "Single-source total new obligations (equals 99.0; 99.5 rounding adjustment blank this column)" + M2,
            ("99.9", 2): "Single-source total new obligations (equals 99.0; 99.5 rounding adjustment blank this column)" + M2,
            **{("1001", c): FTE for c in (1, 2, 3)},
        },
        (60, 7, 36),
    )

def uscc():
    build(
        "omb/budget-appendix-fy2027-leg-uscc-salaries-expenses",
        {"path": PDF, "table": "292-2973-0-1-801", "page": 32,
         "title": "United States-China Economic and Security Review Commission - Salaries and Expenses (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). United States-China Economic and Security Review Commission (id 292-2973-0-1-801): P&F on PDF page 32 (printed 44) right column; ObjClass + Employment on PDF page 33 (printed 45) LEFT column (the right column of p33 belongs to the separate USCIRF account 295-2975). No 0900 row and no 1900 row printed (1100 feeds 1930 alongside 1000). Zero-suppressed blank: 3050 c1 nets to zero (4-4) and prints blank, so 3010/3020 have encodable relations only in c2/c3. 99.5 'Adjustment for rounding' prints in ALL THREE columns (1/1/1) and 99.9 = 99.0 + 99.5 sums EXACTLY in each (4/5/4) - no tolerance; the ObjClass 99.9 equals the P&F 0001 obligations (4/5/4) as a cross-schedule identity (not encoded). Negatives as printed (3020).",
        [
            ("0001 United States-China Economic and Security Review Commission (Direct)", ["4", "5", "4"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["2", "2", "1"]),
            ("1100 Appropriation", ["4", "4", "4"]),
            ("1930 Total budgetary resources available", ["6", "6", "5"]),
            ("1941 Unexpired unobligated balance, end of year", ["2", "1", "1"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", [None, None, "1"]),
            ("3010 New obligations, unexpired accounts", ["4", "5", "4"]),
            ("3020 Outlays (gross)", ["-4", "-4", "-4"]),
            ("3050 Unpaid obligations, end of year", [None, "1", "1"]),
            ("3100 Obligated balance, start of year", [None, None, "1"]),
            ("3200 Obligated balance, end of year", [None, "1", "1"]),
            ("4000 Budget authority, gross", ["4", "4", "4"]),
            ("4010 Outlays from new discretionary authority", ["3", "3", "3"]),
            ("4011 Outlays from discretionary balances", ["1", "1", "1"]),
            ("4020 Outlays, gross (total)", ["4", "4", "4"]),
            ("4180 Budget authority, net (total)", ["4", "4", "4"]),
            ("4190 Outlays, net (total)", ["4", "4", "4"]),
            ("11.1 Personnel compensation: Full-time permanent", ["2", "2", "2"]),
            ("12.1 Civilian personnel benefits", ["1", "1", "1"]),
            ("25.1 Advisory and assistance services", [None, "1", None]),
            ("99.0 Direct obligations", ["3", "4", "3"]),
            ("99.5 Adjustment for rounding", ["1", "1", "1"]),
            ("99.9 Total new obligations, unexpired accounts", ["4", "5", "4"]),
            ("1001 Direct civilian full-time equivalent employment", ["19", "20", "20"]),
        ],
        [
            ("1930", ["1000", "1100"], [1, 2, 3]),
            ("3050", ["3010", "3020"], [2]),
            ("3050", ["3000", "3010", "3020"], [3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("99.0", ["11.1", "12.1"], [1, 3]),
            ("99.0", ["11.1", "12.1", "25.1"], [2]),
            ("99.9", ["99.0", "99.5"], [1, 2, 3]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            **{("1941", c): MEMO for c in (1, 2, 3)},
            ("3010", 1): "New obligations " + ZSUP + " (3050 c1 = 4-4 = 0, printed blank)",
            ("3020", 1): "Outlays " + ZSUP + " (3050 c1 = 4-4 = 0, printed blank)",
            ("3100", 3): MEMO + "; equals 3000 (no uncollected payments in this account)",
            ("3200", 2): MEMO + "; equals 3050 (no uncollected payments in this account)",
            ("3200", 3): MEMO + "; equals 3050 (no uncollected payments in this account)",
            **{("4000", c): "Restates 1100 as gross discretionary budget authority; single-source into 4180" + M2 for c in (1, 2, 3)},
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = 4020 gross (no offsets)" + M2 for c in (1, 2, 3)},
            **{("1001", c): FTE for c in (1, 2, 3)},
        },
        (64, 14, 23),
    )

def uscirf():
    build(
        "omb/budget-appendix-fy2027-leg-uscirf-salaries-expenses",
        {"path": PDF, "table": "295-2975-0-1-801", "page": 33,
         "title": "United States Commission on International Religious Freedom - Salaries and Expenses (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). United States Commission on International Religious Freedom (id 295-2975-0-1-801), PDF page 33 (printed 45): the P&F STARTS at the bottom of the LEFT column (0001, 1000) and CONTINUES at the top of the RIGHT column of the same page (1001 through 4190) - within-page column flow, same layout as GAO pp28-29; ObjClass + Employment follow in the right column. The left column above the P&F start is the separate US-China account 292-2973. No 0900 row and no 1900 row printed. 1001 is a non-add memo subset of 1000 (c1 only). Zero-suppressed blank: 3050 c1 nets to zero (4+1-4-1, via the expired 3011/3041 pair) and prints blank, so 3010/3011/3020/3041 have encodable relations only where 3050 prints (c2 two-source, c3 three-source). 99.5 'Adjustment for rounding' prints c2/c3 (=1) and 99.9 = 99.0 + 99.5 sums EXACTLY there - no tolerance. Negatives as printed (3020, 3041).",
        [
            ("0001 United States Commission on International Religious Freedom (Direct)", ["4", "5", "5"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["2", "2", "2"]),
            ("1001 Discretionary unobligated balance brought fwd, Oct 1", ["2", None, None]),
            ("1100 Appropriation", ["4", "5", "5"]),
            ("1930 Total budgetary resources available", ["6", "7", "7"]),
            ("1941 Unexpired unobligated balance, end of year", ["2", "2", "2"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", [None, None, "1"]),
            ("3010 New obligations, unexpired accounts", ["4", "5", "5"]),
            ("3011 Obligations (\"upward adjustments\"), expired accounts", ["1", None, None]),
            ("3020 Outlays (gross)", ["-4", "-4", "-4"]),
            ("3041 Recoveries of prior year unpaid obligations, expired", ["-1", None, None]),
            ("3050 Unpaid obligations, end of year", [None, "1", "2"]),
            ("3100 Obligated balance, start of year", [None, None, "1"]),
            ("3200 Obligated balance, end of year", [None, "1", "2"]),
            ("4000 Budget authority, gross", ["4", "5", "5"]),
            ("4010 Outlays from new discretionary authority", ["2", "2", "2"]),
            ("4011 Outlays from discretionary balances", ["2", "2", "2"]),
            ("4020 Outlays, gross (total)", ["4", "4", "4"]),
            ("4180 Budget authority, net (total)", ["4", "5", "5"]),
            ("4190 Outlays, net (total)", ["4", "4", "4"]),
            ("11.1 Personnel compensation: Full-time permanent", ["2", "2", "2"]),
            ("25.2 Other services from non-Federal sources", ["2", "2", "2"]),
            ("99.0 Direct obligations", ["4", "4", "4"]),
            ("99.5 Adjustment for rounding", [None, "1", "1"]),
            ("99.9 Total new obligations, unexpired accounts", ["4", "5", "5"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["20", "20", "20"]),
        ],
        [
            ("1930", ["1000", "1100"], [1, 2, 3]),
            ("3050", ["3010", "3020"], [2]),
            ("3050", ["3000", "3010", "3020"], [3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("99.0", ["11.1", "25.2"], [1, 2, 3]),
            ("99.9", ["99.0", "99.5"], [2, 3]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            ("1001", 1): "Memorandum (non-add): discretionary subset of the 1000 unobligated balance, does not feed the section arithmetic (do not add into 1930)",
            **{("1941", c): MEMO for c in (1, 2, 3)},
            ("3010", 1): "New obligations " + ZSUP + " (3050 c1 = 4+1-4-1 = 0, printed blank)",
            ("3011", 1): "Expired upward adjustment " + ZSUP + " (3050 c1 = 4+1-4-1 = 0, printed blank)",
            ("3020", 1): "Outlays " + ZSUP + " (3050 c1 = 4+1-4-1 = 0, printed blank)",
            ("3041", 1): "Expired recovery " + ZSUP + " (3050 c1 = 4+1-4-1 = 0, printed blank)",
            ("3100", 3): MEMO + "; equals 3000 (no uncollected payments in this account)",
            ("3200", 2): MEMO + "; equals 3050 (no uncollected payments in this account)",
            ("3200", 3): MEMO + "; equals 3050 (no uncollected payments in this account)",
            **{("4000", c): "Restates 1100 as gross discretionary budget authority; single-source into 4180" + M2 for c in (1, 2, 3)},
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = 4020 gross (no offsets)" + M2 for c in (1, 2, 3)},
            ("99.9", 1): "Single-source total new obligations (equals 99.0; 99.5 rounding adjustment blank this column)" + M2,
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
        },
        (65, 13, 27),
    )

UNITS = {"csce": csce, "macpac": macpac, "uscc": uscc, "uscirf": uscirf}
UNITS[sys.argv[1]]()
