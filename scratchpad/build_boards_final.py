# Build the final Boards and Commissions units #105-114 (OMB FY2027
# Legislative Branch, PDF pp33-37 / printed 45-49). Values read from
# renders boards-p33..p37-render.png, cross-checked against text extracts.
# Run with: cecc | hdp | spf | semiq | coil | other | stennis | uscpc | openworld | gfra
import json, sys
from decimal import Decimal

M2 = "; schema minItems 2 forbids single-source sum"
MEMO = "Memorandum (non-add) entry: does not feed the section arithmetic"
FTE = ("Employment Summary line (full-time equivalent employment, a headcount, "
       "not USD millions); participates in no arithmetic on this schedule")
INV = ("Memorandum (non-add) investment entry (Federal securities par value); "
       "participates in no arithmetic on this schedule")
NO3050 = ("the 3050 Unpaid-obligations-end-of-year row is absent entirely (nets to "
          "zero in every column, zero-suppressed), so no encodable relation exists")

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

def cecc():
    build(
        "omb/budget-appendix-fy2027-leg-cecc-salaries-expenses",
        {"path": PDF, "table": "272-2930-0-1-801", "page": 33,
         "title": "Congressional-Executive Commission on the People's Republic of China - Salaries and Expenses (Program and Financing + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). Congressional-Executive Commission on the People's Republic of China (id 272-2930-0-1-801): P&F starts PDF page 33 (printed 45) bottom RIGHT column (0001/0900) and continues on PDF page 34 (printed 46) top left; Employment Summary p34 left. No separate ObjClass schedule - the 0900 label carries '(object class 11.1)' inline. The Change-in-obligated-balance section prints only 3010/3020 (they net to zero every column, so the 3050 end-of-year row is zero-suppressed out entirely) - 3010/3020 are standalone. Negatives as printed (3020).",
        [
            ("0001 Direct program activity", ["2", "2", "2"]),
            ("0900 Total new obligations, unexpired accounts (object class 11.1)", ["2", "2", "2"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["1", "1", "1"]),
            ("1100 Appropriation", ["2", "2", "2"]),
            ("1930 Total budgetary resources available", ["3", "3", "3"]),
            ("1941 Unexpired unobligated balance, end of year", ["1", "1", "1"]),
            ("3010 New obligations, unexpired accounts", ["2", "2", "2"]),
            ("3020 Outlays (gross)", ["-2", "-2", "-2"]),
            ("4000 Budget authority, gross", ["2", "2", "2"]),
            ("4010 Outlays from new discretionary authority", ["1", "2", "2"]),
            ("4011 Outlays from discretionary balances", ["1", None, None]),
            ("4020 Outlays, gross (total)", ["2", "2", "2"]),
            ("4180 Budget authority, net (total)", ["2", "2", "2"]),
            ("4190 Outlays, net (total)", ["2", "2", "2"]),
            ("1001 Direct civilian full-time equivalent employment", ["14", "14", "14"]),
        ],
        [
            ("1930", ["1000", "1100"], [1, 2, 3]),
            ("4020", ["4010", "4011"], [1]),
        ],
        {
            **{("0001", c): "Single-source into 0900 Total new obligations (sole program activity)" + M2 for c in (1, 2, 3)},
            **{("0900", c): "Single-source total new obligations (equals sole program activity 0001)" + M2 for c in (1, 2, 3)},
            **{("1941", c): MEMO for c in (1, 2, 3)},
            **{("3010", c): "New obligations: " + NO3050 for c in (1, 2, 3)},
            **{("3020", c): "Outlays: " + NO3050 for c in (1, 2, 3)},
            **{("4000", c): "Restates 1100 as gross discretionary budget authority; single-source into 4180" + M2 for c in (1, 2, 3)},
            ("4010", 2): "Single-source into 4020 Outlays gross (4011 blank this column)" + M2,
            ("4010", 3): "Single-source into 4020 Outlays gross (4011 blank this column)" + M2,
            ("4020", 2): "Single-source outlays gross total (equals 4010; 4011 blank this column); 4190 also single-source" + M2,
            ("4020", 3): "Single-source outlays gross total (equals 4010; 4011 blank this column); 4190 also single-source" + M2,
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = 4020 gross (no offsets)" + M2 for c in (1, 2, 3)},
            **{("1001", c): FTE for c in (1, 2, 3)},
        },
        (43, 4, 31),
    )

def hdp():
    build(
        "omb/budget-appendix-fy2027-leg-house-democracy-partnership",
        {"path": PDF, "table": "548-2851-0-1-801", "page": 34,
         "title": "House Democracy Partnership (Program and Financing + Object Classification)",
         "period": "FY 2027"},
        "USD millions. House Democracy Partnership (id 548-2851-0-1-801), PDF page 34 (printed 46) right column - a newly funded commission: the ENTIRE 2025-actual column is blank (no cells transcribed for c1; blank != zero). No 0900, 1000, 3050, 4011, or 4020 rows printed; no Employment Summary. 3010/3020 net to zero (2-2) so the 3050 row is zero-suppressed out entirely; 4190 outlays net equals 4010 single-source (no 4020 gross-total row exists). Only encodable identity: 99.9 = 21.0 + 25.2 in c2/c3. Negatives as printed (3020).",
        [
            ("0001 Direct program activity", [None, "2", "2"]),
            ("1100 Appropriation", [None, "2", "2"]),
            ("1930 Total budgetary resources available", [None, "2", "2"]),
            ("3010 New obligations, unexpired accounts", [None, "2", "2"]),
            ("3020 Outlays (gross)", [None, "-2", "-2"]),
            ("4000 Budget authority, gross", [None, "2", "2"]),
            ("4010 Outlays from new discretionary authority", [None, "2", "2"]),
            ("4180 Budget authority, net (total)", [None, "2", "2"]),
            ("4190 Outlays, net (total)", [None, "2", "2"]),
            ("21.0 Travel and transportation of persons", [None, "1", "1"]),
            ("25.2 Other services from non-Federal sources", [None, "1", "1"]),
            ("99.9 Total new obligations, unexpired accounts", [None, "2", "2"]),
        ],
        [
            ("99.9", ["21.0", "25.2"], [2, 3]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (2, 3)},
            **{("1100", c): "Single-source into 1930 Total budgetary resources (no other budgetary resources)" + M2 for c in (2, 3)},
            **{("1930", c): "Single-source total budgetary resources (equals 1100 appropriation)" + M2 for c in (2, 3)},
            **{("3010", c): "New obligations: " + NO3050 for c in (2, 3)},
            **{("3020", c): "Outlays: " + NO3050 for c in (2, 3)},
            **{("4000", c): "Restates 1100 as gross discretionary budget authority; single-source into 4180" + M2 for c in (2, 3)},
            **{("4010", c): "Sole outlays line; no 4020 gross-total row printed, and 4190 net equals it single-source" + M2 for c in (2, 3)},
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (2, 3)},
            **{("4190", c): "Single-source outlays net = 4010 (no 4020 row, no offsets)" + M2 for c in (2, 3)},
        },
        (24, 2, 18),
    )

def spf():
    build(
        "omb/budget-appendix-fy2027-leg-senate-preservation-fund",
        {"path": PDF, "table": "000-5509-0-2-801", "page": 34,
         "title": "Senate Preservation Fund (Special and Trust Fund Receipts + Program and Financing)",
         "period": "FY 2027"},
        "USD millions. Senate Preservation Fund (id 000-5509-0-2-801), combined Special and Trust Fund Receipts + P&F: starts PDF page 34 (printed 46) bottom right, ends PDF page 35 (printed 47) top left (5000/5001 investment memos). Gift-funded account with NO obligations section at all (no 0900/3xxx rows). Receipts: 0100 and 5099 print blank (5099 = 4-4 nets to zero, zero-suppressed), so 1130/2000/2101 are standalone. P&F: 1010 is a NEGATIVE unobligated-balance transfer to account [001-0123] (c2 = -4); 1070 c2 = 1000 + 1010 = 5-4 = 1 is the account's only multi-source balance identity besides 1930 c1 = 1070 + 1101 = 1+4 = 5. 1001 is a non-add memo subset of 1000. 4190 prints blank in all columns.",
        [
            ("1130 Gifts, Senate Preservation Fund", ["4", None, None]),
            ("2000 Total: Balances and receipts", ["4", None, None]),
            ("2101 Senate Preservation Fund", ["-4", None, None]),
            ("1000 Unobligated balance brought forward, Oct 1", ["1", "5", "1"]),
            ("1001 Discretionary unobligated balance brought fwd, Oct 1", ["1", "4", None]),
            ("1010 Unobligated balance transfer to other accts [001-0123]", [None, "-4", None]),
            ("1070 Unobligated balance (total)", ["1", "1", "1"]),
            ("1101 Appropriation (special or trust)", ["4", None, None]),
            ("1930 Total budgetary resources available", ["5", "1", "1"]),
            ("1941 Unexpired unobligated balance, end of year", ["5", "1", "1"]),
            ("4000 Budget authority, gross", ["4", None, None]),
            ("4180 Budget authority, net (total)", ["4", None, None]),
            ("5000 Total investments, SOY: Federal securities: Par value", ["1", "1", "1"]),
            ("5001 Total investments, EOY: Federal securities: Par value", ["1", "1", "1"]),
        ],
        [
            ("1070", ["1000", "1010"], [2]),
            ("1930", ["1070", "1101"], [1]),
        ],
        {
            ("1130", 1): "Single-source into 2000 Total balances and receipts (0100 balance blank)" + M2,
            ("2000", 1): "Single-source total (equals 1130); feeds 5099 Balance end of year, which prints blank (4-4 nets to zero, zero-suppressed)" + M2,
            ("2101", 1): "Appropriation out of the fund; feeds 5099 Balance end of year, which prints blank (4-4 nets to zero, zero-suppressed)",
            ("1000", 1): "Single-source into 1070 Unobligated balance total (1010 transfer blank this column)" + M2,
            ("1000", 3): "Single-source into 1070 Unobligated balance total (1010 transfer blank this column)" + M2,
            ("1001", 1): "Memorandum (non-add): discretionary subset of the 1000 unobligated balance, does not feed the section arithmetic",
            ("1001", 2): "Memorandum (non-add): discretionary subset of the 1000 unobligated balance, does not feed the section arithmetic",
            ("1070", 3): "Single-source unobligated balance total (equals 1000; 1010 blank this column), and 1930 this column is also single-source" + M2,
            ("1930", 2): "Single-source total budgetary resources (equals 1070; 1101 appropriation blank this column)" + M2,
            ("1930", 3): "Single-source total budgetary resources (equals 1070; 1101 appropriation blank this column)" + M2,
            **{("1941", c): MEMO for c in (1, 2, 3)},
            ("4000", 1): "Restates 1101 as gross discretionary budget authority; single-source into 4180 (4190 prints blank all columns)" + M2,
            ("4180", 1): "Single-source net total = 4000 gross (no offsets)" + M2,
            **{("5000", c): INV for c in (1, 2, 3)},
            **{("5001", c): INV for c in (1, 2, 3)},
        },
        (27, 2, 21),
    )

def semiq():
    build(
        "omb/budget-appendix-fy2027-leg-semiquincentennial-commission",
        {"path": PDF, "table": "239-2780-0-1-801", "page": 35,
         "title": "United States Semiquincentennial Commission - Salaries and Expenses (Program and Financing + Object Classification + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). United States Semiquincentennial Commission (id 239-2780-0-1-801), complete on PDF page 35 (printed 47): P&F left column, ObjClass + Employment right column. No 0900 and no 1900 rows printed. 1001 is a non-add memo subset of 1000 (c1 only). 1930 = 1070 + 1100 in c1 and 1000 + 1100 in c2/c3 (1070 single-source there, family precedent). 3050 c1 is 4-source (includes 3040 recoveries). The Commission expires December 31, 2027 (close-out account). Negatives as printed (3020, 3040).",
        [
            ("0001 Direct program activity", ["18", "15", "30"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["3", "1", "1"]),
            ("1001 Discretionary unobligated balance brought fwd, Oct 1", ["3", None, None]),
            ("1021 Recoveries of prior year unpaid obligations", ["1", None, None]),
            ("1070 Unobligated balance (total)", ["4", "1", "1"]),
            ("1100 Appropriation", ["15", "15", "30"]),
            ("1930 Total budgetary resources available", ["19", "16", "31"]),
            ("1941 Unexpired unobligated balance, end of year", ["1", "1", "1"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["3", "3", "10"]),
            ("3010 New obligations, unexpired accounts", ["18", "15", "30"]),
            ("3020 Outlays (gross)", ["-17", "-8", "-19"]),
            ("3040 Recoveries of prior year unpaid obligations, unexpired", ["-1", None, None]),
            ("3050 Unpaid obligations, end of year", ["3", "10", "21"]),
            ("3100 Obligated balance, start of year", ["3", "3", "10"]),
            ("3200 Obligated balance, end of year", ["3", "10", "21"]),
            ("4000 Budget authority, gross", ["15", "15", "30"]),
            ("4010 Outlays from new discretionary authority", ["13", "8", "15"]),
            ("4011 Outlays from discretionary balances", ["4", None, "4"]),
            ("4020 Outlays, gross (total)", ["17", "8", "19"]),
            ("4180 Budget authority, net (total)", ["15", "15", "30"]),
            ("4190 Outlays, net (total)", ["17", "8", "19"]),
            ("11.1 Personnel compensation: Full-time permanent", ["1", "1", "1"]),
            ("25.1 Advisory and assistance services", ["1", "1", "2"]),
            ("25.2 Other services from non-Federal sources", ["16", "13", "27"]),
            ("99.9 Total new obligations, unexpired accounts", ["18", "15", "30"]),
            ("1001-fte|1001 Direct civilian full-time equivalent employment", ["7", "7", "7"]),
        ],
        [
            ("1070", ["1000", "1021"], [1]),
            ("1930", ["1070", "1100"], [1]),
            ("1930", ["1000", "1100"], [2, 3]),
            ("3050", ["3000", "3010", "3020", "3040"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [1, 3]),
            ("99.9", ["11.1", "25.1", "25.2"], [1, 2, 3]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            ("1001", 1): "Memorandum (non-add): discretionary subset of the 1000 unobligated balance, does not feed the section arithmetic (do not add into 1070)",
            ("1070", 2): "Single-source unobligated balance total (equals 1000; 1021 recoveries blank this column)" + M2 + ". 1930 this column sums 1000+1100 directly per family precedent",
            ("1070", 3): "Single-source unobligated balance total (equals 1000; 1021 recoveries blank this column)" + M2 + ". 1930 this column sums 1000+1100 directly per family precedent",
            **{("1941", c): MEMO for c in (1, 2, 3)},
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("4000", c): "Restates 1100 as gross discretionary budget authority; single-source into 4180" + M2 for c in (1, 2, 3)},
            ("4010", 2): "Single-source into 4020 Outlays gross (4011 blank this column)" + M2,
            ("4020", 2): "Single-source outlays gross total (equals 4010; 4011 blank this column); 4190 also single-source" + M2,
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = 4020 gross (no offsets)" + M2 for c in (1, 2, 3)},
            **{("1001-fte", c): FTE for c in (1, 2, 3)},
        },
        (71, 12, 29),
    )

def coil():
    build(
        "omb/budget-appendix-fy2027-leg-coil-fund",
        {"path": PDF, "table": "009-0145-0-1-154", "page": 35,
         "title": "Congressional Office for International Leadership Fund (Program and Financing + Object Classification)",
         "period": "FY 2027"},
        "USD millions. Congressional Office for International Leadership Fund (id 009-0145-0-1-154) - the general-fund payment account (the receiving trust fund is 009-8148, a separate unit): P&F starts PDF page 35 (printed 47) bottom right, continues PDF page 36 (printed 48) top left; ObjClass p36 left. No 0900 row; no Employment Summary; the 3050 end-of-year row is absent entirely (2+7-9 = 0 in c1, 6-6 and 7-7 = 0 in c2/c3, zero-suppressed), so 3000/3010/3020 are standalone. 94.0 Financial transfers is the dominant object class. Negatives as printed (3020).",
        [
            ("0001 Open World Leadership Center Trust Fund (Direct)", ["7", "6", "7"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["1", None, None]),
            ("1100 Appropriation", ["6", "6", "7"]),
            ("1900 Budget authority (total)", ["6", "6", "7"]),
            ("1930 Total budgetary resources available", ["7", "6", "7"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["2", None, None]),
            ("3010 New obligations, unexpired accounts", ["7", "6", "7"]),
            ("3020 Outlays (gross)", ["-9", "-6", "-7"]),
            ("3100 Obligated balance, start of year", ["2", None, None]),
            ("4000 Budget authority, gross", ["6", "6", "7"]),
            ("4010 Outlays from new discretionary authority", ["6", "6", "7"]),
            ("4011 Outlays from discretionary balances", ["3", None, None]),
            ("4020 Outlays, gross (total)", ["9", "6", "7"]),
            ("4180 Budget authority, net (total)", ["6", "6", "7"]),
            ("4190 Outlays, net (total)", ["9", "6", "7"]),
            ("25.1 Advisory and assistance services", ["1", None, None]),
            ("94.0 Financial transfers", ["6", "6", "7"]),
            ("99.9 Total new obligations, unexpired accounts", ["7", "6", "7"]),
        ],
        [
            ("1930", ["1000", "1900"], [1]),
            ("4020", ["4010", "4011"], [1]),
            ("99.9", ["25.1", "94.0"], [1]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            **{("1100", c): "Single-source into 1900 Budget authority total" + M2 for c in (1, 2, 3)},
            ("1900", 2): "Single-source into 1930 Total budgetary resources (1000 balance blank this column)" + M2,
            ("1900", 3): "Single-source into 1930 Total budgetary resources (1000 balance blank this column)" + M2,
            ("1930", 2): "Single-source total budgetary resources (equals 1900)" + M2,
            ("1930", 3): "Single-source total budgetary resources (equals 1900)" + M2,
            ("3000", 1): "Unpaid balance brought forward: " + NO3050 + " (c1: 2+7-9 = 0)",
            **{("3010", c): "New obligations: " + NO3050 for c in (1, 2, 3)},
            **{("3020", c): "Outlays: " + NO3050 for c in (1, 2, 3)},
            ("3100", 1): MEMO + "; equals 3000 (no uncollected payments in this account)",
            **{("4000", c): "Restates 1900 as gross discretionary budget authority; single-source into 4180" + M2 for c in (1, 2, 3)},
            ("4010", 2): "Single-source into 4020 Outlays gross (4011 blank this column)" + M2,
            ("4010", 3): "Single-source into 4020 Outlays gross (4011 blank this column)" + M2,
            ("4020", 2): "Single-source outlays gross total (equals 4010); 4190 also single-source" + M2,
            ("4020", 3): "Single-source outlays gross total (equals 4010); 4190 also single-source" + M2,
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = 4020 gross (no offsets)" + M2 for c in (1, 2, 3)},
            ("94.0", 2): "Single-source into 99.9 Total new obligations (25.1 blank this column)" + M2,
            ("94.0", 3): "Single-source into 99.9 Total new obligations (25.1 blank this column)" + M2,
            ("99.9", 2): "Single-source total new obligations (equals 94.0; 25.1 blank this column)" + M2,
            ("99.9", 3): "Single-source total new obligations (equals 94.0; 25.1 blank this column)" + M2,
        },
        (44, 3, 35),
    )

def other():
    build(
        "omb/budget-appendix-fy2027-leg-other-boards-commissions",
        {"path": PDF, "table": "009-9911-0-1-999", "page": 36,
         "title": "Other Legislative Branch Boards and Commissions (Program and Financing)",
         "period": "FY 2027"},
        "USD millions. Other Legislative Branch Boards and Commissions (id 009-9911-0-1-999), a consolidated presentation covering (per the printed narrative): International Conferences and Contingencies; House and Senate Expenses; Western Hemisphere Drug Policy Commission; Women's Suffrage Centennial Commission; and the Oliver Wendell Holmes Devise Fund. P&F starts PDF page 36 (printed 48) bottom left, continues top right (3100/3200 memos; 4180/4190 print blank in all columns). ZERO relations: every printed equality is single-source under schema minItems 2 (same class as OCWR #93 and Capitol Police Security Enhancements #91) - no Outlays row prints at all (3050 carries forward via 3000/3010 alone), and the 0900 label carries '(object class 25.1)' inline.",
        [
            ("0001 Direct program activity", ["1", None, None]),
            ("0900 Total new obligations, unexpired accounts (object class 25.1)", ["1", None, None]),
            ("1000 Unobligated balance brought forward, Oct 1", ["1", None, None]),
            ("1930 Total budgetary resources available", ["1", None, None]),
            ("3000 Unpaid obligations, brought forward, Oct 1", [None, "1", "1"]),
            ("3010 New obligations, unexpired accounts", ["1", None, None]),
            ("3050 Unpaid obligations, end of year", ["1", "1", "1"]),
            ("3100 Obligated balance, start of year", [None, "1", "1"]),
            ("3200 Obligated balance, end of year", ["1", "1", "1"]),
        ],
        [],
        {
            ("0001", 1): "Single-source into 0900 Total new obligations (sole program activity)" + M2,
            ("0900", 1): "Single-source total new obligations (equals sole program activity 0001)" + M2,
            ("1000", 1): "Single-source into 1930 Total budgetary resources" + M2,
            ("1930", 1): "Single-source total budgetary resources (equals 1000; no budget authority rows print)" + M2,
            ("3000", 2): "Single-source into 3050 Unpaid obligations end of year (no outlays row prints; 3010 blank this column)" + M2,
            ("3000", 3): "Single-source into 3050 Unpaid obligations end of year (no outlays row prints; 3010 blank this column)" + M2,
            ("3010", 1): "Single-source into 3050 Unpaid obligations end of year (no outlays row prints; 3000 blank this column)" + M2,
            ("3050", 1): "Single-source unpaid obligations end of year (equals 3010; 3000 blank, no outlays row)" + M2,
            ("3050", 2): "Single-source unpaid obligations end of year (equals 3000; 3010 blank, no outlays row)" + M2,
            ("3050", 3): "Single-source unpaid obligations end of year (equals 3000; 3010 blank, no outlays row)" + M2,
            ("3100", 2): MEMO + "; equals 3000 (no uncollected payments in this account)",
            ("3100", 3): MEMO + "; equals 3000 (no uncollected payments in this account)",
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
        },
        (15, 0, 15),
    )

def stennis():
    build(
        "omb/budget-appendix-fy2027-leg-stennis-center",
        {"path": PDF, "table": "009-8275-0-7-801", "page": 36,
         "title": "John C. Stennis Center for Public Service Training and Development (Special and Trust Fund Receipts + Program and Financing + Employment Summary)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). John C. Stennis Center for Public Service Training and Development trust fund (id 009-8275-0-7-801), combined Receipts + P&F: PDF page 36 (printed 48) right column, Employment Summary on PDF page 37 (printed 49) top left (single printed cell, 5 FTE in 2026 est. only). TWO receipt rows share the printed code 1140 (Payments / Interest Received) and are distinct rows here; 0198 Reconciliation adjustment prints blank all columns (omitted), so 0199 balance equals 0100 single-source. P&F: 0900 label carries '(object class 25.2)' inline; 3010/3020 net to zero every column (3050 row absent, zero-suppressed); the mandatory net section is all single-source (4090=1900 restated, 4180=4090, 4190=4100). 5000/5001 investment memos carry the 18 par-value corpus. Negatives as printed (2101, 3020).",
        [
            ("0100 Balance, start of year", ["8", "8", "9"]),
            ("0199 Balance, start of year", ["8", "8", "9"]),
            ("1140a|1140 Payments, John C. Stennis Center for Public Service Training and Development", ["1", "1", "1"]),
            ("1140b|1140 Interest Received by Trust Fund, J. C. Stennis Center", ["1", "1", "1"]),
            ("1199 Total current law receipts", ["2", "2", "2"]),
            ("1999 Total receipts", ["2", "2", "2"]),
            ("2000 Total: Balances and receipts", ["10", "10", "11"]),
            ("2101 John C. Stennis Center for Public Service Training and Development", ["-2", "-1", "-1"]),
            ("5099 Balance, end of year", ["8", "9", "10"]),
            ("0001 John C. Stennis Center for Public Service Training and Development (Direct)", ["2", "1", "1"]),
            ("0900 Total new obligations, unexpired accounts (object class 25.2)", ["2", "1", "1"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["11", "11", "11"]),
            ("1201 Appropriation (special or trust fund)", ["2", "1", "1"]),
            ("1900 Budget authority (total)", ["2", "1", "1"]),
            ("1930 Total budgetary resources available", ["13", "12", "12"]),
            ("1941 Unexpired unobligated balance, end of year", ["11", "11", "11"]),
            ("3010 New obligations, unexpired accounts", ["2", "1", "1"]),
            ("3020 Outlays (gross)", ["-2", "-1", "-1"]),
            ("4090 Budget authority, gross", ["2", "1", "1"]),
            ("4100 Outlays from new mandatory authority", ["2", "1", "1"]),
            ("4180 Budget authority, net (total)", ["2", "1", "1"]),
            ("4190 Outlays, net (total)", ["2", "1", "1"]),
            ("5000 Total investments, SOY: Federal securities: Par value", ["18", "18", "18"]),
            ("5001 Total investments, EOY: Federal securities: Par value", ["18", "18", "18"]),
            ("1001 Direct civilian full-time equivalent employment", [None, "5", None]),
        ],
        [
            ("1199", ["1140a", "1140b"], [1, 2, 3]),
            ("2000", ["0199", "1999"], [1, 2, 3]),
            ("5099", ["2000", "2101"], [1, 2, 3]),
            ("1930", ["1000", "1900"], [1, 2, 3]),
        ],
        {
            **{("0100", c): "Single-source into 0199 Balance start of year (0198 reconciliation adjustment blank all columns)" + M2 for c in (1, 2, 3)},
            **{("0001", c): "Single-source into 0900 Total new obligations (sole program activity)" + M2 for c in (1, 2, 3)},
            **{("0900", c): "Single-source total new obligations (equals sole program activity 0001)" + M2 for c in (1, 2, 3)},
            **{("1201", c): "Single-source into 1900 Budget authority total (no other budget authority)" + M2 for c in (1, 2, 3)},
            **{("1941", c): MEMO for c in (1, 2, 3)},
            **{("3010", c): "New obligations: " + NO3050 for c in (1, 2, 3)},
            **{("3020", c): "Outlays: " + NO3050 for c in (1, 2, 3)},
            **{("4090", c): "Restates 1900 as gross mandatory budget authority; single-source into 4180" + M2 for c in (1, 2, 3)},
            **{("4100", c): "Sole outlays line; no 4110 gross-total row printed, and 4190 net equals it single-source" + M2 for c in (1, 2, 3)},
            **{("4180", c): "Single-source net total = 4090 gross (no offsets)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = 4100 (no 4110 row, no offsets)" + M2 for c in (1, 2, 3)},
            **{("5000", c): INV for c in (1, 2, 3)},
            **{("5001", c): INV for c in (1, 2, 3)},
            ("1001", 2): FTE,
        },
        (73, 12, 40),
    )

def uscpc():
    build(
        "omb/budget-appendix-fy2027-leg-capitol-preservation-commission",
        {"path": PDF, "table": "009-8300-0-7-801", "page": 37,
         "title": "U.S. Capitol Preservation Commission (Special and Trust Fund Receipts + Program and Financing)",
         "period": "FY 2027"},
        "USD millions. U.S. Capitol Preservation Commission trust fund (id 009-8300-0-7-801), combined Receipts + P&F, PDF page 37 (printed 49) left column. Dormant fund: no obligations section at all (no 0900/3xxx rows), receipts only in 2025 actual. 0100 and 5099 print blank (5099 = 1-1 nets to zero, zero-suppressed) so 1140/2000/2101 are standalone; the only multi-source identity is 1930 c1 = 1000 + 1900 = 12+1 = 13. 4190 prints blank in all columns. 5000/5001 investment memos carry the 12/13 par-value corpus. Negatives as printed (2101).",
        [
            ("1140 Interest on Investments, U.S. Capitol Preservation Commission", ["1", None, None]),
            ("2000 Total: Balances and receipts", ["1", None, None]),
            ("2101 U.S. Capitol Preservation Commission", ["-1", None, None]),
            ("1000 Unobligated balance brought forward, Oct 1", ["12", "13", "13"]),
            ("1201 Appropriation (special or trust fund)", ["1", None, None]),
            ("1900 Budget authority (total)", ["1", None, None]),
            ("1930 Total budgetary resources available", ["13", "13", "13"]),
            ("1941 Unexpired unobligated balance, end of year", ["13", "13", "13"]),
            ("4090 Budget authority, gross", ["1", None, None]),
            ("4180 Budget authority, net (total)", ["1", None, None]),
            ("5000 Total investments, SOY: Federal securities: Par value", ["12", "13", "13"]),
            ("5001 Total investments, EOY: Federal securities: Par value", ["13", "13", "13"]),
        ],
        [
            ("1930", ["1000", "1900"], [1]),
        ],
        {
            ("1140", 1): "Single-source into 2000 Total balances and receipts (0100 balance blank)" + M2,
            ("2000", 1): "Single-source total (equals 1140); feeds 5099 Balance end of year, which prints blank (1-1 nets to zero, zero-suppressed)" + M2,
            ("2101", 1): "Appropriation out of the fund; feeds 5099 Balance end of year, which prints blank (1-1 nets to zero, zero-suppressed)",
            ("1000", 2): "Single-source into 1930 Total budgetary resources (no budget authority this column)" + M2,
            ("1000", 3): "Single-source into 1930 Total budgetary resources (no budget authority this column)" + M2,
            ("1201", 1): "Single-source into 1900 Budget authority total (no other budget authority)" + M2,
            ("1930", 2): "Single-source total budgetary resources (equals 1000)" + M2,
            ("1930", 3): "Single-source total budgetary resources (equals 1000)" + M2,
            **{("1941", c): MEMO for c in (1, 2, 3)},
            ("4090", 1): "Restates 1900 as gross mandatory budget authority; single-source into 4180 (4190 prints blank all columns)" + M2,
            ("4180", 1): "Single-source net total = 4090 gross (no offsets)" + M2,
            **{("5000", c): INV for c in (1, 2, 3)},
            **{("5001", c): INV for c in (1, 2, 3)},
        },
        (22, 1, 19),
    )

def openworld():
    build(
        "omb/budget-appendix-fy2027-leg-open-world-trust-fund",
        {"path": PDF, "table": "009-8148-0-7-154", "page": 37,
         "title": "Open World Leadership Center Trust Fund / International Leadership Fund (Program and Financing + Object Classification + Employment Summary + Special and Trust Fund Receipts)",
         "period": "FY 2027"},
        "USD millions except the Employment Summary FTE line (headcount). Open World Leadership Center Trust Fund (id 009-8148-0-7-154), PDF page 37 (printed 49) right column plus the 'International Leadership Fund' Special and Trust Fund Receipts schedule (bottom left) which carries the SAME id and joins this unit per the combined-schedule precedent (LoC -gift-trust, Tax Court). The paying general-fund account is 009-0145 (separate unit -coil-fund). No 0900 row. Receipts: 0100/5099 print blank (6-6 nets to zero, zero-suppressed) so 1140/2000/2101 are standalone. 99.5 'Adjustment for rounding' prints c1/c2 and 99.9 = 99.0 + 99.5 sums EXACTLY there (7/6); 99.9 c3 is single-source (99.5 blank). 3050 c1 is 4-source (includes 3040 recoveries). Negatives as printed (3020, 3040, 2101).",
        [
            ("0001 Open World Leadership Center Trust Fund (Direct)", ["7", "6", "7"]),
            ("1000 Unobligated balance brought forward, Oct 1", ["1", "1", "1"]),
            ("1021 Recoveries of prior year unpaid obligations", ["1", None, None]),
            ("1070 Unobligated balance (total)", ["2", "1", "1"]),
            ("1101 Appropriation (special or trust)", ["6", "6", "7"]),
            ("1930 Total budgetary resources available", ["8", "7", "8"]),
            ("1941 Unexpired unobligated balance, end of year", ["1", "1", "1"]),
            ("3000 Unpaid obligations, brought forward, Oct 1", ["3", "3", "1"]),
            ("3010 New obligations, unexpired accounts", ["7", "6", "7"]),
            ("3020 Outlays (gross)", ["-6", "-8", "-7"]),
            ("3040 Recoveries of prior year unpaid obligations, unexpired", ["-1", None, None]),
            ("3050 Unpaid obligations, end of year", ["3", "1", "1"]),
            ("3100 Obligated balance, start of year", ["3", "3", "1"]),
            ("3200 Obligated balance, end of year", ["3", "1", "1"]),
            ("4000 Budget authority, gross", ["6", "6", "7"]),
            ("4010 Outlays from new discretionary authority", ["6", "5", "6"]),
            ("4011 Outlays from discretionary balances", [None, "3", "1"]),
            ("4020 Outlays, gross (total)", ["6", "8", "7"]),
            ("4180 Budget authority, net (total)", ["6", "6", "7"]),
            ("4190 Outlays, net (total)", ["6", "8", "7"]),
            ("5000 Total investments, SOY: Federal securities: Par value", ["3", "3", "3"]),
            ("5001 Total investments, EOY: Federal securities: Par value", ["3", "3", "3"]),
            ("11.1 Personnel compensation: Full-time permanent", ["1", "1", "1"]),
            ("25.1 Advisory and assistance services", [None, "1", "2"]),
            ("25.3 Other goods and services from Federal sources", ["1", "1", "2"]),
            ("41.0 Grants, subsidies, and contributions", ["3", "2", "2"]),
            ("99.0 Direct obligations", ["5", "5", "7"]),
            ("99.5 Adjustment for rounding", ["2", "1", None]),
            ("99.9 Total new obligations, unexpired accounts", ["7", "6", "7"]),
            ("1001 Direct civilian full-time equivalent employment", ["8", "8", "9"]),
            ("1140 Payment from the General Fund, Open World Leadership Center Trust Fund", ["6", "6", "7"]),
            ("2000 Total: Balances and receipts", ["6", "6", "7"]),
            ("2101 International Leadership Fund", ["-6", "-6", "-7"]),
        ],
        [
            ("1070", ["1000", "1021"], [1]),
            ("1930", ["1070", "1101"], [1]),
            ("1930", ["1000", "1101"], [2, 3]),
            ("3050", ["3000", "3010", "3020", "3040"], [1]),
            ("3050", ["3000", "3010", "3020"], [2, 3]),
            ("4020", ["4010", "4011"], [2, 3]),
            ("99.0", ["11.1", "25.3", "41.0"], [1]),
            ("99.0", ["11.1", "25.1", "25.3", "41.0"], [2, 3]),
            ("99.9", ["99.0", "99.5"], [1, 2]),
        ],
        {
            **{("0001", c): "Sole program activity; this account prints no 0900 row, so it feeds nothing" + M2 for c in (1, 2, 3)},
            ("1070", 2): "Single-source unobligated balance total (equals 1000; 1021 blank this column)" + M2 + ". 1930 this column sums 1000+1101 directly per family precedent",
            ("1070", 3): "Single-source unobligated balance total (equals 1000; 1021 blank this column)" + M2 + ". 1930 this column sums 1000+1101 directly per family precedent",
            **{("1941", c): MEMO for c in (1, 2, 3)},
            **{("3100", c): MEMO + "; equals 3000 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("3200", c): MEMO + "; equals 3050 (no uncollected payments in this account)" for c in (1, 2, 3)},
            **{("4000", c): "Restates 1101 as gross discretionary budget authority; single-source into 4180" + M2 for c in (1, 2, 3)},
            ("4010", 1): "Single-source into 4020 Outlays gross (4011 blank this column)" + M2,
            ("4020", 1): "Single-source outlays gross total (equals 4010; 4011 blank this column); 4190 also single-source" + M2,
            **{("4180", c): "Single-source net total = 4000 gross (no offsets, no mandatory amounts)" + M2 for c in (1, 2, 3)},
            **{("4190", c): "Single-source outlays net = 4020 gross (no offsets)" + M2 for c in (1, 2, 3)},
            **{("5000", c): INV for c in (1, 2, 3)},
            **{("5001", c): INV for c in (1, 2, 3)},
            ("99.9", 3): "Single-source total new obligations (equals 99.0; 99.5 rounding adjustment blank this column)" + M2,
            **{("1001", c): FTE for c in (1, 2, 3)},
            **{("1140", c): "Single-source into 2000 Total balances and receipts (0100 balance blank)" + M2 for c in (1, 2, 3)},
            **{("2000", c): "Single-source total (equals 1140); feeds 5099 Balance end of year, which prints blank (payment minus appropriation nets to zero, zero-suppressed)" + M2 for c in (1, 2, 3)},
            **{("2101", c): "Appropriation out of the fund; feeds 5099 Balance end of year, which prints blank (nets to zero, zero-suppressed)" for c in (1, 2, 3)},
        },
        (92, 14, 44),
    )

def gfra():
    build(
        "omb/budget-appendix-fy2027-leg-general-fund-receipts",
        {"path": PDF, "table": "general-fund-receipt-accounts", "page": 37,
         "title": "Legislative Branch - General Fund Receipt Accounts",
         "period": "FY 2027"},
        "USD millions. The Legislative Branch chapter's closing GENERAL FUND RECEIPT ACCOUNTS table, PDF page 37 (printed 49) bottom right - a two-row offsetting-receipts listing with no identification-code header (the account row carries its own code 001-322000). The total row equals the sole detail row single-source under schema minItems 2, so both cells are standalone. 2026/2027 print blank (omitted per blank != zero). This closes the chapter's transcribable content: pp38-40 are General Provisions (pure legal text, out of scope).",
        [
            ("001-322000 All Other General Fund Proprietary Receipts Including Budget Clearing Accounts", ["1", None, None]),
            ("total|General Fund Offsetting receipts from the public", ["1", None, None]),
        ],
        [],
        {
            ("001-322000", 1): "Single-source into the General Fund offsetting-receipts total (sole detail row)" + M2,
            ("total", 1): "Single-source total (equals the sole detail row 001-322000)" + M2,
        },
        (2, 0, 2),
    )

UNITS = {"cecc": cecc, "hdp": hdp, "spf": spf, "semiq": semiq, "coil": coil,
         "other": other, "stennis": stennis, "uscpc": uscpc,
         "openworld": openworld, "gfra": gfra}
UNITS[sys.argv[1]]()
