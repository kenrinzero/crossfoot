# Build omb/budget-appendix-fy2027-leg-gao-salaries-pf.cells.json
# GAO Salaries and Expenses (005-0107-0-1-801), Program and Financing schedule.
# Source: sources/omb/budget-2027-app-2-3-legislative.pdf, PDF p28 (printed 40)
# right column, continuing to PDF p29 (printed 41) LEFT column top.
# Values read from the staged renders gao-p28-render.png / gao-p29-render.png,
# cross-checked against the text layer (gao-p28-text.txt / gao-p29-text.txt).
import json
from decimal import Decimal

# (code+label, [c1, c2, c3])  None = blank (dotted leader) as printed
ROWS = [
    ("0001 GOAL 1-Address Current and Emerging Challenges to the Well-being and Financial Security of the American People", ["298", "293", "311"]),
    ("0002 GOAL 2-Respond to Changing Security Threats and the Challenges of Global Interdependence", ["223", "219", "231"]),
    ("0003 GOAL 3-Help Transform the Federal Government to Address National Challenges", ["198", "195", "207"]),
    ("0004 GOAL 4-Maximize the Value of GAO by Enabling Quality, Timely Service to the Congress, and by Being a Leading Practices Federal Agency", ["17", "17", "18"]),
    ("0005 GOAL 8-Other Costs in Support of the Congress", ["89", "88", "93"]),
    ("0799 Total direct obligations", ["825", "812", "860"]),
    ("0801 Reimbursable program activity goal 1", ["1", "1", "1"]),
    ("0803 Reimbursable program activity goal 3", ["97", "87", "47"]),
    ("0805 Reimbursable program activity goal 8", ["3", "3", "2"]),
    ("0809 Reimbursable program activities, subtotal", ["101", "91", "50"]),
    ("0899 Total reimbursable obligations", ["101", "91", "50"]),
    ("0900 Total new obligations, unexpired accounts", ["926", "903", "910"]),
    ("1000 Unobligated balance brought forward, Oct 1", ["156", "100", "37"]),
    ("1001 Discretionary unobligated balance brought fwd, Oct 1", ["135", "86", None]),
    ("1021 Recoveries of prior year unpaid obligations", ["1", None, None]),
    ("1033 Recoveries of prior year paid obligations", ["15", None, None]),
    ("1070 Unobligated balance (total)", ["172", "100", "37"]),
    ("1100 Appropriation", ["822", "812", "860"]),
    ("1700 Collected", ["35", "28", "28"]),
    ("1701 Change in uncollected payments, Federal sources", ["-3", None, None]),
    ("1750 Spending auth from offsetting collections, disc (total)", ["32", "28", "28"]),
    ("1900 Budget authority (total)", ["854", "840", "888"]),
    ("1930 Total budgetary resources available", ["1026", "940", "925"]),
    ("1941 Unexpired unobligated balance, end of year", ["100", "37", "15"]),
    ("3000 Unpaid obligations, brought forward, Oct 1", ["140", "138", "128"]),
    ("3010 New obligations, unexpired accounts", ["926", "903", "910"]),
    ("3011 Obligations (\"upward adjustments\"), expired accounts", ["18", None, None]),
    ("3020 Outlays (gross)", ["-928", "-913", "-898"]),
    ("3040 Recoveries of prior year unpaid obligations, unexpired", ["-1", None, None]),
    ("3041 Recoveries of prior year unpaid obligations, expired", ["-17", None, None]),
    ("3050 Unpaid obligations, end of year", ["138", "128", "140"]),
    ("3060 Uncollected pymts, Fed sources, brought forward, Oct 1", ["-20", "-17", "-17"]),
    ("3070 Change in uncollected pymts, Fed sources, unexpired", ["3", None, None]),
    ("3090 Uncollected pymts, Fed sources, end of year", ["-17", "-17", "-17"]),
    ("3100 Obligated balance, start of year", ["120", "121", "111"]),
    ("3200 Obligated balance, end of year", ["121", "111", "123"]),
    ("4000 Budget authority, gross", ["854", "840", "888"]),
    ("4010 Outlays from new discretionary authority", ["746", "831", "878"]),
    ("4011 Outlays from discretionary balances", ["174", "82", "20"]),
    ("4020 Outlays, gross (total)", ["920", "913", "898"]),
    ("4030 Federal sources", ["-34", "-28", "-28"]),
    ("4033 Non-Federal sources", ["-21", None, None]),
    ("4040 Offsets against gross budget authority and outlays (total)", ["-55", "-28", "-28"]),
    ("4050 Change in uncollected pymts, Fed sources, unexpired", ["3", None, None]),
    ("4052 Offsetting collections credited to expired accounts", ["5", None, None]),
    ("4053 Recoveries of prior year paid obligations, unexpired accounts", ["15", None, None]),
    ("4060 Additional offsets against budget authority only (total)", ["23", None, None]),
    ("4070 Budget authority, net (discretionary)", ["822", "812", "860"]),
    ("4080 Outlays, net (discretionary)", ["865", "885", "870"]),
    ("4101 Outlays from mandatory balances", ["8", None, None]),
    ("4180 Budget authority, net (total)", ["822", "812", "860"]),
    ("4190 Outlays, net (total)", ["873", "885", "870"]),
]

