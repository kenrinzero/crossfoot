"""Builder for the FEC cross-page capstone: per-state TOTAL VOTES re-anchor.

Values RE-ANCHORED from the PDF (never copied from the block units), then
machine-checked for byte equality against the committed block-1..5 files
(0 mismatches allowed, Table-5 -departmental pattern).

Per-state identities verified 2026-07-17 (Kimi): for every one of the 51
jurisdictions, Σ(populated candidate cells across pp2-6) == TOTAL VOTES,
0 mismatches. National identity: Σ(26 candidate national totals) ==
155,238,302 — exact.
"""
import json
import pdfplumber
from decimal import Decimal
from pathlib import Path

PDF = "sources/fec/2024presgeresults.pdf"
STATES = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID",
          "IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO",
          "MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA",
          "RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]

# (page_idx, bands, [column names in order]) — pages 1..5 (0 = electoral)
PAGES = [
    (1, [215, 320, 405, 505], ["AYYADURAI", "BOWMAN", "DE LA CRUZ", "DUNCAN", "EBKE"]),
    (2, [195, 260, 336, 418, 500], ["EVERYLOVE", "FRUIT", "GARRITY", "HARRIS", "HUBER", "KENNEDY"]),
    (3, [178, 260, 342, 425, 510], ["KISHORE", "OLIVER", "PRESTON", "SKOUSEN", "SONSKI", "STEIN"]),
    (4, [199, 300, 392, 490], ["STODDEN", "SUPREME", "TERRY", "TRUMP", "WELLS"]),
    (5, [170, 240, 360, 480], ["WEST", "WOOD", "NONE OF THESE CANDIDATES", "WRITE-IN VOTES (SCATTERED)", "TOTAL VOTES"]),
]
CANDIDATES = [c for _, _, cols in PAGES for c in cols if c != "TOTAL VOTES"]
assert len(CANDIDATES) == 26

# ---- re-anchor from the PDF ----
cells = {}        # (state, candidate) -> value string (no commas)
nat_totals = {}   # candidate -> national total
total_votes = {}  # state -> TOTAL VOTES
nat_tv = None
pdf = pdfplumber.open(PDF)
for pidx, bands, cols in PAGES:
    p = pdf.pages[pidx]
    words = [w for w in p.extract_words() if w["top"] > 95]
    words.sort(key=lambda w: (w["top"], w["x0"]))
    lines, cur, last = [], [], None
    for w in words:
        if last is None or abs(w["top"] - last) <= 4:
            cur.append(w)
        else:
            lines.append(cur); cur = [w]
        last = w["top"]
    lines.append(cur)
    for ws in lines:
        ws.sort(key=lambda w: w["x0"])
        label = ws[0]["text"]
        vals = [None] * (len(bands) + 1)
        for w in ws[1:]:
            t = w["text"]
            if t.replace(",", "").replace(".", "").replace("%", "").isdigit():
                xc = (w["x0"] + w["x1"]) / 2
                b = 0
                while b < len(bands) and xc >= bands[b]:
                    b += 1
                vals[b] = t
        if label == "Total:":
            for ci, name in enumerate(cols):
                if name == "TOTAL VOTES":
                    nat_tv = vals[ci].replace(",", "")
                elif vals[ci]:
                    nat_totals[name] = vals[ci].replace(",", "")
            continue
        if not (len(label) == 2 and label.isupper()):
            continue
        for ci, name in enumerate(cols):
            v = vals[ci]
            if v is None:
                continue
            if name == "TOTAL VOTES":
                total_votes[label] = v.replace(",", "")
            else:
                cells[(label, name)] = v.replace(",", "")

# ---- proofs ----
for st in STATES:
    s = sum(Decimal(cells[(st, c)]) for c in CANDIDATES if (st, c) in cells)
    assert s == Decimal(total_votes[st]), (st, s, total_votes[st])
assert sum(Decimal(v) for v in nat_totals.values()) == Decimal(nat_tv)
print("51 per-state identities + national identity: ALL EXACT (re-anchored)")

# ---- consistency vs committed block units (0 mismatches required) ----
mismatches = 0
checked = 0
for bf in sorted(Path("tables/fec").glob("2024-presidential-general-popular-block-*.cells.json")):
    unit = json.loads(bf.read_text(encoding="utf-8"))
    colmap = {c["index"]: c["label"] for c in unit["columns"]}
    rowmap = {r["index"]: r["label"] for r in unit["rows"]}
    for cell in unit["cells"]:
        lab_c, lab_r = colmap[cell["col"]], rowmap[cell["row"]]
        if lab_r == "Total:":
            ref = nat_totals.get(lab_c) or (nat_tv if lab_c == "TOTAL VOTES" else None)
        elif lab_r.startswith("Percentage"):
            continue
        else:
            ref = total_votes.get(lab_r) if lab_c == "TOTAL VOTES" else cells.get((lab_r, lab_c))
        if ref is None:
            continue
        checked += 1
        if ref != cell["value"]:
            mismatches += 1
            print("MISMATCH", bf.name, lab_r, lab_c, ref, "!=", cell["value"])
print(f"consistency vs block units: {checked} overlapping cells checked, {mismatches} mismatches")
assert mismatches == 0

