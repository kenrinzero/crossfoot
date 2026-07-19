# Build AoC units #118-120 (PDF pp9-12 / printed 21-24). Values read from
# renders aoc-p9..p12-render.png, cross-checked against text extracts.
# Run with: sob | hob | cpp
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

def sob():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-senate-office-buildings",
        {"path": PDF, "table": "001-0123-0-1-801", "page": 9,
         "title": "Architect of the Capitol - Senate Office Buildings (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). AoC Senate Office Buildings (id 001-0123-0-1-801): P&F starts PDF page 9 (printed 21) bottom right and continues PDF page 10 (printed 22) left column; ObjClass + Employment p10 left. Printed note: includes the Senate Restaurant Fund and Senate Wellness Center Fund. 1011 (+4 c2) is the receiving twin of the Senate Preservation Fund's 1010 transfer (unit #107, printed [000-5509] cross-reference) - inter-unit consistency held at ship time (not encoded). 1070 is genuinely two-source in c1 (1000+1021) AND c2 (1000+1011) but single-source in c3. 6-source 3050 c1. 4040 c1 is a single-source total (= 4033) that feeds 4070/4080 c1 as a leaf. Negatives as printed (3020, 3040, 3041, 4033, 4040).",
        [
            ("0001 Senate Office Buildings (Direct)", ["115", "160", "170"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["100", "129", "96"]),
            ("1011 Unobligated balance transfer from other acct [000-5509]", [None, "4", None]),
            ("1021 Recoveries of prior year unpaid obligations", ["5", None, None]),
            ("1070 Unobligated balance (total)", ["105", "133", "96"]),
            ("1100 Appropriation", ["139", "123", "253"]),
            ("1900 Budget authority (total)", ["139", "123", "253"]),
            ("1930 Total budgetary resources available", ["244", "256", "349"]),
            ("1941 Unexpired unobligated balance, end of year", ["129", "96", "179"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["78", "59", "90"]),
            ("3010 New obligations, unexpired accounts", ["115", "160", "170"]),
            ("3011 Obligations (\"upward adjustments\"), expired accounts", ["2", None, None]),
            ("3020 Outlays (gross)", ["-129", "-129", "-162"]),
            ("3040 Recoveries of prior year unpaid obligations, unexpired", ["-5", None, None]),
            ("3041 Recoveries of prior year unpaid obligations, expired", ["-2", None, None]),
            ("3050 Unpaid obligations, end of year", ["59", "90", "98"]),
            ("3100 Obligated balance, start of year", ["78", "59", "90"]),
            ("3200 Obligated balance, end of year", ["59", "90", "98"]),
            ("4000 Budget authority, gross", ["139", "123", "253"]),
            ("4010 Outlays from new discretionary authority", ["76", "79", "114"]),
            ("4011 Outlays from discretionary balances", ["53", "50", "48"]),
            ("4020 Outlays, gross (total)", ["129", "129", "162"]),
            ("4033 Non-Federal sources", ["-1", None, None]),
            ("4040 Offsets against gross budget authority and outlays (total)", ["-1", None, None]),
            ("4052 Offsetting collections credited to expired accounts", ["1", None, None]),
            ("4070 Budget authority, net (discretionary)", ["139", "123", "253"]),
            ("4080 Outlays, net (discretionary)", ["128", "129", "162"]),
            ("4180 Budget authority, net (total)", ["139", "123", "253"]),
            ("4190 Outlays, net (total)", ["128", "129", "162"]),
            ("11.1 Full-time permanent", ["39", "40", "41"]),
            ("11.3 Other than full-time permanent", ["3", "3", "3"]),
            ("11.5 Other personnel compensation", ["7", "7", "7"]),
            ("11.9 Total personnel compensation", ["49", "50", "51"]),
            ("12.1 Civilian personnel benefits", ["19", "19", "19"]),
            ("23.1 Rental payments to GSA", ["4", "4", "4"]),
            ("23.2 Rental payments to others", ["2", "2", "2"]),
            ("25.1 Advisory and assistance services", ["3", "3", "15"]),
            ("25.3 Other goods and services from Federal sources", ["1", "1", "1"]),
            ("25.4 Operation and maintenance of facilities", ["18", "44", "41"]),
            ("26.0 Supplies and materials", ["6", "6", "6"]),
            ("31.0 Equipment", ["1", "1", "1"]),
            ("32.0 Land and structures", ["12", "30", "30"]),
            ("99.9 Total new obligations, unexpired accounts", ["115", "160", "170"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["489", "509", "515"]),
        ],
        [
            ("1070", ["1000", "1021"], [1]),
            ("1070", ["1000", "1011"], [2]),
            ("1930", ["1070", "1900"], [1, 2]),
            ("1930", ["1000", "1900"], [3]),
            ("3050", ["3000", "3010", "3011", "3020", "3040", "3041"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("4070", ["4000", "4040", "4052"], [1]),
            ("4080", ["4020", "4040"], [1]),
            ("11.9", ["11.1", "11.3", "11.5"], [1, 2, 3]),
            ("99.9", ["11.9", "12.1", "23.1", "23.2", "25.1", "25.3", "25.4", "26.0", "31.0", "32.0"], [1, 2, 3]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            **{("1100", c): "Single-source into 1900 Budget authority total (no other budget authority)" + M2 for c in (1, 2, 3)},
            ("1070", 3): "Single-source unobligated balance total (equals 1000; 1011/1021 blank this column)" + M2 + ". 1930 this column sums 1000+1900 directly per family precedent",
            ("1941", 1): MEMO, ("1941", 2): MEMO, ("1941", 3): MEMO,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            ("4000", 2): "Restates 1900 as gross discretionary; 4070 this column is single-source (no offsets)" + M2,
            ("4000", 3): "Restates 1900 as gross discretionary; 4070 this column is single-source (no offsets)" + M2,
            ("4033", 1): "Single-source into 4040 offsets total (sole collection line)" + M2,
            ("4070", 2): "Single-source net discretionary (equals 4000; no offsets this column); 4180 also single-source" + M2,
            ("4070", 3): "Single-source net discretionary (equals 4000; no offsets this column); 4180 also single-source" + M2,
            ("4080", 2): "Single-source outlays net (equals 4020; no offsets this column); 4190 also single-source" + M2,
            ("4080", 3): "Single-source outlays net (equals 4020; no offsets this column); 4190 also single-source" + M2,
            **{("4180", c): "Single-source net total = 4070 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net total = 4080 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
        },
        (116, 19, 32),
    )

def hob():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-house-office-buildings",
        {"path": PDF, "table": "001-0127-0-1-801", "page": 10,
         "title": "Architect of the Capitol - House Office Buildings (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). AoC House Office Buildings (id 001-0127-0-1-801): P&F on PDF page 10 (printed 22) right column; ObjClass tail + Employment on PDF page 11 (printed 23) top left. Printed note: includes the House of Representatives Wellness Center Fund. Rich transfer topology: 1010 (-1/-5) unobligated-balance transfers to [001-1833] and 1120 (-10/-46 c2/c3) appropriation transfers to [001-1833] (the House Historic Buildings Revitalization Trust Fund receives both - its 1011/1121 rows mirror them), plus 1121 (+4 c1) received from [000-0400]. 1160 is genuinely multi-source in ALL three columns. 6-source 3050 c1. 4060 c1 is a single-source total (= 4052) that feeds 4070 c1 as a leaf; 4040 c1 likewise (= 4033). ObjClass prints both 99.0 Direct and 99.9 (equal, single-source -> 99.9 standalone). Negatives as printed (1010, 1120, 3020, 3040, 3041, 4033, 4040).",
        [
            ("0001 House Office Buildings (Direct)", ["121", "140", "185"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["110", "142", "99"]),
            ("1001 Discretionary unobligated balance brought fwd, Oct 1", ["110", None, None]),
            ("1010 Unobligated balance transfer to other accts [001-1833]", ["-1", "-5", None]),
            ("1021 Recoveries of prior year unpaid obligations", ["4", None, None]),
            ("1070 Unobligated balance (total)", ["113", "137", "99"]),
            ("1100 Appropriation", ["146", "112", "435"]),
            ("1120 Appropriations transferred to other acct [001-1833]", [None, "-10", "-46"]),
            ("1121 Appropriations transferred from other acct [000-0400]", ["4", None, None]),
            ("1160 Appropriation, discretionary (total)", ["150", "102", "389"]),
            ("1900 Budget authority (total)", ["150", "102", "389"]),
            ("1930 Total budgetary resources available", ["263", "239", "488"]),
            ("1941 Unexpired unobligated balance, end of year", ["142", "99", "303"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["122", "82", "93"]),
            ("3010 New obligations, unexpired accounts", ["121", "140", "185"]),
            ("3011 Obligations (\"upward adjustments\"), expired accounts", ["3", None, None]),
            ("3020 Outlays (gross)", ["-158", "-129", "-159"]),
            ("3040 Recoveries of prior year unpaid obligations, unexpired", ["-4", None, None]),
            ("3041 Recoveries of prior year unpaid obligations, expired", ["-2", None, None]),
            ("3050 Unpaid obligations, end of year", ["82", "93", "119"]),
            ("3100 Obligated balance, start of year", ["122", "82", "93"]),
            ("3200 Obligated balance, end of year", ["82", "93", "119"]),
            ("4000 Budget authority, gross", ["150", "102", "389"]),
            ("4010 Outlays from new discretionary authority", ["67", "65", "97"]),
            ("4011 Outlays from discretionary balances", ["91", "64", "62"]),
            ("4020 Outlays, gross (total)", ["158", "129", "159"]),
            ("4033 Non-Federal sources", ["-1", None, None]),
            ("4040 Offsets against gross budget authority and outlays (total)", ["-1", None, None]),
            ("4052 Offsetting collections credited to expired accounts", ["1", None, None]),
            ("4060 Additional offsets against budget authority only (total)", ["1", None, None]),
            ("4070 Budget authority, net (discretionary)", ["150", "102", "389"]),
            ("4080 Outlays, net (discretionary)", ["157", "129", "159"]),
            ("4180 Budget authority, net (total)", ["150", "102", "389"]),
            ("4190 Outlays, net (total)", ["157", "129", "159"]),
            ("11.1 Full-time permanent", ["43", "43", "48"]),
            ("11.3 Other than full-time permanent", ["3", "3", "3"]),
            ("11.5 Other personnel compensation", ["6", "6", "6"]),
            ("11.9 Total personnel compensation", ["52", "52", "57"]),
            ("12.1 Civilian personnel benefits", ["21", "21", "22"]),
            ("25.1 Advisory and assistance services", ["4", "15", "43"]),
            ("25.4 Operation and maintenance of facilities", ["5", "5", "6"]),
            ("26.0 Supplies and materials", ["5", "5", "5"]),
            ("32.0 Land and structures", ["34", "42", "52"]),
            ("99.0 Direct obligations", ["121", "140", "185"]),
            ("99.9 Total new obligations, unexpired accounts", ["121", "140", "185"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["563", "557", "584"]),
        ],
        [
            ("1070", ["1000", "1010", "1021"], [1]),
            ("1070", ["1000", "1010"], [2]),
            ("1160", ["1100", "1121"], [1]),
            ("1160", ["1100", "1120"], [2, 3]),
            ("1930", ["1070", "1900"], [1, 2]),
            ("1930", ["1000", "1900"], [3]),
            ("3050", ["3000", "3010", "3011", "3020", "3040", "3041"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("4070", ["4000", "4040", "4060"], [1]),
            ("4080", ["4020", "4040"], [1]),
            ("11.9", ["11.1", "11.3", "11.5"], [1, 2, 3]),
            ("99.0", ["11.9", "12.1", "25.1", "25.4", "26.0", "32.0"], [1, 2, 3]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            ("1001", 1): "Memorandum (non-add): discretionary subset of the 1000 unobligated balance, does not feed the section arithmetic (do not add into 1070)",
            ("1070", 3): "Single-source unobligated balance total (equals 1000; transfer/recovery rows blank this column)" + M2 + ". 1930 this column sums 1000+1900 directly per family precedent",
            **{("1900", c): None for c in ()},
            ("1941", 1): MEMO, ("1941", 2): MEMO, ("1941", 3): MEMO,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            ("4000", 2): "Restates 1900 as gross discretionary; 4070 this column is single-source (no offsets)" + M2,
            ("4000", 3): "Restates 1900 as gross discretionary; 4070 this column is single-source (no offsets)" + M2,
            ("4033", 1): "Single-source into 4040 offsets total (sole collection line)" + M2,
            ("4052", 1): "Single-source into 4060 additional-offsets total (sole line)" + M2,
            ("4070", 2): "Single-source net discretionary (equals 4000; no offsets this column); 4180 also single-source" + M2,
            ("4070", 3): "Single-source net discretionary (equals 4000; no offsets this column); 4180 also single-source" + M2,
            ("4080", 2): "Single-source outlays net (equals 4020; no offsets this column); 4190 also single-source" + M2,
            ("4080", 3): "Single-source outlays net (equals 4020; no offsets this column); 4190 also single-source" + M2,
            **{("4180", c): "Single-source net total = 4070 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net total = 4080 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("99.9", c): "Single-source total new obligations (equals 99.0 Direct; no reimbursable obligations)" + M2 for c in (1, 2, 3)},
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
        },
        (116, 22, 34),
    )

def cpp():
    build(
        "omb/budget-appendix-fy2027-leg-aoc-capitol-power-plant",
        {"path": PDF, "table": "001-0133-0-1-801", "page": 11,
         "title": "Architect of the Capitol - Capitol Power Plant (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). AoC Capitol Power Plant (id 001-0133-0-1-801): P&F on PDF page 11 (printed 23) right column; ObjClass + Employment on PDF page 12 (printed 24) left column. The richest relation topology in the AoC family: genuine reimbursable program (0900 = 0001 + 0801 in ALL columns), offsetting-collections spending authority in ALL columns (1900 = 1100 + 1700), two-source 4040 = 4030 + 4033 in ALL columns, and both 99.0 Direct and 99.0 Reimbursable rows with 99.9 = Direct + Reimbursable. 1940 'Unobligated balance expiring' memo prints -1 in c1. 4060 c1 is a single-source total (= 4052) feeding 4070 c1 as a leaf. Cross-schedule sanity (not encoded): 99.0 Direct = 0001 (170/138/135), 99.0 Reimbursable = 0801 (9/10/10), 99.9 = 0900 (179/148/145). Negatives as printed (1940, 3020, 3041, 4030, 4033, 4040).",
        [
            ("0001 Capitol Power Plant (Direct)", ["170", "138", "135"]),
            ("0801 Capitol Power Plant (Reimbursable)", ["9", "10", "10"]),
            ("0900 Total new obligations, unexpired accounts", ["179", "148", "145"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["100", "54", "57"]),
            ("1001 Discretionary unobligated balance brought fwd, Oct 1", ["100", None, None]),
            ("1100 Appropriation", ["124", "141", "167"]),
            ("1700 Collected", ["10", "10", "10"]),
            ("1900 Budget authority (total)", ["134", "151", "177"]),
            ("1930 Total budgetary resources available", ["234", "205", "234"]),
            ("1940 Unobligated balance expiring", ["-1", None, None]),
            ("1941 Unexpired unobligated balance, end of year", ["54", "57", "89"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["63", "110", "76"]),
            ("3010 New obligations, unexpired accounts", ["179", "148", "145"]),
            ("3011 Obligations (\"upward adjustments\"), expired accounts", ["4", None, None]),
            ("3020 Outlays (gross)", ["-133", "-182", "-182"]),
            ("3041 Recoveries of prior year unpaid obligations, expired", ["-3", None, None]),
            ("3050 Unpaid obligations, end of year", ["110", "76", "39"]),
            ("3100 Obligated balance, start of year", ["63", "110", "76"]),
            ("3200 Obligated balance, end of year", ["110", "76", "39"]),
            ("4000 Budget authority, gross", ["134", "151", "177"]),
            ("4010 Outlays from new discretionary authority", ["80", "95", "127"]),
            ("4011 Outlays from discretionary balances", ["53", "87", "55"]),
            ("4020 Outlays, gross (total)", ["133", "182", "182"]),
            ("4030 Federal sources", ["-9", "-8", "-8"]),
            ("4033 Non-Federal sources", ["-2", "-2", "-2"]),
            ("4040 Offsets against gross budget authority and outlays (total)", ["-11", "-10", "-10"]),
            ("4052 Offsetting collections credited to expired accounts", ["1", None, None]),
            ("4060 Additional offsets against budget authority only (total)", ["1", None, None]),
            ("4070 Budget authority, net (discretionary)", ["124", "141", "167"]),
            ("4080 Outlays, net (discretionary)", ["122", "172", "172"]),
            ("4180 Budget authority, net (total)", ["124", "141", "167"]),
            ("4190 Outlays, net (total)", ["122", "172", "172"]),
            ("11.1 Full-time permanent", ["13", "13", "14"]),
            ("11.5 Other personnel compensation", ["2", "2", "2"]),
            ("11.9 Total personnel compensation", ["15", "15", "16"]),
            ("12.1 Civilian personnel benefits", ["6", "6", "7"]),
            ("23.3 Communications, utilities, and miscellaneous charges", ["47", "55", "50"]),
            ("25.1 Advisory and assistance services", ["6", "6", "6"]),
            ("25.4 Operation and maintenance of facilities", ["33", "25", "25"]),
            ("26.0 Supplies and materials", ["6", "6", "6"]),
            ("32.0 Land and structures", ["57", "25", "25"]),
            ("99.0d|99.0 Direct obligations", ["170", "138", "135"]),
            ("99.0r|99.0 Reimbursable obligations", ["9", "10", "10"]),
            ("99.9 Total new obligations, unexpired accounts", ["179", "148", "145"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["119", "117", "125"]),
        ],
        [
            ("0900", ["0001", "0801"], [1, 2, 3]),
            ("1900", ["1100", "1700"], [1, 2, 3]),
            ("1930", ["1000", "1900"], [1, 2, 3]),
            ("3050", ["3000", "3010", "3011", "3020", "3041"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("4040", ["4030", "4033"], [1, 2, 3]),
            ("4070", ["4000", "4040", "4060"], [1]),
            ("4070", ["4000", "4040"], [2, 3]),
            ("4080", ["4020", "4040"], [1, 2, 3]),
            ("11.9", ["11.1", "11.5"], [1, 2, 3]),
            ("99.0d", ["11.9", "12.1", "23.3", "25.1", "25.4", "26.0", "32.0"], [1, 2, 3]),
            ("99.9", ["99.0d", "99.0r"], [1, 2, 3]),
        ],
        {
            ("1001", 1): "Memorandum (non-add): discretionary subset of the 1000 unobligated balance, does not feed the section arithmetic",
            ("1940", 1): MEMO,
            ("1941", 1): MEMO, ("1941", 2): MEMO, ("1941", 3): MEMO,
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            ("4052", 1): "Single-source into 4060 additional-offsets total (sole line)" + M2,
            **{("4180", c): "Single-source net total = 4070 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net total = 4080 net discretionary (no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
        },
        (123, 33, 21),
    )

UNITS = {"sob": sob, "hob": hob, "cpp": cpp}
UNITS[sys.argv[1]]()