CODE = {label.split()[0]: i + 1 for i, (label, _) in enumerate(ROWS)}

# Relations: (target_code, [source_codes], [columns])
RELATIONS = [
    ("0799", ["0001", "0002", "0003", "0004", "0005"], [1, 2, 3]),
    ("0809", ["0801", "0803", "0805"], [1, 2, 3]),
    ("0900", ["0799", "0899"], [1, 2, 3]),
    ("1070", ["1000", "1021", "1033"], [1]),
    ("1750", ["1700", "1701"], [1]),
    ("1900", ["1100", "1750"], [1, 2, 3]),
    ("1930", ["1070", "1900"], [1]),
    ("1930", ["1000", "1900"], [2, 3]),  # 1070 single-source in c2/c3; family precedent (#86 tax-court-salaries)
    ("3050", ["3000", "3010", "3011", "3020", "3040", "3041"], [1]),
    ("3050", ["3000", "3010", "3020"], [2, 3]),
    ("3090", ["3060", "3070"], [1]),
    ("3100", ["3000", "3060"], [1, 2, 3]),
    ("3200", ["3050", "3090"], [1, 2, 3]),
    ("4020", ["4010", "4011"], [1, 2, 3]),
    ("4040", ["4030", "4033"], [1]),
    ("4060", ["4050", "4052", "4053"], [1]),
    ("4070", ["4000", "4040", "4060"], [1]),
    ("4070", ["4000", "4040"], [2, 3]),
    ("4080", ["4020", "4040"], [1, 2, 3]),
    ("4190", ["4080", "4101"], [1]),
]

STANDALONE = {
    ("1001", 1): "Memorandum (non-add): discretionary subset of the 1000 unobligated balance, does not feed the section arithmetic (do not add into 1070)",
    ("1001", 2): "Memorandum (non-add): discretionary subset of the 1000 unobligated balance, does not feed the section arithmetic (do not add into 1070)",
    ("1070", 2): "Single-source unobligated balance total (equals 1000 brought-forward; 1021/1033 recoveries blank this column); schema minItems 2 forbids single-source sum. 1930 this column sums 1000+1900 directly per family precedent",
    ("1070", 3): "Single-source unobligated balance total (equals 1000 brought-forward; 1021/1033 recoveries blank this column); schema minItems 2 forbids single-source sum. 1930 this column sums 1000+1900 directly per family precedent",
    ("1700", 2): "Single-source into 1750 Spending auth from offsetting collections (1701 change blank this column); schema minItems 2 forbids single-source sum",
    ("1700", 3): "Single-source into 1750 Spending auth from offsetting collections (1701 change blank this column); schema minItems 2 forbids single-source sum",
    ("1941", 1): "Memorandum (non-add) entry: Unexpired unobligated balance end of year does not feed the section arithmetic",
    ("1941", 2): "Memorandum (non-add) entry: Unexpired unobligated balance end of year does not feed the section arithmetic",
    ("1941", 3): "Memorandum (non-add) entry: Unexpired unobligated balance end of year does not feed the section arithmetic",
    ("4030", 2): "Single-source into 4040 offsets total (4033 non-Federal blank this column); schema minItems 2 forbids single-source sum",
    ("4030", 3): "Single-source into 4040 offsets total (4033 non-Federal blank this column); schema minItems 2 forbids single-source sum",
    ("4180", 1): "Single-source net total = net discretionary (4180 = 4070, no mandatory budget authority); schema minItems 2 forbids single-source sum",
    ("4180", 2): "Single-source net total = net discretionary (4180 = 4070, no mandatory budget authority); schema minItems 2 forbids single-source sum",
    ("4180", 3): "Single-source net total = net discretionary (4180 = 4070, no mandatory budget authority); schema minItems 2 forbids single-source sum",
    ("4190", 2): "Single-source outlays net total = net discretionary (4190 = 4080, 4101 mandatory outlays blank this column); schema minItems 2 forbids single-source sum",
    ("4190", 3): "Single-source outlays net total = net discretionary (4190 = 4080, 4101 mandatory outlays blank this column); schema minItems 2 forbids single-source sum",
}

