import json, sys
from decimal import Decimal

M2 = "; schema minItems 2 forbids single-source sum"
MEMO = "Memorandum (non-add) entry: does not feed the section arithmetic"
FTE = ("Employment Summary line (full-time equivalent employment, a headcount, "
       "not USD millions); participates in no arithmetic on this schedule")

def build(table_id, source, unit_note, rows, relations, standalone, expect):
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

# 1. House Historic Buildings Revitalization Trust Fund
def build_hhb():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-house-historic-buildings",
        {"path": PDF, "table": "001-1833-0-1-801", "page": 11,
         "title": "Architect of the Capitol - House Historic Buildings Revitalization Trust Fund (Program and Financing)",
         "period": "FY 2027"},
        "USD millions. AoC House Historic Buildings Revitalization Trust Fund (id 001-1833-0-1-801): P&F on PDF page 11 (printed 23) left column. Receives transfers from House Office Buildings (unit #119): unobligated balance transfers (1011 unobligated balance transfer from HOB's 1010 line) and appropriation transfers (1121 appropriations transferred from HOB's 1120 line). 1070 is multi-source in c1/c2 (1000+1011) but single-source in c3. 1930 c2/c3 is multi-source (1070+4000). Change in obligated balance: 3050 c1 is two-source (3000+3020; no 3010 new obligations row prints), while c2/c3 are three-source (3000+3010+3020). Negatives as printed (3020).",
        [
            ("0001 House Historic Buildings Revitalization Trust Fund (Direct)", [None, "7", "9"]),
            ("0900 Total new obligations, unexpired accounts (object class 25.1)", [None, "7", "9"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["1", "2", "10"]),
            ("1011 Unobligated balance transfer from other acct [001-0127]", ["1", "5", None]),
            ("1070 Unobligated balance (total)", ["2", "7", "10"]),
            ("1121 Appropriations transferred from other acct [001-0127]", [None, "10", "46"]),
            ("1930 Total budgetary resources available", ["2", "17", "56"]),
            ("1941 Unexpired unobligated balance, end of year", ["2", "10", "47"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["2", "1", "6"]),
            ("3010 New obligations, unexpired accounts", [None, "7", "9"]),
            ("3020 Outlays (gross)", ["-1", "-2", "-6"]),
            ("3050 Unpaid obligations, end of year", ["1", "6", "9"]),
            ("3100 Obligated balance, start of year", ["2", "1", "6"]),
            ("3200 Obligated balance, end of year", ["1", "6", "9"]),
            ("4000 Budget authority, gross", [None, "10", "46"]),
            ("4010 Outlays from new discretionary authority", [None, None, "2"]),
            ("4011 Outlays from discretionary balances", ["1", "2", "4"]),
            ("4020 Outlays, gross (total)", ["1", "2", "6"]),
            ("4180 Budget authority, net (total)", [None, "10", "46"]),
            ("4190 Outlays, net (total)", ["1", "2", "6"]),
        ],
        [
            ("1070", ["1000", "1011"], [1, 2]),
            ("1930", ["1070", "4000"], [2]),
            ("1930", ["1000", "4000"], [3]),
            ("3050", ["3000", "3020"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [3]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (2, 3)},
            **{("0900", c): "Single-source total obligations (equals 0001)" + M2 for c in (2, 3)},
            ("1070", 3): "Single-source unobligated balance total (equals 1000; 1011 blank this column)" + M2 + ". 1930 this column sums 1000+4000 directly",
            **{("1121", c): "Single-source discretionary appropriation transfer (sole budget authority line)" + M2 for c in (2, 3)},
            ("1930", 1): "Single-source total budgetary resources (equals 1070; 4000 blank this column)" + M2,
            ("1941", 1): MEMO, ("1941", 2): MEMO, ("1941", 3): MEMO,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("4011", c): "Single-source outlays from discretionary balances (sole source of gross outlays)" + M2 for c in (1, 2)},
            ("4020", 1): "Single-source outlays gross (equals 4011; 4010 blank this column)" + M2,
            ("4020", 2): "Single-source outlays gross (equals 4011; 4010 blank this column)" + M2,
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (2, 3)},
            **{("4190", c): "Single-source outlays net total = 4020 gross (no offsets)" + M2 for c in (1, 2, 3)},
        },
        (51, 8, 26),
    )

# 2. House Office Buildings Fund
def build_hobf():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-house-office-buildings-fund",
        {"path": PDF, "table": "001-0137-0-1-801", "page": 11,
         "title": "Architect of the Capitol - House Office Buildings Fund (Program and Financing)",
         "period": "FY 2027"},
        "USD millions. AoC House Office Buildings Fund (id 001-0137-0-1-801): P&F on PDF page 11 (printed 23) left column bottom. A degenerate 4-cell table with zero relations. Offsetting-collections rows 1702 and 1724 net to zero. Budget authority net (4180) and outlays net (4190) are completely blank (suppressed).",
        [
            ("1702 Offsetting collections (previously unavailable)", [None, "13", "13"]),
            ("1724 Spending authority from offsetting collections precluded from obligation (limitation on obligations)", [None, "-13", "-13"]),
        ],
        [],
        {
            ("1702", 2): "Standalone collection line; participates in no arithmetic on this schedule",
            ("1702", 3): "Standalone collection line; participates in no arithmetic on this schedule",
            ("1724", 2): "Standalone precluded collection line; participates in no arithmetic on this schedule",
            ("1724", 3): "Standalone precluded collection line; participates in no arithmetic on this schedule",
        },
        (4, 0, 4)
    )

