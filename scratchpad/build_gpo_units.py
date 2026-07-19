# Build the four GPO units (corpus #96-99) from OMB FY2027 Legislative
# Branch chapter, PDF pp26-28 (printed pp38-40). Values read from renders
# gpo-p26/p27-render.png + gao-p28-render.png, cross-checked against the
# text layer. Run with a unit argument: cong-pub | pip | bizops-pf | bizops-oc
import json, sys
from decimal import Decimal

M2 = "; schema minItems 2 forbids single-source sum"
MEMO = "Memorandum (non-add) entry: does not feed the section arithmetic"

def build(table_id, source, unit_note, rows, relations, standalone, expect):
    # rows: list of (label, [c1,c2,c3]) with None = blank as printed
    code_row = {}
    values = {}
    for i, (label, vals) in enumerate(rows, 1):
        code = label.split()[0]
        code_row[code] = i
        for col, v in enumerate(vals, 1):
            if v is not None:
                values[(code, col)] = v
    targets, sources = set(), set()
    rels = []
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
    for i, (label, vals) in enumerate(rows, 1):
        code = label.split()[0]
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
    doc = {
        "table_id": table_id,
        "source": source,
        "unit_note": unit_note,
        "columns": [{"index": 1, "label": "2025 actual"},
                    {"index": 2, "label": "2026 est."},
                    {"index": 3, "label": "2027 est."}],
        "rows": [{"index": i, "label": label} for i, (label, _) in enumerate(rows, 1)],
        "cells": cells,
        "relations": rels,
    }
    out = f"tables/omb/{table_id.split('/', 1)[1]}.cells.json"
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {out}: {len(cells)} cells, {len(rels)} relations, {n_sa} standalone")

PDF = "sources/omb/budget-2027-app-2-3-legislative.pdf"