def cid(code, col):
    return f"r{CODE[code]}c{col}"

VALUES = {}
for i, (label, vals) in enumerate(ROWS):
    code = label.split()[0]
    for col, v in enumerate(vals, 1):
        if v is not None:
            VALUES[(code, col)] = v

# roles: start standalone/leaf, promote targets to total
targets = set()
sources = set()
for tgt, srcs, cols in RELATIONS:
    for col in cols:
        assert (tgt, col) in VALUES, f"target {tgt} c{col} missing"
        total = Decimal(0)
        for s in srcs:
            assert (s, col) in VALUES, f"source {s} c{col} missing (rel -> {tgt})"
            total += Decimal(VALUES[(s, col)])
            sources.add((s, col))
        assert total == Decimal(VALUES[(tgt, col)]), \
            f"{tgt} c{col}: sum {total} != printed {VALUES[(tgt, col)]}"
        targets.add((tgt, col))

cells = []
n_standalone = 0
for i, (label, vals) in enumerate(ROWS):
    code = label.split()[0]
    for col, v in enumerate(vals, 1):
        if v is None:
            continue
        key = (code, col)
        if key in targets:
            role = "total"
            cell = {"id": cid(code, col), "row": CODE[code], "col": col, "value": v, "role": role}
        elif key in STANDALONE:
            assert key not in sources, f"{key} standalone but used as source"
            role = "standalone"
            cell = {"id": cid(code, col), "row": CODE[code], "col": col, "value": v,
                    "role": role, "why": STANDALONE[key]}
            n_standalone += 1
        else:
            assert key in sources, f"{key} is neither target, source, nor waived standalone"
            role = "leaf"
            cell = {"id": cid(code, col), "row": CODE[code], "col": col, "value": v, "role": role}
        cells.append(cell)

assert len(cells) == 129, f"cell count {len(cells)} != 129"

relations = []
for tgt, srcs, cols in RELATIONS:
    for col in cols:
        relations.append({"type": "sum",
                          "sources": [cid(s, col) for s in srcs],
                          "target": cid(tgt, col)})
assert len(relations) == 39, f"relation count {len(relations)} != 39"

doc = {
    "table_id": "omb/budget-appendix-fy2027-leg-gao-salaries-pf",
    "source": {
        "path": "sources/omb/budget-2027-app-2-3-legislative.pdf",
        "table": "005-0107-0-1-801",
        "page": 28,
        "title": "Government Accountability Office - Salaries and Expenses (Program and Financing)",
        "period": "FY 2027"
    },
    "unit_note": "USD millions. GAO Salaries and Expenses account (id 005-0107-0-1-801), Program and Financing schedule: PDF page 28 (printed page 40) right column, continuing onto PDF page 29 (printed page 41) LEFT column (4030 through 4190; the right column of page 29 is the separate US Tax Court account 023-0100). Unit 1 of the 2-unit by-schedule split of this 195-cell account (sibling: -gao-salaries-objclass); each schedule prints its own 005-0107 header, so no cross-unit re-anchoring is needed. Has offsetting-collections spending authority (1700/1701/1750), uncollected-payments tracking (3060/3070/3090), and net offsets incl. non-Federal sources and expired-account credits (4030/4033/4050/4052/4053/4060) - same machinery as Capitol Police General Expenses (002-0476). Blank (dotted-leader) cells not transcribed per convention (blank != zero); most recovery/adjustment/offset detail lines print only in col 1 (2025 actual). Negatives as printed (1701, 3020, 3040, 3041, 3060, 3090, 4030, 4033, 4040). 1001 is a non-add memo subset of 1000 (never fed into 1070). Obligated-balance memo lines 3100/3200 are genuine sums (unpaid obligations + uncollected payments) because uncollected payments are present. Cross-schedule sanity (not encoded; sibling unit re-reads independently): 0900 = 99.9 (926/903/910), 0799 = 99.0 Direct (825/812/860), 0899 = 99.0 Reimbursable (101/91/50).",
    "columns": [
        {"index": 1, "label": "2025 actual"},
        {"index": 2, "label": "2026 est."},
        {"index": 3, "label": "2027 est."}
    ],
    "rows": [{"index": i + 1, "label": label} for i, (label, _) in enumerate(ROWS)],
    "cells": cells,
    "relations": relations
}

out = "tables/omb/budget-appendix-fy2027-leg-gao-salaries-pf.cells.json"
with open(out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"wrote {out}: {len(cells)} cells, {len(relations)} relations, {n_standalone} standalone")