# 3. Library Buildings and Grounds
def build_lbg():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-library-buildings-grounds",
        {"path": PDF, "table": "001-0155-0-1-801", "page": 12,
         "title": "Architect of the Capitol - Library Buildings and Grounds (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
         "USD millions except the Employment Summary FTE line (headcount). AoC Library Buildings and Grounds (id 001-0155-0-1-801): P&F on PDF page 12 (printed 24) right column; ObjClass + Employment on PDF page 12 (printed 24) right column. Direct program activity 0001 (78/104/115) and reimbursable 0801 (-/2/2) sum to total new obligations 0900 (78/106/117). 1070 is multi-source in c1 (1000+1021) but single-source in c2/c3 (equals 1000). 1930 c1 is multi-source (1070+1900) while c2/c3 sum 1000+1900 directly. Change in obligated balance: 3050 c1 is five-source (3000+3010+3011+3020+3040+3041 = 137+78+3-98-1-1 = 118). Offsets: two-source 4040 c1 (4030 Federal + 4033 Non-Federal). ObjClass has 99.0 Direct (78/104/115) and 99.0 Reimbursable (-/2/2) summing to 99.9 (78/106/117). Negatives as printed (3020, 3040, 3041, 4030, 4033, 4040).",
         [
            ("0001 Library Buildings and Grounds (Direct)", ["78", "104", "115"]),
            ("0801 Library Buildings and Grounds (Reimbursable)", [None, "2", "2"]),
            ("0900 Total new obligations, unexpired accounts", ["78", "106", "117"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["98", "89", "42"]),
            ("1001 Discretionary unobligated balance brought fwd, Oct 1", ["98", None, None]),
            ("1021 Recoveries of prior year unpaid obligations", ["1", None, None]),
            ("1070 Unobligated balance (total)", ["99", "89", "42"]),
            ("1100 Appropriation", ["65", "57", "184"]),
            ("1700 Collected", ["3", "2", "2"]),
            ("1900 Budget authority (total)", ["68", "59", "186"]),
            ("1930 Total budgetary resources available", ["167", "148", "228"]),
            ("1941 Unexpired unobligated balance, end of year", ["89", "42", "111"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["137", "118", "36"]),
            ("3010 New obligations, unexpired accounts", ["78", "106", "117"]),
            ("3011 Obligations (\"upward adjustments\"), expired accounts", ["3", None, None]),
            ("3020 Outlays (gross)", ["-98", "-188", "-100"]),
            ("3040 Recoveries of prior year unpaid obligations, unexpired", ["-1", None, None]),
            ("3041 Recoveries of prior year unpaid obligations, expired", ["-1", None, None]),
            ("3050 Unpaid obligations, end of year", ["118", "36", "53"]),
            ("3100 Obligated balance, start of year", ["137", "118", "36"]),
            ("3200 Obligated balance, end of year", ["118", "36", "53"]),
            ("4000 Budget authority, gross", ["68", "59", "186"]),
            ("4010 Outlays from new discretionary authority", ["30", "34", "72"]),
            ("4011 Outlays from discretionary balances", ["68", "154", "28"]),
            ("4020 Outlays, gross (total)", ["98", "188", "100"]),
            ("4030 Federal sources", ["-3", "-2", "-2"]),
            ("4033 Non-Federal sources", ["-1", None, None]),
            ("4040 Offsets against gross budget authority and outlays (total)", ["-4", "-2", "-2"]),
            ("4052 Offsetting collections credited to expired accounts", ["1", None, None]),
            ("4070 Budget authority, net (discretionary)", ["65", "57", "184"]),
            ("4080 Outlays, net (discretionary)", ["94", "186", "98"]),
            ("4180 Budget authority, net (total)", ["65", "57", "184"]),
            ("4190 Outlays, net (total)", ["94", "186", "98"]),
            ("11.1 Full-time permanent", ["19", "20", "20"]),
            ("11.5 Other personnel compensation", ["3", "3", "3"]),
            ("11.9 Total personnel compensation", ["22", "23", "23"]),
            ("12.1 Civilian personnel benefits", ["9", "9", "9"]),
            ("23.2 Rental payments to others", ["2", "2", "2"]),
            ("25.1 Advisory and assistance services", ["8", "12", "23"]),
            ("25.4 Operation and maintenance of facilities", ["6", "6", "6"]),
            ("26.0 Supplies and materials", ["2", "2", "2"]),
            ("32.0 Land and structures", ["29", "50", "50"]),
            ("99.0d|99.0 Direct obligations", ["78", "104", "115"]),
            ("99.0r|99.0 Reimbursable obligations", [None, "2", "2"]),
            ("99.9 Total new obligations, unexpired accounts", ["78", "106", "117"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["178", "181", "183"]),
         ],
         [
            ("0900", ["0001", "0801"], [2, 3]),
            ("1070", ["1000", "1021"], [1]),
            ("1900", ["1100", "1700"], [1, 2, 3]),
            ("1930", ["1070", "1900"], [1]),
            ("1930", ["1000", "1900"], [2, 3]),
            ("3050", ["3000", "3010", "3011", "3020", "3040", "3041"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("4040", ["4030", "4033"], [1]),
            ("4070", ["4000", "4040", "4052"], [1]),
            ("4070", ["4000", "4040"], [2, 3]),
            ("4080", ["4020", "4040"], [1, 2, 3]),
            ("11.9", ["11.1", "11.5"], [1, 2, 3]),
            ("99.0d", ["11.9", "12.1", "23.2", "25.1", "25.4", "26.0", "32.0"], [1, 2, 3]),
            ("99.9", ["99.0d", "99.0r"], [2, 3]),
         ],
         {
            ("0001", 1): "Single-source direct obligations (no reimbursable obligations in this column); 0900/99.9 also single-source" + M2,
            ("0900", 1): "Single-source total obligations (equals 0001; 0801 blank this column)" + M2,
            ("99.9", 1): "Single-source total obligations (equals 99.0d; 99.0r blank this column)" + M2,
            ("1001", 1): "Memorandum (non-add): discretionary subset of the 1000 unobligated balance, does not feed the section arithmetic",
            ("1070", 2): "Single-source unobligated balance total (equals 1000; 1021 blank this column)" + M2 + ". 1930 this column sums 1000+1900 directly",
            ("1070", 3): "Single-source unobligated balance total (equals 1000; 1021 blank this column)" + M2 + ". 1930 this column sums 1000+1900 directly",
            ("1941", 1): MEMO, ("1941", 2): MEMO, ("1941", 3): MEMO,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            ("4030", 2): "Single-source into 4040 offsets total (4033 blank this column)" + M2,
            ("4030", 3): "Single-source into 4040 offsets total (4033 blank this column)" + M2,
            **{("4180", c): "Single-source net total = 4070 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net total = 4080 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
         },
         (122, 30, 26),
    )

# 4. Capitol Police Buildings, Grounds and Security
def build_cpb():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-capitol-police-buildings",
        {"path": PDF, "table": "001-0171-0-1-801", "page": 12,
         "title": "Architect of the Capitol - Capitol Police Buildings, Grounds and Security (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
         "USD millions except the Employment Summary FTE line (headcount). AoC Capitol Police Buildings, Grounds and Security (id 001-0171-0-1-801): P&F starts on PDF page 12 (printed 24) bottom right column and continues on PDF page 13 (printed 25) top left column; ObjClass + Employment on PDF page 13 (printed 25) left column. 1070 c1 is multi-source (1000+1021) but single-source c2/c3 (equals 1000). 1900 is multi-source in c1 (1100+1700) but single-source in c2/c3 (equals 1100). 1930 c1 is multi-source (1070+1900) while c2/c3 sum 1000+1900 directly. Change in obligated balance: 3050 c1 is six-source (3000+3010+3011+3020+3040+3041 = 149+192+2-208-14-3 = 118). Offsets: 4040 c1 is single-source (equals 4030). ObjClass has only direct obligations 99.9 (192/168/150). Negatives as printed (3020, 3040, 3041, 4030, 4040).",
         [
            ("0001 Capitol Police Buildings, Grounds, and Security (Direct)", ["192", "168", "150"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["348", "259", "166"]),
            ("1001 Discretionary unobligated balance brought fwd, Oct 1", ["348", None, None]),
            ("1021 Recoveries of prior year unpaid obligations", ["14", None, None]),
            ("1070 Unobligated balance (total)", ["362", "259", "166"]),
            ("1100 Appropriation", ["85", "75", "239"]),
            ("1700 Collected", ["4", None, None]),
            ("1900 Budget authority (total)", ["89", "75", "239"]),
            ("1930 Total budgetary resources available", ["451", "334", "405"]),
            ("1941 Unexpired unobligated balance, end of year", ["259", "166", "255"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["149", "118", "113"]),
            ("3010 New obligations, unexpired accounts", ["192", "168", "150"]),
            ("3011 Obligations (\"upward adjustments\"), expired accounts", ["2", None, None]),
            ("3020 Outlays (gross)", ["-208", "-173", "-117"]),
            ("3040 Recoveries of prior year unpaid obligations, unexpired", ["-14", None, None]),
            ("3041 Recoveries of prior year unpaid obligations, expired", ["-3", None, None]),
            ("3050 Unpaid obligations, end of year", ["118", "113", "146"]),
            ("3100 Obligated balance, start of year", ["149", "118", "113"]),
            ("3200 Obligated balance, end of year", ["118", "113", "146"]),
            ("4000 Budget authority, gross", ["89", "75", "239"]),
            ("4010 Outlays from new discretionary authority", ["32", "30", "60"]),
            ("4011 Outlays from discretionary balances", ["176", "143", "57"]),
            ("4020 Outlays, gross (total)", ["208", "173", "117"]),
            ("4030 Federal sources", ["-4", None, None]),
            ("4040 Offsets against gross budget authority and outlays (total)", ["-4", None, None]),
            ("4070 Budget authority, net (discretionary)", ["85", "75", "239"]),
            ("4080 Outlays, net (discretionary)", ["204", "173", "117"]),
            ("4180 Budget authority, net (total)", ["85", "75", "239"]),
            ("4190 Outlays, net (total)", ["204", "173", "117"]),
            ("11.1 Full-time permanent", ["8", "9", "10"]),
            ("11.3 Other than full-time permanent", ["1", "1", "1"]),
            ("11.5 Other personnel compensation", ["1", "1", "1"]),
            ("11.9 Total personnel compensation", ["10", "11", "12"]),
            ("12.1 Civilian personnel benefits", ["4", "4", "4"]),
            ("23.2 Rental payments to others", ["15", "15", "15"]),
            ("25.1 Advisory and assistance services", ["129", "88", "69"]),
            ("25.3 Other goods and services from Federal sources", ["1", "1", "1"]),
            ("25.4 Operation and maintenance of facilities", ["24", "24", "24"]),
            ("32.0 Land and structures", ["9", "25", "25"]),
            ("99.9 Total new obligations, unexpired accounts", ["192", "168", "150"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["48", "53", "58"]),
         ],
         [
            ("1070", ["1000", "1021"], [1]),
            ("1900", ["1100", "1700"], [1]),
            ("1930", ["1070", "1900"], [1]),
            ("1930", ["1000", "1900"], [2, 3]),
            ("3050", ["3000", "3010", "3011", "3020", "3040", "3041"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("4070", ["4000", "4040"], [1]),
            ("4080", ["4020", "4040"], [1]),
            ("11.9", ["11.1", "11.3", "11.5"], [1, 2, 3]),
            ("99.9", ["11.9", "12.1", "23.2", "25.1", "25.3", "25.4", "32.0"], [1, 2, 3]),
         ],
         {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            ("1001", 1): "Memorandum (non-add): discretionary subset of the 1000 unobligated balance, does not feed the section arithmetic",
            ("1070", 2): "Single-source unobligated balance total (equals 1000; 1021 blank this column)" + M2 + ". 1930 this column sums 1000+1900 directly",
            ("1070", 3): "Single-source unobligated balance total (equals 1000; 1021 blank this column)" + M2 + ". 1930 this column sums 1000+1900 directly",
            ("1100", 2): "Single-source into 1900 Budget authority total (1700 Collected blank this column)" + M2,
            ("1100", 3): "Single-source into 1900 Budget authority total (1700 Collected blank this column)" + M2,
            ("1941", 1): MEMO, ("1941", 2): MEMO, ("1941", 3): MEMO,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            ("4000", 2): "Restates 1900 as gross discretionary; 4070 this column is single-source (no offsets)" + M2,
            ("4000", 3): "Restates 1900 as gross discretionary; 4070 this column is single-source (no offsets)" + M2,
            ("4030", 1): "Single-source into 4040 offsets total (sole collection line)" + M2,
            ("4070", 2): "Single-source net discretionary (equals 4000; no offsets this column); 4180 also single-source" + M2,
            ("4070", 3): "Single-source net discretionary (equals 4000; no offsets this column); 4180 also single-source" + M2,
            ("4080", 2): "Single-source outlays net (equals 4020; no offsets this column); 4190 also single-source" + M2,
            ("4080", 3): "Single-source outlays net (equals 4020; no offsets this column); 4190 also single-source" + M2,
            **{("4180", c): "Single-source net total = 4070 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net total = 4080 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
         },
         (107, 19, 33),
    )

# 5. Capitol Visitor Center
def build_cvc():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-capitol-visitor-center",
        {"path": PDF, "table": "001-0161-0-1-801", "page": 13,
         "title": "Architect of the Capitol - Capitol Visitor Center (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
         "USD millions except the Employment Summary FTE line (headcount). AoC Capitol Visitor Center (id 001-0161-0-1-801): complete on PDF page 13 (printed 25) right column. Receives 1121 transfer (+1 c1) from Capitol Grounds (unit #117) - its 1120b row matches. 1160 discretionary total is multi-source in c1 (1100+1121) but single-source in c2/c3 (equals 1100). Change in obligated balance: 3050 c1 is five-source (3000+3010+3011+3020+3041 = 8+29+1-31-1 = 6). ObjClass direct obligations sum into 99.9 (29/30/31). Negatives as printed (3020, 3041).",
         [
            ("0001 Capitol Visitor Center (Direct)", ["29", "30", "31"]),
            ("1000 Unobligated balance brought forward, Oct 1", [None, None, None]), # all blank
            ("1100 Appropriation", ["28", "30", "31"]),
            ("1121 Appropriations transferred from other acct [001-0108]", ["1", None, None]),
            ("1160 Appropriation, discretionary (total)", ["29", "30", "31"]),
            ("1930 Total budgetary resources available", ["29", "30", "31"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["8", "6", "2"]),
            ("3010 New obligations, unexpired accounts", ["29", "30", "31"]),
            ("3011 Obligations (\"upward adjustments\"), expired accounts", ["1", None, None]),
            ("3020 Outlays (gross)", ["-31", "-34", "-27"]),
            ("3041 Recoveries of prior year unpaid obligations, expired", ["-1", None, None]),
            ("3050 Unpaid obligations, end of year", ["6", "2", "6"]),
            ("3100 Obligated balance, start of year", ["8", "6", "2"]),
            ("3200 Obligated balance, end of year", ["6", "2", "6"]),
            ("4000 Budget authority, gross", ["29", "30", "31"]),
            ("4010 Outlays from new discretionary authority", ["25", "28", "25"]),
            ("4011 Outlays from discretionary balances", ["6", "6", "2"]),
            ("4020 Outlays, gross (total)", ["31", "34", "27"]),
            ("4180 Budget authority, net (total)", ["29", "30", "31"]),
            ("4190 Outlays, net (total)", ["31", "34", "27"]),
            ("11.1 Full-time permanent", ["17", "18", "19"]),
            ("11.5 Other personnel compensation", ["1", "1", "1"]),
            ("11.9 Total personnel compensation", ["18", "19", "20"]),
            ("12.1 Civilian personnel benefits", ["7", "8", "8"]),
            ("25.1 Advisory and assistance services", ["1", "1", "1"]),
            ("25.4 Operation and maintenance of facilities", ["2", "1", "1"]),
            ("31.0 Equipment", ["1", "1", "1"]),
            ("99.9 Total new obligations, unexpired accounts", ["29", "30", "31"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["220", "228", "234"]),
         ],
         [
            ("1160", ["1100", "1121"], [1]),
            ("3050", ["3000", "3010", "3011", "3020", "3041"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("11.9", ["11.1", "11.5"], [1, 2, 3]),
            ("99.9", ["11.9", "12.1", "25.1", "25.4", "31.0"], [1, 2, 3]),
         ],
         {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            ("1100", 2): "Single-source into 1160 Appropriation discretionary total (1121 transfer blank this column)" + M2,
            ("1100", 3): "Single-source into 1160 Appropriation discretionary total (1121 transfer blank this column)" + M2,
            **{("1160", c): "Single-source discretionary appropriation total (equals 1100; 1121 transfer blank this column)" + M2 for c in (2, 3)},

            ("1930", 1): "Single-source total budgetary resources (equals 1160; 1000 unobligated balance is blank)" + M2,
            ("1930", 2): "Single-source total budgetary resources (equals 1160; 1000 unobligated balance is blank)" + M2,
            ("1930", 3): "Single-source total budgetary resources (equals 1160; 1000 unobligated balance is blank)" + M2,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("4000", c): "Restates 1160 as gross discretionary budget authority; single-source into 4180" + M2 for c in (1, 2, 3)},
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = 4020 gross (no offsets)" + M2 for c in (1, 2, 3)},
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
         },
         (78, 13, 28),
    )

# 6. Capitol Visitor Center Revolving Fund
def build_cvcr():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-capitol-visitor-center-revolving",
        {"path": PDF, "table": "001-4296-0-3-801", "page": 13,
         "title": "Architect of the Capitol - Capitol Visitor Center Revolving Fund (Program and Financing)",
         "period": "FY 2027"},
         "USD millions. AoC Capitol Visitor Center Revolving Fund (id 001-4296-0-3-801): P&F starts PDF page 13 (printed 25) right column bottom and continues PDF page 14 (printed 26) left column top. Offsetting collections: two-source 4040 c1 (4031 Interest + 4033 Non-Federal). 4080 (and 4190) is gross outlays 4020 plus offsets 4040 (4-9 = -5, 8-9 = -1, 8-9 = -1). 4180 net budget authority is completely blank (suppressed). Negatives as printed (3020, 4031, 4033, 4040, 4080, 4190).",
         [
            ("0801 Capitol Visitor Center Revolving Fund (Reimbursable)", ["6", "9", "6"]),
            ("0900 Total new obligations, unexpired accounts (object class 26.0)", ["6", "9", "6"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["14", "17", "17"]),
            ("1700 Collected", ["9", "9", "9"]),
            ("1930 Total budgetary resources available", ["23", "26", "26"]),
            ("1941 Unexpired unobligated balance, end of year", ["17", "17", "20"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["1", "3", "4"]),
            ("3010 New obligations, unexpired accounts", ["6", "9", "6"]),
            ("3020 Outlays (gross)", ["-4", "-8", "-8"]),
            ("3050 Unpaid obligations, end of year", ["3", "4", "2"]),
            ("3100 Obligated balance, start of year", ["1", "3", "4"]),
            ("3200 Obligated balance, end of year", ["3", "4", "2"]),
            ("4000 Budget authority, gross", ["9", "9", "9"]),
            ("4010 Outlays from new discretionary authority", [None, "6", "6"]),
            ("4011 Outlays from discretionary balances", ["4", "2", "2"]),
            ("4020 Outlays, gross (total)", ["4", "8", "8"]),
            ("4031 Interest on Federal securities", ["-1", None, None]),
            ("4033 Non-Federal sources", ["-8", "-9", "-9"]),
            ("4040 Offsets against gross budget authority and outlays (total)", ["-9", "-9", "-9"]),
            ("4080 Outlays, net (discretionary)", ["-5", "-1", "-1"]),
            ("4190 Outlays, net (total)", ["-5", "-1", "-1"]),
            ("5000 Total investments, SOY: Federal securities: Par value", ["15", "20", "20"]),
            ("5001 Total investments, EOY: Federal securities: Par value", ["20", "20", "20"]),
         ],
         [
            ("1930", ["1000", "1700"], [1, 2, 3]),
            ("3050", ["3000", "3010", "3020"], [1, 2, 3]),
            ("4020", ["4010", "4011"], [2, 3]),
            ("4040", ["4031", "4033"], [1]),
            ("4080", ["4020", "4040"], [1, 2, 3]),
         ],
         {
            ("0801", 1): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2,
            ("0801", 2): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2,
            ("0801", 3): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2,
            ("0900", 1): "Single-source total obligations (equals 0801)" + M2,
            ("0900", 2): "Single-source total obligations (equals 0801)" + M2,
            ("0900", 3): "Single-source total obligations (equals 0801)" + M2,
            **{("4000", c): "Restates gross discretionary budget authority; 4180 net is blank" + M2 for c in (1, 2, 3)},
            ("1941", 1): MEMO, ("1941", 2): MEMO, ("1941", 3): MEMO,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            ("4011", 1): "Single-source outlays from discretionary balances (sole source of gross outlays)" + M2,
            ("4033", 2): "Single-source into 4040 offsets total (4031 blank this column)" + M2,
            ("4033", 3): "Single-source into 4040 offsets total (4031 blank this column)" + M2,
            **{("4190", c): "Single-source outlays net total = 4080 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("5000", c): MEMO for c in (1, 2, 3)},
            **{("5001", c): MEMO for c in (1, 2, 3)},
         },
         (66, 12, 30),
    )

# 7. Recyclable Materials Revolving Fund
def build_rmr():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-recyclable-materials-revolving",
        {"path": PDF, "table": "001-4297-0-3-801", "page": 14,
         "title": "Architect of the Capitol - Recyclable Materials Revolving Fund (Program and Financing)",
         "period": "FY 2027"},
         "USD millions. AoC Recyclable Materials Revolving Fund (id 001-4297-0-3-801): P&F on PDF page 14 (printed 26) left column. A very simple 3-row table with no relations (all standalone). Budget authority net (4180) and outlays net (4190) are completely blank (suppressed).",
         [
            ("1000 Unobligated balance brought forward, Oct 1", ["1", "1", "1"]),
            ("1930 Total budgetary resources available", ["1", "1", "1"]),
            ("1941 Unexpired unobligated balance, end of year", ["1", "1", "1"]),
         ],
         [],
         {
            **{("1000", c): "Standalone balance row; participates in no arithmetic" for c in (1, 2, 3)},
            **{("1930", c): "Standalone balance row; participates in no arithmetic" for c in (1, 2, 3)},
            **{("1941", c): MEMO for c in (1, 2, 3)},
         },
         (9, 0, 9),
    )

# 8. Judiciary Office Building Development and Operations Fund
def build_job():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-judiciary-office-building",
        {"path": PDF, "table": "001-4518-0-4-801", "page": 14,
         "title": "Architect of the Capitol - Judiciary Office Building Development and Operations Fund (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
         "USD millions except the Employment Summary FTE line (headcount). AoC Judiciary Office Building Development and Operations Fund (id 001-4518-0-4-801): P&F on PDF page 14 (printed 26) left column; ObjClass + Employment on PDF page 14 (printed 26) right column. Offsetting collections: mandatory collected 1800 (39/15/15) is gross budget authority 1900. Unobligated balance total 1070 c1 is two-source (1000+1021). 1930 c1 is multi-source (1070+1900). Change in obligated balance: 3050 c1 is four-source (3000+3010+3020+3040 = 28+38-28-2 = 36). Outlays: gross mandatory outlays 4110 = 4100 + 4101. Offsets total 4130 = 4120 Federal + 4123 Non-Federal in c1. Net mandatory outlays 4170 = 4110 gross + 4130 offsets (28-39 = -11, 51-15 = 36, 15-15 = 0; c3 is zero so suppressed/blank). ObjClass direct obligations sum into 99.9 (38/22/20). Negatives as printed (3020, 3040, 4120, 4123, 4130, 4170 c1).",
         [
            ("0801 Operations and Maintenance", ["38", "22", "20"]),
            ("0900 Total new obligations, unexpired accounts (object class 26.0)", ["38", "22", "20"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["10", "13", "6"]),
            ("1021 Recoveries of prior year unpaid obligations", ["2", None, None]),
            ("1070 Unobligated balance (total)", ["12", "13", "6"]),
            ("1800 Collected", ["39", "15", "15"]),
            ("1900 Budget authority (total)", ["39", "15", "15"]),
            ("1930 Total budgetary resources available", ["51", "28", "21"]),
            ("1941 Unexpired unobligated balance, end of year", ["13", "6", "1"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["28", "36", "7"]),
            ("3010 New obligations, unexpired accounts", ["38", "22", "20"]),
            ("3020 Outlays (gross)", ["-28", "-51", "-15"]),
            ("3040 Recoveries of prior year unpaid obligations, unexpired", ["-2", None, None]),
            ("3050 Unpaid obligations, end of year", ["36", "7", "12"]),
            ("3100 Obligated balance, start of year", ["28", "36", "7"]),
            ("3200 Obligated balance, end of year", ["36", "7", "12"]),
            ("4090 Budget authority, gross", ["39", "15", "15"]),
            ("4100 Outlays from new mandatory authority", ["8", "15", "15"]),
            ("4101 Outlays from mandatory balances", ["20", "36", None]),
            ("4110 Outlays, gross (total)", ["28", "51", "15"]),
            ("4120 Federal sources", ["-27", "-15", "-15"]),
            ("4123 Non-Federal sources", ["-12", None, None]),
            ("4130 Offsets against gross budget authority and outlays (total)", ["-39", "-15", "-15"]),
            ("4170 Outlays, net (mandatory)", ["-11", "36", None]),
            ("11.1 Reimbursable obligations: Personnel compensation: Full-time permanent", ["1", "1", "1"]),
            ("11.9 Total personnel compensation", ["1", "1", "1"]),
            ("12.1 Civilian personnel benefits", ["1", "1", "1"]),
            ("23.3 Communications, utilities, and miscellaneous charges", ["5", "5", "5"]),
            ("25.1 Advisory and assistance services", ["1", "1", "1"]),
            ("25.4 Operation and maintenance of facilities", ["10", "7", "9"]),
            ("32.0 Land and structures", ["20", "7", "3"]),
            ("99.9 Total new obligations, unexpired accounts", ["38", "22", "20"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["15", "15", "15"]),
         ],
         [
            ("1070", ["1000", "1021"], [1]),
            ("1930", ["1070", "1900"], [1]),
            ("1930", ["1000", "1900"], [2, 3]),
            ("3050", ["3000", "3010", "3020", "3040"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4110", ["4100", "4101"], [1, 2]),
            ("4130", ["4120", "4123"], [1]),
            ("4170", ["4110", "4130"], [1, 2]),
            ("99.9", ["11.9", "12.1", "23.3", "25.1", "25.4", "32.0"], [1, 2, 3]),
         ],
         {
            ("0801", 1): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2,
            ("0801", 2): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2,
            ("0801", 3): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2,
            ("0900", 1): "Single-source total obligations (equals 0801)" + M2,
            ("0900", 2): "Single-source total obligations (equals 0801)" + M2,
            ("0900", 3): "Single-source total obligations (equals 0801)" + M2,
            ("1070", 2): "Single-source unobligated balance total (equals 1000; 1021 blank this column)" + M2 + ". 1930 this column sums 1000+1900 directly",
            ("1070", 3): "Single-source unobligated balance total (equals 1000; 1021 blank this column)" + M2 + ". 1930 this column sums 1000+1900 directly",
            **{("1800", c): "Restates mandatory Collected; single-source into gross budget authority 1900" + M2 for c in (1, 2, 3)},
            ("1941", 1): MEMO, ("1941", 2): MEMO, ("1941", 3): MEMO,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("4090", c): "Restates gross mandatory budget authority; net mandatory is blank (suppressed)" + M2 for c in (1, 2, 3)},
            ("4100", 3): "Single-source outlays from new mandatory authority (sole source of gross outlays)" + M2,
            ("4110", 3): "Single-source outlays gross total (equals 4100; 4101 blank this column)" + M2,
            ("4120", 2): "Single-source offsets total (4123 blank this column)" + M2,
            ("4120", 3): "Single-source offsets total (4123 blank this column)" + M2,
             ("4130", 3): "Single-source offsets total (equals 4120; 4123 blank this column)" + M2,
            ("11.1", 1): "Single-source total personnel compensation (sole detail row)" + M2,
            ("11.1", 2): "Single-source total personnel compensation (sole detail row)" + M2,
            ("11.1", 3): "Single-source total personnel compensation (sole detail row)" + M2,
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
         },
         (91, 15, 34),
    )

# 9. Botanic Garden
def build_bg():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-botanic-garden",
        {"path": PDF, "table": "009-0200-0-1-801", "page": 16,
         "title": "Architect of the Capitol - Botanic Garden (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
         "USD millions except the Employment Summary FTE line (headcount). Botanic Garden (id 009-0200-0-1-801): complete on PDF page 16 (printed 28). Receives 1121 transfer (+2 c1) from Capitol Grounds (unit #117) - its 1120b row matches. 1160 discretionary total is multi-source in c1 (1100+1121) but single-source in c2/c3 (equals 1100). 1070 c1 is multi-source (1000+1021) but single-source c2/c3. 1930 c1/c2 is multi-source (1070+1900) while c3 sums 1000+1900 directly. Change in obligated balance: 3050 c1 is four-source (3000+3010+3020+3040 = 17+21-25-1 = 12). ObjClass direct obligations sum into 99.9 (21/28/38). Negatives as printed (3020, 3040).",
         [
            ("0001 Botanic Garden (Direct)", ["21", "28", "38"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["17", "20", "14"]),
            ("1021 Recoveries of prior year unpaid obligations", ["1", None, None]),
            ("1070 Unobligated balance (total)", ["18", "20", "14"]),
            ("1100 Appropriation", ["21", "22", "70"]),
            ("1121 Appropriations transferred from other acct [001-0108]", ["2", None, None]),
            ("1160 Appropriation, discretionary (total)", ["23", "22", "70"]),
            ("1930 Total budgetary resources available", ["41", "42", "84"]),
            ("1941 Unexpired unobligated balance, end of year", ["20", "14", "46"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["17", "12", "10"]),
            ("3010 New obligations, unexpired accounts", ["21", "28", "38"]),
            ("3020 Outlays (gross)", ["-25", "-30", "-37"]),
            ("3040 Recoveries of prior year unpaid obligations, unexpired", ["-1", None, None]),
            ("3050 Unpaid obligations, end of year", ["12", "10", "11"]),
            ("3100 Obligated balance, start of year", ["17", "12", "10"]),
            ("3200 Obligated balance, end of year", ["12", "10", "11"]),
            ("4000 Budget authority, gross", ["23", "22", "70"]),
            ("4010 Outlays from new discretionary authority", ["13", "18", "35"]),
            ("4011 Outlays from discretionary balances", ["12", "12", "2"]),
            ("4020 Outlays, gross (total)", ["25", "30", "37"]),
            ("4180 Budget authority, net (total)", ["23", "22", "70"]),
            ("4190 Outlays, net (total)", ["25", "30", "37"]),
            ("11.1 Full-time permanent", ["7", "8", "9"]),
            ("11.3 Other than full-time permanent", ["1", "1", "1"]),
            ("11.9 Total personnel compensation", ["8", "9", "10"]),
            ("12.1 Civilian personnel benefits", ["3", "3", "3"]),
            ("25.1 Advisory and assistance services", ["3", "6", "12"]),
            ("25.4 Operation and maintenance of facilities", ["4", "4", "4"]),
            ("26.0 Supplies and materials", ["1", "1", "1"]),
            ("32.0 Land and structures", ["2", "5", "8"]),
            ("99.9 Total new obligations, unexpired accounts", ["21", "28", "38"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["82", "81", "84"]),
         ],
         [
            ("1070", ["1000", "1021"], [1]),
            ("1160", ["1100", "1121"], [1]),
            ("1930", ["1070", "1160"], [1]),
            ("1930", ["1000", "1160"], [2, 3]),
            ("3050", ["3000", "3010", "3020", "3040"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("11.9", ["11.1", "11.3"], [1, 2, 3]),
            ("99.9", ["11.9", "12.1", "25.1", "25.4", "26.0", "32.0"], [1, 2, 3]),
         ],
         {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            ("1070", 2): "Single-source unobligated balance total (equals 1000; 1021 blank this column)" + M2 + ". 1930 this column sums 1000+1160 directly",
            ("1070", 3): "Single-source unobligated balance total (equals 1000; 1021 blank this column)" + M2 + ". 1930 this column sums 1000+1160 directly",
            ("1100", 2): "Single-source into 1160 Appropriation discretionary total (1121 transfer blank this column)" + M2,
            ("1100", 3): "Single-source into 1160 Appropriation discretionary total (1121 transfer blank this column)" + M2,

            ("1941", 1): MEMO, ("1941", 2): MEMO, ("1941", 3): MEMO,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("4000", c): "Restates 1160 as gross discretionary budget authority; single-source into 4180" + M2 for c in (1, 2, 3)},
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = 4020 gross (no offsets)" + M2 for c in (1, 2, 3)},
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
         },
         (90, 17, 28),
    )

if __name__ == "__main__":
    build_hhb()
    build_hobf()
    build_lbg()
    build_cpb()
    build_cvc()
    build_cvcr()
    build_rmr()
    build_job()
    build_bg()