def cong_pub():
    sa1 = "Single-source into 0900 Total new obligations (sole program activity)" + M2
    build(
        "omb/budget-appendix-fy2027-leg-gpo-congressional-publishing",
        {"path": PDF, "table": "004-0203-0-1-801", "page": 26,
         "title": "Government Publishing Office - Congressional Publishing (Program and Financing)",
         "period": "FY 2027"},
        "USD millions. GPO Congressional Publishing account (id 004-0203-0-1-801), Program and Financing schedule, PDF page 26 (printed page 38) left column. The account has no separate Object Classification or Employment Summary schedule; the 0900 row label carries '(object class 24.0)' inline. Blank (dotted-leader) cells not transcribed per convention (blank != zero): 3041 prints only in col 1. Negatives as printed (3020, 3041). Single-source chains (0001->0900, 1100->1930, 4000->4180, 4020->4190, memo 3100/3200) are standalone under schema minItems 2.",
        [
            ("0001 Congressional Publishing", ["83", "80", "80"]),
            ("0900 Total new obligations, unexpired accounts (object class 24.0)", ["83", "80", "80"]),
            ("1100 Appropriation", ["83", "80", "80"]),
            ("1930 Total budgetary resources available", ["83", "80", "80"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["89", "92", "84"]),
            ("3010 New obligations, unexpired accounts", ["83", "80", "80"]),
            ("3020 Outlays (gross)", ["-70", "-88", "-86"]),
            ("3041 Recoveries of prior year unpaid obligations, expired", ["-10", None, None]),
            ("3050 Unpaid obligations, end of year", ["92", "84", "78"]),
            ("3100 Obligated balance, start of year", ["89", "92", "84"]),
            ("3200 Obligated balance, end of year", ["92", "84", "78"]),
            ("4000 Budget authority, gross", ["83", "80", "80"]),
            ("4010 Outlays from new discretionary authority", ["49", "57", "57"]),
            ("4011 Outlays from discretionary balances", ["21", "31", "29"]),
            ("4020 Outlays, gross (total)", ["70", "88", "86"]),
            ("4180 Budget authority, net (total)", ["83", "80", "80"]),
            ("4190 Outlays, net (total)", ["70", "88", "86"]),
        ],
        [
            ("3050", ["3000", "3010", "3020", "3041"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
        ],
        {
            ("0001", 1): sa1, ("0001", 2): sa1, ("0001", 3): sa1,
            ("0900", 1): "Single-source total new obligations (equals sole program activity 0001)" + M2,
            ("0900", 2): "Single-source total new obligations (equals sole program activity 0001)" + M2,
            ("0900", 3): "Single-source total new obligations (equals sole program activity 0001)" + M2,
            ("1100", 1): "Single-source into 1930 Total budgetary resources (no other budgetary resources)" + M2,
            ("1100", 2): "Single-source into 1930 Total budgetary resources (no other budgetary resources)" + M2,
            ("1100", 3): "Single-source into 1930 Total budgetary resources (no other budgetary resources)" + M2,
            ("1930", 1): "Single-source total budgetary resources (equals 1100 appropriation)" + M2,
            ("1930", 2): "Single-source total budgetary resources (equals 1100 appropriation)" + M2,
            ("1930", 3): "Single-source total budgetary resources (equals 1100 appropriation)" + M2,
            ("3100", 1): MEMO + "; equals 3000 (no uncollected payments in this account)",
            ("3100", 2): MEMO + "; equals 3000 (no uncollected payments in this account)",
            ("3100", 3): MEMO + "; equals 3000 (no uncollected payments in this account)",
            ("3200", 1): MEMO + "; equals 3050 (no uncollected payments in this account)",
            ("3200", 2): MEMO + "; equals 3050 (no uncollected payments in this account)",
            ("3200", 3): MEMO + "; equals 3050 (no uncollected payments in this account)",
            ("4000", 1): "Restates 1100/1930 as gross discretionary budget authority; single-source" + M2,
            ("4000", 2): "Restates 1100/1930 as gross discretionary budget authority; single-source" + M2,
            ("4000", 3): "Restates 1100/1930 as gross discretionary budget authority; single-source" + M2,
            ("4180", 1): "Single-source net total = gross (no offsets, no mandatory amounts)" + M2,
            ("4180", 2): "Single-source net total = gross (no offsets, no mandatory amounts)" + M2,
            ("4180", 3): "Single-source net total = gross (no offsets, no mandatory amounts)" + M2,
            ("4190", 1): "Single-source outlays net = gross (4190 = 4020, no offsets)" + M2,
            ("4190", 2): "Single-source outlays net = gross (4190 = 4020, no offsets)" + M2,
            ("4190", 3): "Single-source outlays net = gross (4190 = 4020, no offsets)" + M2,
        },
        (49, 6, 27),
    )

def pip():
    build(
        "omb/budget-appendix-fy2027-leg-gpo-public-information",
        {"path": PDF, "table": "004-0201-0-1-808", "page": 26,
         "title": "GPO - Public Information Programs of the Superintendent of Documents, Salaries and Expenses (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). GPO Public Information Programs of the Superintendent of Documents - Salaries and Expenses (id 004-0201-0-1-808): Program and Financing on PDF page 26 (printed page 38) right column; Object Classification + Employment Summary on PDF page 27 (printed page 39) left column. No blank cells. Negatives as printed (3020). Single-source chains (1100->1930, 4000->4180, 4020->4190, memo 3100/3200) are standalone under schema minItems 2.",
        [
            ("0001 Depository Library Distribution", ["26", "30", "30"]),
            ("0002 Cataloging and Indexing", ["10", "12", "12"]),
            ("0003 International Exchange", ["1", "1", "1"]),
            ("0900 Total new obligations, unexpired accounts", ["37", "43", "43"]),
            ("1100 Appropriation", ["37", "43", "43"]),
            ("1930 Total budgetary resources available", ["37", "43", "43"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["17", "22", "23"]),
            ("3010 New obligations, unexpired accounts", ["37", "43", "43"]),
            ("3020 Outlays (gross)", ["-32", "-42", "-43"]),
            ("3050 Unpaid obligations, end of year", ["22", "23", "23"]),
            ("3100 Obligated balance, start of year", ["17", "22", "23"]),
            ("3200 Obligated balance, end of year", ["22", "23", "23"]),
            ("4000 Budget authority, gross", ["37", "43", "43"]),
            ("4010 Outlays from new discretionary authority", ["27", "34", "34"]),
            ("4011 Outlays from discretionary balances", ["5", "8", "9"]),
            ("4020 Outlays, gross (total)", ["32", "42", "43"]),
            ("4180 Budget authority, net (total)", ["37", "43", "43"]),
            ("4190 Outlays, net (total)", ["32", "42", "43"]),
            ("11.1 Personnel compensation: Full-time permanent", ["13", "14", "14"]),
            ("12.1 Civilian personnel benefits", ["5", "5", "5"]),
            ("22.0 Transportation of things", ["1", "1", "1"]),
            ("24.0 Printing and reproduction", ["4", "6", "6"]),
            ("25.2 Other services from non-Federal sources", ["14", "17", "17"]),
            ("99.9 Total new obligations, unexpired accounts", ["37", "43", "43"]),
            ("1001 Direct civilian full-time equivalent employment", ["81", "81", "93"]),
        ],
        [
            ("0900", ["0001", "0002", "0003"], [1, 2, 3]),
            ("3050", ["3000", "3010", "3020"], [1, 2, 3]),
            ("4020", ["4010", "4011"], [1, 2, 3]),
            ("99.9", ["11.1", "12.1", "22.0", "24.0", "25.2"], [1, 2, 3]),
        ],
        {
            **{("1100", c): "Single-source into 1930 Total budgetary resources (no other budgetary resources)" + M2 for c in (1, 2, 3)},
            **{("1930", c): "Single-source total budgetary resources (equals 1100 appropriation)" + M2 for c in (1, 2, 3)},
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("4000", c): "Restates 1100/1930 as gross discretionary budget authority; single-source" + M2 for c in (1, 2, 3)},
            **{("4180", c): "Single-source net total = gross (no offsets, no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = gross (4190 = 4020, no offsets)" + M2 for c in (1, 2, 3)},
            **{("1001", c): "Employment Summary line (full-time equivalent employment, a headcount, not USD millions); participates in no arithmetic on this schedule" for c in (1, 2, 3)},
        },
        (75, 12, 24),
    )

def bizops_pf():
    build(
        "omb/budget-appendix-fy2027-leg-gpo-business-operations-pf",
        {"path": PDF, "table": "004-4505-0-4-808", "page": 27,
         "title": "GPO - Business Operations Revolving Fund (Program and Financing)",
         "period": "FY 2027"},
        "USD millions. GPO Business Operations Revolving Fund (id 004-4505-0-4-808), Program and Financing schedule, PDF page 27 (printed page 39) right column. Unit 1 of the 2-unit by-schedule split of this 152-cell account (sibling: -gpo-business-operations-objclass), following the GAO 005-0107 by-schedule precedent; each schedule prints its own 004-4505 header. Revolving fund: mandatory offsetting-collections spending authority (1800/1801/1850), uncollected-payments tracking (3060/3070/3090), and a mandatory net section (4090-4170). Row 4160 Budget authority, net (mandatory) prints dotted-leader blank in ALL three columns (4090+4130+4140 nets to zero, zero-suppressed) and is omitted per convention (blank != zero) - consequently 4090/4140 feed no encodable relation and 4180 is single-source. Blank cells: 1012 col 1 only, 4010 blank col 1, 4123 blank col 1. Negatives as printed (1801 c1, 3020, 3060, 3090, 4120, 4123, 4130, 4140 c2/c3, 3070 c2/c3). 1930 sums 1000+1900 directly in c2/c3 (1070 single-source there) per family precedent. Obligated-balance memo lines 3100/3200 are genuine sums (uncollected payments present). Cross-schedule sanity (not encoded; sibling re-reads independently): 0900 = 99.9 (1302/1294/1294).",
        [
            ("0801 Business Operations", ["1276", "1268", "1268"]),
            ("0811 Capital investment", ["26", "26", "26"]),
            ("0900 Total new obligations, unexpired accounts", ["1302", "1294", "1294"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["372", "404", "319"]),
            ("1012 Unobligated balance transfers between expired and unexpired accounts", ["10", None, None]),
            ("1070 Unobligated balance (total)", ["382", "404", "319"]),
            ("1100 Appropriation", ["12", "9", "9"]),
            ("1800 Collected", ["1343", "1179", "1179"]),
            ("1801 Change in uncollected payments, Federal sources", ["-31", "21", "21"]),
            ("1850 Spending auth from offsetting collections, mand (total)", ["1312", "1200", "1200"]),
            ("1900 Budget authority (total)", ["1324", "1209", "1209"]),
            ("1930 Total budgetary resources available", ["1706", "1613", "1528"]),
            ("1941 Unexpired unobligated balance, end of year", ["404", "319", "234"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["692", "580", "655"]),
            ("3010 New obligations, unexpired accounts", ["1302", "1294", "1294"]),
            ("3020 Outlays (gross)", ["-1414", "-1219", "-1241"]),
            ("3050 Unpaid obligations, end of year", ["580", "655", "708"]),
            ("3060 Uncollected pymts, Fed sources, brought forward, Oct 1", ["-244", "-213", "-234"]),
            ("3070 Change in uncollected pymts, Fed sources, unexpired", ["31", "-21", "-21"]),
            ("3090 Uncollected pymts, Fed sources, end of year", ["-213", "-234", "-255"]),
            ("3100 Obligated balance, start of year", ["448", "367", "421"]),
            ("3200 Obligated balance, end of year", ["367", "421", "453"]),
            ("4000 Budget authority, gross", ["12", "9", "9"]),
            ("4010 Outlays from new discretionary authority", [None, "4", "4"]),
            ("4011 Outlays from discretionary balances", ["14", "23", "19"]),
            ("4020 Outlays, gross (total)", ["14", "27", "23"]),
            ("4090 Budget authority, gross", ["1312", "1200", "1200"]),
            ("4100 Outlays from new mandatory authority", ["1028", "960", "960"]),
            ("4101 Outlays from mandatory balances", ["372", "232", "258"]),
            ("4110 Outlays, gross (total)", ["1400", "1192", "1218"]),
            ("4120 Federal sources", ["-1343", "-1155", "-1155"]),
            ("4123 Non-Federal sources", [None, "-24", "-24"]),
            ("4130 Offsets against gross budget authority and outlays (total)", ["-1343", "-1179", "-1179"]),
            ("4140 Change in uncollected pymts, Fed sources, unexpired", ["31", "-21", "-21"]),
            ("4170 Outlays, net (mandatory)", ["57", "13", "39"]),
            ("4180 Budget authority, net (total)", ["12", "9", "9"]),
            ("4190 Outlays, net (total)", ["71", "40", "62"]),
        ],
        [
            ("0900", ["0801", "0811"], [1, 2, 3]),
            ("1070", ["1000", "1012"], [1]),
            ("1850", ["1800", "1801"], [1, 2, 3]),
            ("1900", ["1100", "1850"], [1, 2, 3]),
            ("1930", ["1070", "1900"], [1]),
            ("1930", ["1000", "1900"], [2, 3]),
            ("3050", ["3000", "3010", "3020"], [1, 2, 3]),
            ("3090", ["3060", "3070"], [1, 2, 3]),
            ("3100", ["3000", "3060"], [1, 2, 3]),
            ("3200", ["3050", "3090"], [1, 2, 3]),
            ("4020", ["4010", "4011"], [2, 3]),
            ("4110", ["4100", "4101"], [1, 2, 3]),
            ("4130", ["4120", "4123"], [2, 3]),
            ("4170", ["4110", "4130"], [1, 2, 3]),
            ("4190", ["4020", "4170"], [1, 2, 3]),
        ],
        {
            ("1070", 2): "Single-source unobligated balance total (equals 1000 brought-forward; 1012 transfers blank this column)" + M2 + ". 1930 this column sums 1000+1900 directly per family precedent",
            ("1070", 3): "Single-source unobligated balance total (equals 1000 brought-forward; 1012 transfers blank this column)" + M2 + ". 1930 this column sums 1000+1900 directly per family precedent",
            **{("1941", c): "Memorandum (non-add) entry: Unexpired unobligated balance end of year does not feed the section arithmetic" for c in (1, 2, 3)},
            **{("4000", c): "Restates 1100 as gross discretionary budget authority; single-source into 4180 (4160 mandatory net prints blank/zero-suppressed)" + M2 for c in (1, 2, 3)},
            ("4011", 1): "Single-source into 4020 Outlays gross (4010 blank this column)" + M2,
            **{("4090", c): "Restates 1850 as gross mandatory budget authority; feeds only 4160 Budget authority net (mandatory), which prints blank (zero-suppressed) in all columns, so no encodable relation exists" for c in (1, 2, 3)},
            ("4120", 1): "Single-source into 4130 offsets total (4123 non-Federal blank this column)" + M2,
            **{("4140", c): "Feeds only 4160 Budget authority net (mandatory), which prints blank (zero-suppressed) in all columns, so no encodable relation exists" for c in (1, 2, 3)},
            **{("4180", c): "Single-source net total = 4000 gross discretionary (4160 mandatory net prints blank/zero-suppressed)" + M2 for c in (1, 2, 3)},
        },
        (107, 38, 19),
    )

def bizops_oc():
    build(
        "omb/budget-appendix-fy2027-leg-gpo-business-operations-objclass",
        {"path": PDF, "table": "004-4505-0-4-808", "page": 28,
         "title": "GPO - Business Operations Revolving Fund (Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). GPO Business Operations Revolving Fund (id 004-4505-0-4-808), Object Classification + Employment Summary schedules, PDF page 28 (printed page 40) LEFT column - the right column of this two-column page is the separate GAO account 005-0107 (do not cross-contaminate). Unit 2 of the 2-unit by-schedule split of this 152-cell account (sibling: -gpo-business-operations-pf); each schedule prints its own 004-4505 header. All obligations are reimbursable (revolving fund): 99.0 Reimbursable obligations sums 11.9 Total personnel compensation plus the non-personnel line items; 99.9 equals 99.0 single-source (no direct obligations) and is standalone under schema minItems 2. No blank cells. Cross-schedule sanity (not encoded; sibling re-reads independently): 99.9 = 0900 (1302/1294/1294).",
        [
            ("11.1 Full-time permanent", ["189", "189", "189"]),
            ("11.5 Other personnel compensation", ["3", "3", "3"]),
            ("11.9 Total personnel compensation", ["192", "192", "192"]),
            ("12.1 Civilian personnel benefits", ["84", "84", "84"]),
            ("21.0 Travel and transportation of persons", ["1", "1", "1"]),
            ("22.0 Transportation of things", ["16", "16", "16"]),
            ("23.2 Rental payments to others", ["5", "5", "5"]),
            ("23.3 Communications, utilities, and miscellaneous charges", ["15", "15", "15"]),
            ("24.0 Printing and reproduction", ["460", "452", "452"]),
            ("25.2 Other services from non-Federal sources", ["95", "95", "95"]),
            ("26.0 Supplies and materials", ["408", "408", "408"]),
            ("31.0 Equipment", ["26", "26", "26"]),
            ("99.0 Reimbursable obligations", ["1302", "1294", "1294"]),
            ("99.9 Total new obligations, unexpired accounts", ["1302", "1294", "1294"]),
            ("2001 Reimbursable civilian full-time equivalent employment", ["1553", "1553", "1600"]),
        ],
        [
            ("11.9", ["11.1", "11.5"], [1, 2, 3]),
            ("99.0", ["11.9", "12.1", "21.0", "22.0", "23.2", "23.3", "24.0", "25.2", "26.0", "31.0"], [1, 2, 3]),
        ],
        {
            **{("99.9", c): "Single-source total new obligations (equals 99.0 Reimbursable; no direct obligations in this revolving fund)" + M2 for c in (1, 2, 3)},
            **{("2001", c): "Employment Summary line (full-time equivalent employment, a headcount, not USD millions); participates in no arithmetic on this schedule" for c in (1, 2, 3)},
        },
        (45, 6, 6),
    )

UNITS = {"cong-pub": cong_pub, "pip": pip, "bizops-pf": bizops_pf, "bizops-oc": bizops_oc}
UNITS[sys.argv[1]]()