# ---- split states into sub-units at the <=140 ceiling ----
def state_cell_count(st):
    return sum(1 for c in CANDIDATES if (st, c) in cells) + 1  # + TOTAL VOTES

groups, cur, cur_n = [], [], 0
NATIONAL_ROW_CELLS = len(CANDIDATES) + 1  # candidate totals + national TOTAL VOTES
for st in STATES:
    n = state_cell_count(st)
    if cur and cur_n + n + (NATIONAL_ROW_CELLS if st == STATES[-1] else 0) > 138 and len(groups) < 4:
        groups.append(cur); cur, cur_n = [], 0
    cur.append(st); cur_n += n
groups.append(cur)
print("sub-unit split:", [(g[0] + "…" + g[-1], sum(state_cell_count(s) for s in g)) for g in groups],
      "+ national row", NATIONAL_ROW_CELLS, "in last")
SUFFIXES = "abcde"

def build(idx, group, with_national):
    sfx = SUFFIXES[idx]
    lines = []
    add = lines.append
    add("{")
    add(f'  "table_id": "fec/2024-presidential-general-popular-capstone-{sfx}",')
    add('  "source": {')
    add('    "path": "sources/fec/2024presgeresults.pdf",')
    add(f'    "table": "OFFICIAL 2024 PRESIDENTIAL GENERAL ELECTION RESULTS — pages 2–6, cross-page per-state TOTAL VOTES re-anchor capstone, part {sfx} ({group[0]}–{group[-1]}{" + national Total row" if with_national else ""})",')
    add('    "title": "FEC official 2024 presidential general election results — per-state TOTAL VOTES cross-page capstone",')
    add('    "period": "General Election Date: 11/05/2024 (source: State Elections Offices)"')
    add("  },")
    add('  "unit_note": "Cross-page capstone (Table-5 -departmental re-anchor pattern): every candidate cell and TOTAL VOTES cell re-read from the PDF — never copied from the block units — then machine-checked byte-for-byte against the committed block-1..5 units (0 mismatches). Each per-state relation sums the jurisdiction\'s populated candidate cells across all popular-vote blocks into its TOTAL VOTES cell (blank = not printed = no cell, per family convention).' + (' The national Total row closes the family: the 26 candidate national totals sum to the printed national TOTAL VOTES 155,238,302.' if with_national else '') + '",')
    add('  "columns": [')
    ncols = CANDIDATES + ["TOTAL VOTES"]
    for j, name in enumerate(ncols, 1):
        comma = "," if j < len(ncols) else ""
        add(f'    {{ "index": {j}, "label": "{name}" }}{comma}')
    add("  ],")
    add('  "rows": [')
    row_lines = [f'    {{ "index": {i}, "label": "{st}" }}' for i, st in enumerate(group, 1)]
    if with_national:
        row_lines.append(f'    {{ "index": {len(group)+1}, "label": "Total:" }}')
    add(",\n".join(row_lines))
    add("  ],")
    add('  "cells": [')
    cell_lines = []
    TV = len(ncols)
    for i, st in enumerate(group, 1):
        for j, name in enumerate(CANDIDATES, 1):
            v = cells.get((st, name))
            if v is not None:
                cell_lines.append(f'    {{ "id": "r{i}c{j}", "row": {i}, "col": {j}, "value": "{v}", "role": "leaf" }}')
        cell_lines.append(f'    {{ "id": "r{i}c{TV}", "row": {i}, "col": {TV}, "value": "{total_votes[st]}", "role": "total" }}')
    if with_national:
        nr = len(group) + 1
        for j, name in enumerate(CANDIDATES, 1):
            cell_lines.append(f'    {{ "id": "r{nr}c{j}", "row": {nr}, "col": {j}, "value": "{nat_totals[name]}", "role": "leaf" }}')
        cell_lines.append(f'    {{ "id": "r{nr}c{TV}", "row": {nr}, "col": {TV}, "value": "{nat_tv}", "role": "total" }}')
    add(",\n".join(cell_lines))
    add("  ],")
    rel_lines = []
    for i, st in enumerate(group, 1):
        srcs = [f'"r{i}c{j}"' for j, name in enumerate(CANDIDATES, 1) if (st, name) in cells]
        rel_lines.append(f'    {{ "type": "sum", "sources": [{", ".join(srcs)}], "target": "r{i}c{TV}", "note": "all populated candidate cells for {st} across the popular-vote blocks sum to its printed TOTAL VOTES" }}')
    if with_national:
        nr = len(group) + 1
        srcs = [f'"r{nr}c{j}"' for j in range(1, len(CANDIDATES) + 1)]
        rel_lines.append(f'    {{ "type": "sum", "sources": [{", ".join(srcs)}], "target": "r{nr}c{TV}", "note": "the 26 candidate national totals sum to the printed national TOTAL VOTES 155,238,302" }}')
    add('  "relations": [')
    add(",\n".join(rel_lines))
    add("  ]")
    add("}")
    out = Path(f"tables/fec/2024-presidential-general-popular-capstone-{sfx}.cells.json")
    text = "\n".join(lines) + "\n"
    out.write_text(text, encoding="utf-8", newline="\n")
    json.loads(text)
    print(f"wrote {out} — {len(cell_lines)} cells, {len(rel_lines)} relations")

for idx, group in enumerate(groups):
    build(idx, group, with_national=(idx == len(groups) - 1))
