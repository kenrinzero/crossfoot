# Build Architect of the Capitol units #115-117 (OMB FY2027 Legislative
# Branch, PDF pp8-9 / printed 20-21). Values read from renders
# aoc-p8-render.png / aoc-p9-render.png, cross-checked against text extracts.
# Run with: ccops | capitol-building | capitol-grounds
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

def ccops():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-capital-construction-ops",
        {"path": PDF, "table": "001-0100-0-1-801", "page": 8,
         "title": "Architect of the Capitol - Capital Construction and Operations (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). Architect of the Capitol - Capital Construction and Operations (id 001-0100-0-1-801), the AoC department starter, PDF page 8 (printed 20): P&F starts bottom LEFT column and continues top RIGHT column (within-page flow, USCIRF/GAO pattern); ObjClass + Employment follow in the right column. The left column above the AoC header is CBO's continuation (008-0100 - separate, already-shipped unit #75). Discretionary offsetting collections (1700 Collected, c1 only) make 1900 c1 two-source; the net section has no 4040... wait 4040 prints (4030+4033); no 4060 total row prints, so 4070 c1 = 4000+4040+4052 three-source. No 99.0 row in ObjClass (line items sum straight into 99.9). Negatives as printed (3020, 3041, 4030, 4033, 4040).",
        [
            ("0001 General Administration (Direct)", ["155", "159", "183"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["6", "5", "5"]),
            ("1001 Discretionary unobligated balance brought fwd, Oct 1", ["6", None, None]),
            ("1100 Appropriation", ["153", "159", "193"]),
            ("1700 Collected", ["1", None, None]),
            ("1900 Budget authority (total)", ["154", "159", "193"]),
            ("1930 Total budgetary resources available", ["160", "164", "198"]),
            ("1941 Unexpired unobligated balance, end of year", ["5", "5", "15"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["49", "42", "42"]),
            ("3010 New obligations, unexpired accounts", ["155", "159", "183"]),
            ("3011 Obligations (\"upward adjustments\"), expired accounts", ["3", None, None]),
            ("3020 Outlays (gross)", ["-160", "-159", "-166"]),
            ("3041 Recoveries of prior year unpaid obligations, expired", ["-5", None, None]),
            ("3050 Unpaid obligations, end of year", ["42", "42", "59"]),
            ("3100 Obligated balance, start of year", ["49", "42", "42"]),
            ("3200 Obligated balance, end of year", ["42", "42", "59"]),
            ("4000 Budget authority, gross", ["154", "159", "193"]),
            ("4010 Outlays from new discretionary authority", ["116", "119", "135"]),
            ("4011 Outlays from discretionary balances", ["44", "40", "31"]),
            ("4020 Outlays, gross (total)", ["160", "159", "166"]),
            ("4030 Federal sources", ["-1", None, None]),
            ("4033 Non-Federal sources", ["-1", None, None]),
            ("4040 Offsets against gross budget authority and outlays (total)", ["-2", None, None]),
            ("4052 Offsetting collections credited to expired accounts", ["1", None, None]),
            ("4070 Budget authority, net (discretionary)", ["153", "159", "193"]),
            ("4080 Outlays, net (discretionary)", ["158", "159", "166"]),
            ("4180 Budget authority, net (total)", ["153", "159", "193"]),
            ("4190 Outlays, net (total)", ["158", "159", "166"]),
            ("11.1 Full-time permanent", ["61", "63", "69"]),
            ("11.5 Other personnel compensation", ["2", "2", "3"]),
            ("11.9 Total personnel compensation", ["63", "65", "72"]),
            ("12.1 Civilian personnel benefits", ["27", "28", "30"]),
            ("23.2 Rental payments to others", ["1", "1", "1"]),
            ("25.1 Advisory and assistance services", ["46", "47", "60"]),
            ("25.4 Operation and maintenance of facilities", ["15", "15", "17"]),
            ("26.0 Supplies and materials", ["2", "2", "2"]),
            ("31.0 Equipment", ["1", "1", "1"]),
            ("99.9 Total new obligations, unexpired accounts", ["155", "159", "183"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["426", "436", "467"]),
        ],
        [
            ("1900", ["1100", "1700"], [1]),
            ("1930", ["1000", "1900"], [1, 2, 3]),
            ("3050", ["3000", "3010", "3011", "3020", "3041"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("4040", ["4030", "4033"], [1]),
            ("4070", ["4000", "4040", "4052"], [1]),
            ("4080", ["4020", "4040"], [1]),
            ("11.9", ["11.1", "11.5"], [1, 2, 3]),
            ("99.9", ["11.9", "12.1", "23.2", "25.1", "25.4", "26.0", "31.0"], [1, 2, 3]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            ("1001", 1): "Memorandum (non-add): discretionary subset of the 1000 unobligated balance, does not feed the section arithmetic",
            ("1100", 2): "Single-source into 1900 Budget authority total (1700 collections blank this column)" + M2,
            ("1100", 3): "Single-source into 1900 Budget authority total (1700 collections blank this column)" + M2,
            ("1941", 1): MEMO, ("1941", 2): MEMO, ("1941", 3): MEMO,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            ("4000", 2): "Restates 1900 as gross discretionary; 4070 this column is single-source (no offsets)" + M2,
            ("4000", 3): "Restates 1900 as gross discretionary; 4070 this column is single-source (no offsets)" + M2,
            ("4070", 2): "Single-source net discretionary (equals 4000; no offsets this column); 4180 also single-source" + M2,
            ("4070", 3): "Single-source net discretionary (equals 4000; no offsets this column); 4180 also single-source" + M2,
            ("4080", 2): "Single-source outlays net (equals 4020; no offsets this column); 4190 also single-source" + M2,
            ("4080", 3): "Single-source outlays net (equals 4020; no offsets this column); 4190 also single-source" + M2,
            **{("4180", c): "Single-source net total = 4070 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net total = 4080 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
        },
        (101, 19, 30),
    )

def capitol_building():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-capitol-building",
        {"path": PDF, "table": "001-0105-0-1-801", "page": 8,
         "title": "Architect of the Capitol - Capitol Building (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). Architect of the Capitol - Capitol Building (id 001-0105-0-1-801): P&F starts PDF page 8 (printed 20) bottom right column and continues PDF page 9 (printed 21) top left; ObjClass + Employment p9 left. Printed note: 'This presentation includes the Flag Office Revolving fund.' 1900 is single-source (= 1100) in every column, so 1100 is standalone and 1930 sums through 1900 (c1 = 1070+1900, c2/c3 = 1000+1900 with 1070 single-source there, family precedent). 6-source 3050 c1 (includes both 3040 unexpired and 3041 expired recoveries). Net section: no 4040 total row prints - 4070 c1 = 4000+4033+4052 three-source directly; no 99.0 row in ObjClass. Negatives as printed (3020, 3040, 3041, 4033).",
        [
            ("0001 Capitol Building (Direct)", ["60", "80", "88"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["113", "103", "97"]),
            ("1001 Discretionary unobligated balance brought fwd, Oct 1", ["113", None, None]),
            ("1021 Recoveries of prior year unpaid obligations", ["1", None, None]),
            ("1070 Unobligated balance (total)", ["114", "103", "97"]),
            ("1100 Appropriation", ["49", "74", "55"]),
            ("1900 Budget authority (total)", ["49", "74", "55"]),
            ("1930 Total budgetary resources available", ["163", "177", "152"]),
            ("1941 Unexpired unobligated balance, end of year", ["103", "97", "64"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["22", "26", "34"]),
            ("3010 New obligations, unexpired accounts", ["60", "80", "88"]),
            ("3011 Obligations (\"upward adjustments\"), expired accounts", ["2", None, None]),
            ("3020 Outlays (gross)", ["-56", "-72", "-58"]),
            ("3040 Recoveries of prior year unpaid obligations, unexpired", ["-1", None, None]),
            ("3041 Recoveries of prior year unpaid obligations, expired", ["-1", None, None]),
            ("3050 Unpaid obligations, end of year", ["26", "34", "64"]),
            ("3100 Obligated balance, start of year", ["22", "26", "34"]),
            ("3200 Obligated balance, end of year", ["26", "34", "64"]),
            ("4000 Budget authority, gross", ["49", "74", "55"]),
            ("4010 Outlays from new discretionary authority", ["32", "33", "22"]),
            ("4011 Outlays from discretionary balances", ["24", "39", "36"]),
            ("4020 Outlays, gross (total)", ["56", "72", "58"]),
            ("4033 Non-Federal sources", ["-1", None, None]),
            ("4052 Offsetting collections credited to expired accounts", ["1", None, None]),
            ("4070 Budget authority, net (discretionary)", ["49", "74", "55"]),
            ("4080 Outlays, net (discretionary)", ["55", "72", "58"]),
            ("4180 Budget authority, net (total)", ["49", "74", "55"]),
            ("4190 Outlays, net (total)", ["55", "72", "58"]),
            ("11.1 Full-time permanent", ["18", "18", "19"]),
            ("11.3 Other than full-time permanent", ["1", "1", "1"]),
            ("11.5 Other personnel compensation", ["3", "3", "3"]),
            ("11.9 Total personnel compensation", ["22", "22", "23"]),
            ("12.1 Civilian personnel benefits", ["9", "9", "10"]),
            ("25.1 Advisory and assistance services", ["5", "20", "25"]),
            ("25.4 Operation and maintenance of facilities", ["3", "3", "3"]),
            ("26.0 Supplies and materials", ["2", "4", "4"]),
            ("32.0 Land and structures", ["19", "22", "23"]),
            ("99.9 Total new obligations, unexpired accounts", ["60", "80", "88"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["232", "225", "227"]),
        ],
        [
            ("1070", ["1000", "1021"], [1]),
            ("1930", ["1070", "1900"], [1]),
            ("1930", ["1000", "1900"], [2, 3]),
            ("3050", ["3000", "3010", "3011", "3020", "3040", "3041"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("4070", ["4000", "4033", "4052"], [1]),
            ("4080", ["4020", "4033"], [1]),
            ("11.9", ["11.1", "11.3", "11.5"], [1, 2, 3]),
            ("99.9", ["11.9", "12.1", "25.1", "25.4", "26.0", "32.0"], [1, 2, 3]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            ("1001", 1): "Memorandum (non-add): discretionary subset of the 1000 unobligated balance, does not feed the section arithmetic (do not add into 1070)",
            **{("1100", c): "Single-source into 1900 Budget authority total (no offsetting collections in this account)" + M2 for c in (1, 2, 3)},
            ("1070", 2): "Single-source unobligated balance total (equals 1000; 1021 blank this column)" + M2 + ". 1930 this column sums 1000+1900 directly per family precedent",
            ("1070", 3): "Single-source unobligated balance total (equals 1000; 1021 blank this column)" + M2 + ". 1930 this column sums 1000+1900 directly per family precedent",
            ("1941", 1): MEMO, ("1941", 2): MEMO, ("1941", 3): MEMO,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            ("4000", 2): "Restates 1900 as gross discretionary; 4070 this column is single-source (no offsets)" + M2,
            ("4000", 3): "Restates 1900 as gross discretionary; 4070 this column is single-source (no offsets)" + M2,
            ("4070", 2): "Single-source net discretionary (equals 4000; no offsets this column); 4180 also single-source" + M2,
            ("4070", 3): "Single-source net discretionary (equals 4000; no offsets this column); 4180 also single-source" + M2,
            ("4080", 2): "Single-source outlays net (equals 4020; no offsets this column); 4190 also single-source" + M2,
            ("4080", 3): "Single-source outlays net (equals 4020; no offsets this column); 4190 also single-source" + M2,
            **{("4180", c): "Single-source net total = 4070 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net total = 4080 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
        },
        (103, 18, 33),
    )

def capitol_grounds():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-capitol-grounds",
        {"path": PDF, "table": "001-0108-0-1-801", "page": 9,
         "title": "Architect of the Capitol - Capitol Grounds (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). Architect of the Capitol - Capitol Grounds (id 001-0108-0-1-801), complete on PDF page 9 (printed 21) right column. TWO printed 1120 transfer rows (to [001-0161] and to [009-0200]) are distinct rows here; 1160 Appropriation discretionary (total) = 1100+1120+1120 = 22-1-2 = 19 in c1 (single-source = 1100 in c2/c3). Cross-account note (not encoded): the -1/-2 transfers reappear as receipts in accounts 001-0161 and 009-0200. Negatives as printed (1120 rows, 3020).",
        [
            ("0001 Capitol Grounds (Direct)", ["22", "19", "28"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["11", "8", "8"]),
            ("1100 Appropriation", ["22", "19", "34"]),
            ("1120a|1120 Appropriations transferred to other acct [001-0161]", ["-1", None, None]),
            ("1120b|1120 Appropriations transferred to other acct [009-0200]", ["-2", None, None]),
            ("1160 Appropriation, discretionary (total)", ["19", "19", "34"]),
            ("1930 Total budgetary resources available", ["30", "27", "42"]),
            ("1941 Unexpired unobligated balance, end of year", ["8", "8", "14"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["6", "10", "6"]),
            ("3010 New obligations, unexpired accounts", ["22", "19", "28"]),
            ("3020 Outlays (gross)", ["-18", "-23", "-21"]),
            ("3050 Unpaid obligations, end of year", ["10", "6", "13"]),
            ("3100 Obligated balance, start of year", ["6", "10", "6"]),
            ("3200 Obligated balance, end of year", ["10", "6", "13"]),
            ("4000 Budget authority, gross", ["19", "19", "34"]),
            ("4010 Outlays from new discretionary authority", ["13", "13", "15"]),
            ("4011 Outlays from discretionary balances", ["5", "10", "6"]),
            ("4020 Outlays, gross (total)", ["18", "23", "21"]),
            ("4180 Budget authority, net (total)", ["19", "19", "34"]),
            ("4190 Outlays, net (total)", ["18", "23", "21"]),
            ("11.1 Full-time permanent", ["7", "7", "8"]),
            ("11.5 Other personnel compensation", ["1", "1", "1"]),
            ("11.9 Total personnel compensation", ["8", "8", "9"]),
            ("12.1 Civilian personnel benefits", ["3", "3", "3"]),
            ("23.2 Rental payments to others", ["1", "1", "1"]),
            ("25.1 Advisory and assistance services", ["5", "4", "10"]),
            ("25.4 Operation and maintenance of facilities", ["2", "1", "1"]),
            ("26.0 Supplies and materials", ["1", "1", "2"]),
            ("31.0 Equipment", ["1", "1", "2"]),
            ("32.0 Land and structures", ["1", None, None]),
            ("99.9 Total new obligations, unexpired accounts", ["22", "19", "28"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["83", "84", "85"]),
        ],
        [
            ("1160", ["1100", "1120a", "1120b"], [1]),
            ("1930", ["1000", "1160"], [1, 2, 3]),
            ("3050", ["3000", "3010", "3020"], [1, 2, 3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("11.9", ["11.1", "11.5"], [1, 2, 3]),
            ("99.9", ["11.9", "12.1", "23.2", "25.1", "25.4", "26.0", "31.0", "32.0"], [1]),
            ("99.9", ["11.9", "12.1", "23.2", "25.1", "25.4", "26.0", "31.0"], [2, 3]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            ("1100", 2): "Single-source into 1160 Appropriation discretionary total (1120 transfer rows blank this column)" + M2,
            ("1100", 3): "Single-source into 1160 Appropriation discretionary total (1120 transfer rows blank this column)" + M2,
            ("1941", 1): MEMO, ("1941", 2): MEMO, ("1941", 3): MEMO,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("4000", c): "Restates 1160 as gross discretionary budget authority; single-source into 4180" + M2 for c in (1, 2, 3)},
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = 4020 gross (no offsets)" + M2 for c in (1, 2, 3)},
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
        },
        (90, 16, 26),
    )

UNITS = {"ccops": ccops, "capitol-building": capitol_building, "capitol-grounds": capitol_grounds}
UNITS[sys.argv[1]]()
