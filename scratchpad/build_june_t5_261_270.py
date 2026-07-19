#!/usr/bin/env python3
"""Build June MTS Table 5 units #261–270 (Agriculture → Energy)."""
from __future__ import annotations

import json
import re
from decimal import Decimal
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "sources/treasury-mts/mts-202606.pdf"
OUT = ROOT / "tables/treasury-mts"

COLS = [
    {"index": 1, "label": "This Month / Gross Outlays"},
    {"index": 2, "label": "This Month / Applicable Receipts"},
    {"index": 3, "label": "This Month / Outlays"},
    {"index": 4, "label": "Current FYTD / Gross Outlays"},
    {"index": 5, "label": "Current FYTD / Applicable Receipts"},
    {"index": 6, "label": "Current FYTD / Outlays"},
    {"index": 7, "label": "Prior FYTD / Gross Outlays"},
    {"index": 8, "label": "Prior FYTD / Applicable Receipts"},
    {"index": 9, "label": "Prior FYTD / Outlays"},
]

ROUNDING_WHY = (
    'Table 5 footnote prints: "Note: Details may not add to totals due to '
    'rounding." Components are independently rounded to $ millions.'
)
STANDALONE_WHY = (
    "Single-source or omission-sparse column; not multi-source sum eligible "
    "under schema minItems:2."
)
TOKEN = re.compile(r"\.\.\.\.\.\.|\(\*\*\)|-?[\d,]+")


def parse_nums(text: str):
    toks = TOKEN.findall(text)
    if len(toks) < 9:
        return None
    toks = toks[-9:]
    out = []
    for t in toks:
        if t in ("......", "(**)"):
            out.append(None)
        else:
            out.append(Decimal(t.replace(",", "")))
    return out


def extract_rows(page_from: int = 10, page_to: int = 13):
    pdf = pdfplumber.open(PDF)
    raw: list[str] = []
    for pn in range(page_from, page_to + 1):
        t = pdf.pages[pn - 1].extract_text() or ""
        for line in t.splitlines():
            s = line.rstrip()
            if not s or s.strip().isdigit():
                continue
            if s.startswith(
                (
                    "Table 5",
                    "[$ millions]",
                    "This Month",
                    "Classification",
                    "Outlays Receipts",
                )
            ):
                continue
            raw.append(s)

    merged: list[tuple[str, list[Decimal | None] | None]] = []
    i = 0
    while i < len(raw):
        line = raw[i]
        if line.rstrip().endswith(":") or "Continued" in line:
            merged.append((line.strip().rstrip(":"), None))
            i += 1
            continue
        nums = parse_nums(line)
        if nums is None and i + 1 < len(raw):
            combined = line.rstrip() + " " + raw[i + 1].lstrip()
            nums2 = parse_nums(combined)
            if nums2 is not None:
                alltoks = list(TOKEN.finditer(combined))
                start = alltoks[-9].start()
                label = combined[:start].strip()
                merged.append((label, nums2))
                i += 2
                continue
        if nums is None:
            merged.append((line.strip(), None))
            i += 1
            continue
        alltoks = list(TOKEN.finditer(line))
        start = alltoks[-9].start()
        label = line[:start].strip()
        merged.append((label, nums))
        i += 1
    return merged


def val_str(v: Decimal) -> str:
    if v == v.to_integral_value():
        return str(int(v))
    return format(v, "f")


def build_unit(
    table_id: str,
    title: str,
    page: int,
    unit_note: str,
    row_specs: list[tuple[str, list[Decimal | None]]],
    total_rows: set[int] | None = None,
    rollups: list[tuple[int, list[int]]] | None = None,
):
    total_rows = total_rows or set()
    rollups = rollups or []

    # Drop rows that are entirely omitted
    filtered = []
    for lab, vals in row_specs:
        if all(v is None for v in vals):
            continue
        filtered.append((lab, vals))
    row_specs = filtered

    rows = [{"index": i + 1, "label": lab} for i, (lab, _) in enumerate(row_specs)]
    cell_map: dict[tuple[int, int], Decimal] = {}
    for ri, (lab, vals) in enumerate(row_specs, start=1):
        for ci, v in enumerate(vals, start=1):
            if v is None:
                continue
            cell_map[(ri, ci)] = v

    relations = []

    # Net identities: Gross = Outlays(net) + Applicable (May pattern: gross is total target)
    for ri in range(1, len(row_specs) + 1):
        for g, a, n in ((1, 2, 3), (4, 5, 6), (7, 8, 9)):
            if (ri, g) not in cell_map or (ri, n) not in cell_map:
                continue
            if (ri, a) not in cell_map:
                continue
            sources = [f"r{ri}c{n}", f"r{ri}c{a}"]
            target = f"r{ri}c{g}"
            actual = cell_map[(ri, g)]
            recomputed = cell_map[(ri, n)] + cell_map[(ri, a)]
            delta = abs(actual - recomputed)
            rel = {
                "type": "sum",
                "sources": sources,
                "target": target,
                "note": "net identity: Outlays(net)+Applicable=Gross",
            }
            if delta != 0:
                rel["tol"] = val_str(delta)
                rel["why"] = ROUNDING_WHY
            relations.append(rel)

    # Explicit roll-ups
    for target_ri, source_ris in rollups:
        for ci in range(1, 10):
            if (target_ri, ci) not in cell_map:
                continue
            srcs = [f"r{s}c{ci}" for s in source_ris if (s, ci) in cell_map]
            if len(srcs) < 2:
                continue
            actual = cell_map[(target_ri, ci)]
            recomputed = sum(
                cell_map[(s, ci)] for s in source_ris if (s, ci) in cell_map
            )
            delta = abs(actual - recomputed)
            rel = {
                "type": "sum",
                "sources": srcs,
                "target": f"r{target_ri}c{ci}",
                "note": f"section roll-up col {ci}",
            }
            if delta != 0:
                rel["tol"] = val_str(delta)
                rel["why"] = ROUNDING_WHY
            relations.append(rel)

    # Role assignment from relation graph (DESIGN §4):
    # target → total; source → leaf; neither → standalone.
    targets = {rel["target"] for rel in relations}
    sources_used: set[str] = set()
    for rel in relations:
        sources_used.update(rel["sources"])

    cells = []
    for (ri, ci), v in sorted(cell_map.items()):
        cid = f"r{ri}c{ci}"
        if cid in targets:
            role = "total"
            cell = {
                "id": cid,
                "row": ri,
                "col": ci,
                "value": val_str(v),
                "role": role,
            }
        elif cid in sources_used:
            role = "leaf"
            cell = {
                "id": cid,
                "row": ri,
                "col": ci,
                "value": val_str(v),
                "role": role,
            }
        else:
            cell = {
                "id": cid,
                "row": ri,
                "col": ci,
                "value": val_str(v),
                "role": "standalone",
                "why": STANDALONE_WHY,
            }
        cells.append(cell)

    doc = {
        "table_id": table_id,
        "source": {
            "path": "sources/treasury-mts/mts-202606.pdf",
            "table": f"Table 5. Outlays — {title}",
            "page": page,
            "title": title,
            "period": "June FY2026",
        },
        "unit_note": unit_note,
        "columns": COLS,
        "rows": rows,
        "cells": cells,
        "relations": relations,
    }
    path = OUT / f"{table_id.split('/', 1)[1]}.cells.json"
    path.write_text(json.dumps(doc, indent=2) + "\n")
    print(
        f"wrote {path.name}: cells={len(cells)} rels={len(relations)} "
        f"sa={sum(1 for c in cells if c['role']=='standalone')} rows={len(rows)}"
    )
    return path


def V(merged, idx):
    lab, nums = merged[idx]
    assert nums is not None, f"no data at {idx}: {lab}"
    return nums


def main():
    m = extract_rows(10, 13)

    # --- #261 agriculture-programs ---
    # Skip all-omitted Agricultural Disaster Relief Fund (38)
    specs = [
        ("Agricultural Research Service", V(m, 24)),
        (
            "National Institute of Food and Agriculture: Research and Education Activities",
            V(m, 26),
        ),
        (
            "National Institute of Food and Agriculture: Extension Activities",
            V(m, 27),
        ),
        ("National Institute of Food and Agriculture: Other", V(m, 28)),
        ("Animal and Plant Health Inspection Service", V(m, 29)),
        ("Food Safety and Inspection Service", V(m, 30)),
        ("Agricultural Marketing Service", V(m, 31)),
        (
            "Risk Management Agency: Administrative and Operating Expenses",
            V(m, 33),
        ),
        (
            "Risk Management Agency: Federal Crop Insurance Corporation Fund",
            V(m, 34),
        ),
        ("Farm Service Agency: Salaries and Expenses", V(m, 36)),
        ("Farm Service Agency: USDA Supplemental Assistance", V(m, 37)),
        ("Farm Service Agency: Commodity Credit Corporation", V(m, 39)),
        ("Farm Service Agency: Tobacco Trust Fund", V(m, 40)),
        ("Farm Service Agency: Agricultural Credit Insurance Fund", V(m, 41)),
        ("Farm Service Agency: Other", V(m, 42)),
        ("Total--Farm Service Agency", V(m, 43)),
        (
            "Natural Resources Conservation Service: Conservation Operations",
            V(m, 45),
        ),
        (
            "Natural Resources Conservation Service: Farm Security and Rural Investment Programs",
            V(m, 46),
        ),
        ("Natural Resources Conservation Service: Other", V(m, 47)),
    ]
    # FSA components 10-15 → total 16
    build_unit(
        "treasury-mts/2026-06-outlays-agriculture-programs",
        "Department of Agriculture (programs)",
        10,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 1/3 of Agriculture. All-omitted Agricultural Disaster Relief Fund row skipped.",
        specs,
        total_rows={16},
        rollups=[(16, [10, 11, 12, 13, 14, 15])],
    )

    # --- #262 agriculture-fns ---
    specs = [
        ("Rural Development", V(m, 48)),
        ("Rural Housing Service: Rural Housing Insurance Fund", V(m, 50)),
        ("Rural Housing Service: Rental Assistance Program", V(m, 51)),
        ("Rural Housing Service: Other", V(m, 52)),
        (
            "Rural Utilities Service: Rural Electrification and Telecommunications Fund",
            V(m, 54),
        ),
        ("Rural Utilities Service: Other", V(m, 55)),
        ("Foreign Agricultural Service", V(m, 56)),
        (
            "Food and Nutrition Service: Supplemental Nutrition Assistance Program",
            V(m, 58),
        ),
        ("Food and Nutrition Service: Child Nutrition Programs", V(m, 59)),
        (
            "Food and Nutrition Service: Special Supplemental Nutrition Program for Women, Infants, and Children (WIC)",
            V(m, 60),
        ),
        ("Food and Nutrition Service: Other", V(m, 61)),
        ("Total--Food and Nutrition Service", V(m, 62)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-agriculture-fns",
        "Department of Agriculture (FNS and Rural)",
        10,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 2/3 of Agriculture.",
        specs,
        total_rows={12},
        rollups=[(12, [8, 9, 10, 11])],
    )

    # --- #263 agriculture-departmental ---
    specs = [
        ("Forest Service: National Forest System", V(m, 65)),
        ("Forest Service: Capital Improvement and Maintenance", V(m, 66)),
        ("Forest Service: Wildland Fire Management", V(m, 67)),
        ("Forest Service: Forest Service Permanent Appropriations", V(m, 68)),
        ("Forest Service: Other", V(m, 69)),
        ("Total--Forest Service", V(m, 70)),
        ("Agriculture Departmental: Other", V(m, 71)),
        ("Proprietary Receipts from the Public", V(m, 72)),
        ("Intrabudgetary Transactions", V(m, 73)),
        ("Total--Department of Agriculture", V(m, 74)),
        # re-anchors
        ("Agricultural Research Service", V(m, 24)),
        (
            "National Institute of Food and Agriculture: Research and Education Activities",
            V(m, 26),
        ),
        (
            "National Institute of Food and Agriculture: Extension Activities",
            V(m, 27),
        ),
        ("National Institute of Food and Agriculture: Other", V(m, 28)),
        ("Animal and Plant Health Inspection Service", V(m, 29)),
        ("Food Safety and Inspection Service", V(m, 30)),
        ("Agricultural Marketing Service", V(m, 31)),
        (
            "Risk Management Agency: Administrative and Operating Expenses",
            V(m, 33),
        ),
        (
            "Risk Management Agency: Federal Crop Insurance Corporation Fund",
            V(m, 34),
        ),
        ("Total--Farm Service Agency", V(m, 43)),
        (
            "Natural Resources Conservation Service: Conservation Operations",
            V(m, 45),
        ),
        (
            "Natural Resources Conservation Service: Farm Security and Rural Investment Programs",
            V(m, 46),
        ),
        ("Natural Resources Conservation Service: Other", V(m, 47)),
        ("Rural Development", V(m, 48)),
        ("Rural Housing Service: Rural Housing Insurance Fund", V(m, 50)),
        ("Rural Housing Service: Rental Assistance Program", V(m, 51)),
        ("Rural Housing Service: Other", V(m, 52)),
        (
            "Rural Utilities Service: Rural Electrification and Telecommunications Fund",
            V(m, 54),
        ),
        ("Rural Utilities Service: Other", V(m, 55)),
        ("Foreign Agricultural Service", V(m, 56)),
        ("Total--Food and Nutrition Service", V(m, 62)),
    ]
    # Forest 1-5 → 6; department sources → 10
    dept_sources = (
        [6, 7, 8, 9]
        + list(range(11, 20))
        + [20]
        + list(range(21, 24))
        + list(range(24, 31))
        + [31]
    )
    build_unit(
        "treasury-mts/2026-06-outlays-agriculture-departmental",
        "Department of Agriculture (departmental capstone)",
        11,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 3/3 of Agriculture; re-anchors program/FNS lines.",
        specs,
        total_rows={6, 10, 20, 31},
        rollups=[(6, [1, 2, 3, 4, 5]), (10, dept_sources)],
    )

    # --- #264 commerce ---
    specs = [
        ("Economic Development Administration", V(m, 76)),
        ("Bureau of the Census", V(m, 77)),
        ("International Trade Administration", V(m, 78)),
        ("National Oceanic and Atmospheric Administration", V(m, 79)),
        ("National Institute of Standards and Technology", V(m, 80)),
        (
            "National Telecommunications and Information Administration",
            V(m, 81),
        ),
        ("Other", V(m, 82)),
        ("Proprietary Receipts from the Public", V(m, 83)),
        ("Intrabudgetary Transactions", V(m, 84)),
        ("Offsetting Governmental Receipts", V(m, 85)),
        ("Total--Department of Commerce", V(m, 86)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-commerce",
        "Department of Commerce",
        11,
        "USD millions. ...... and (**) cells omitted (not zero).",
        specs,
        total_rows={11},
        rollups=[(11, list(range(1, 11)))],
    )

    # --- #265 defense-programs ---
    specs = [
        ("Military Personnel: Department of the Army", V(m, 89)),
        ("Military Personnel: Department of the Navy", V(m, 90)),
        ("Military Personnel: Department of the Air Force", V(m, 91)),
        ("Military Personnel: Defense Agencies", V(m, 92)),
        ("Total--Military Personnel", V(m, 93)),
        ("Operation and Maintenance: Department of the Army", V(m, 95)),
        ("Operation and Maintenance: Department of the Navy", V(m, 96)),
        ("Operation and Maintenance: Department of the Air Force", V(m, 97)),
        ("Operation and Maintenance: Defense Agencies", V(m, 98)),
        ("Total--Operation and Maintenance", V(m, 99)),
        ("Procurement: Department of the Army", V(m, 101)),
        ("Procurement: Department of the Navy", V(m, 102)),
        ("Procurement: Department of the Air Force", V(m, 103)),
        ("Procurement: Defense Agencies", V(m, 104)),
        ("Total--Procurement", V(m, 105)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-defense-programs",
        "Department of Defense--Military Programs (Personnel/O&M/Procurement)",
        11,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 1/3 of DoD Military.",
        specs,
        total_rows={5, 10, 15},
        rollups=[
            (5, [1, 2, 3, 4]),
            (10, [6, 7, 8, 9]),
            (15, [11, 12, 13, 14]),
        ],
    )

    # --- #266 defense-rdte ---
    # Find RDT&E block
    # From dump pattern: after Procurement total
    # Let's locate by scanning
    def find_exact(label: str, start: int = 0):
        for i, (lab, nums) in enumerate(m):
            if i >= start and lab == label and nums is not None:
                return i
        raise KeyError(label)

    def find_header(label: str, start: int = 0):
        for i, (lab, nums) in enumerate(m):
            if i >= start and lab == label and nums is None:
                return i
        raise KeyError(label)

    rdte_h = find_header("Research, Development, Test, and Evaluation")
    # next 4 agencies + total
    r1, r2, r3, r4 = rdte_h + 1, rdte_h + 2, rdte_h + 3, rdte_h + 4
    rtot = find_exact("Total--Research, Development, Test, and Evaluation")
    milcon_h = find_header("Military Construction")
    m1, m2, m3, m4 = milcon_h + 1, milcon_h + 2, milcon_h + 3, milcon_h + 4
    mtot = find_exact("Total--Military Construction")
    fh_h = find_header("Family Housing")
    f1, f2, f3, f4 = fh_h + 1, fh_h + 2, fh_h + 3, fh_h + 4

    specs = [
        (
            "Research, Development, Test, and Evaluation: Department of the Army",
            V(m, r1),
        ),
        (
            "Research, Development, Test, and Evaluation: Department of the Navy",
            V(m, r2),
        ),
        (
            "Research, Development, Test, and Evaluation: Department of the Air Force",
            V(m, r3),
        ),
        (
            "Research, Development, Test, and Evaluation: Defense Agencies",
            V(m, r4),
        ),
        (
            "Total--Research, Development, Test, and Evaluation",
            V(m, rtot),
        ),
        ("Military Construction: Department of the Army", V(m, m1)),
        ("Military Construction: Department of the Navy", V(m, m2)),
        ("Military Construction: Department of the Air Force", V(m, m3)),
        ("Military Construction: Defense Agencies", V(m, m4)),
        ("Total--Military Construction", V(m, mtot)),
        ("Family Housing: Department of the Army", V(m, f1)),
        ("Family Housing: Department of the Navy", V(m, f2)),
        ("Family Housing: Department of the Air Force", V(m, f3)),
        ("Family Housing: Defense Agencies", V(m, f4)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-defense-rdte",
        "Department of Defense--Military Programs (RDT&E/MilCon/Family Housing)",
        11,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 2/3 of DoD Military.",
        specs,
        total_rows={5, 10},
        rollups=[(5, [1, 2, 3, 4]), (10, [6, 7, 8, 9])],
    )

    # --- #267 defense-departmental ---
    rev_h = find_header("Revolving and Management Funds")
    # Department of the Navy under revolving
    rev_navy = rev_h + 1
    # Defense Agencies header then Working Capital / Other (maybe page break)
    wcf = find_exact("Working Capital Fund")
    other_rev = wcf + 1
    trust_h = find_header("Trust Funds")
    t1, t2, t3, t4 = trust_h + 1, trust_h + 2, trust_h + 3, trust_h + 4
    prop_h = find_header("Proprietary Receipts from the Public", start=trust_h)
    p1, p2, p3, p4 = prop_h + 1, prop_h + 2, prop_h + 3, prop_h + 4
    intra_h = find_header("Intrabudgetary Transactions", start=prop_h)
    i1, i2, i3, i4 = intra_h + 1, intra_h + 2, intra_h + 3, intra_h + 4
    off_h = find_header("Offsetting Governmental Receipts", start=intra_h)
    o1 = off_h + 1
    total_dod = find_exact("Total--Department of Defense--Military Programs")

    specs = [
        ("Total--Military Personnel", V(m, find_exact("Total--Military Personnel"))),
        (
            "Total--Operation and Maintenance",
            V(m, find_exact("Total--Operation and Maintenance")),
        ),
        ("Total--Procurement", V(m, find_exact("Total--Procurement"))),
        (
            "Total--Research, Development, Test, and Evaluation",
            V(m, rtot),
        ),
        ("Total--Military Construction", V(m, mtot)),
        ("Family Housing: Department of the Army", V(m, f1)),
        ("Family Housing: Department of the Navy", V(m, f2)),
        ("Family Housing: Department of the Air Force", V(m, f3)),
        ("Family Housing: Defense Agencies", V(m, f4)),
        ("Revolving and Management Funds: Department of the Navy", V(m, rev_navy)),
        (
            "Revolving and Management Funds: Defense Agencies: Working Capital Fund",
            V(m, wcf),
        ),
        (
            "Revolving and Management Funds: Defense Agencies: Other",
            V(m, other_rev),
        ),
        ("Trust Funds: Department of the Army", V(m, t1)),
        ("Trust Funds: Department of the Navy", V(m, t2)),
        ("Trust Funds: Department of the Air Force", V(m, t3)),
        ("Trust Funds: Defense Agencies", V(m, t4)),
        (
            "Proprietary Receipts from the Public: Department of the Army",
            V(m, p1),
        ),
        (
            "Proprietary Receipts from the Public: Department of the Navy",
            V(m, p2),
        ),
        (
            "Proprietary Receipts from the Public: Department of the Air Force",
            V(m, p3),
        ),
        (
            "Proprietary Receipts from the Public: Defense Agencies",
            V(m, p4),
        ),
        ("Intrabudgetary Transactions: Department of the Army", V(m, i1)),
        ("Intrabudgetary Transactions: Department of the Navy", V(m, i2)),
        ("Intrabudgetary Transactions: Department of the Air Force", V(m, i3)),
        ("Intrabudgetary Transactions: Defense Agencies", V(m, i4)),
        (
            "Offsetting Governmental Receipts: Department of the Army",
            V(m, o1),
        ),
        (
            "Total--Department of Defense--Military Programs",
            V(m, total_dod),
        ),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-defense-departmental",
        "Department of Defense--Military Programs (departmental capstone)",
        12,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 3/3 of DoD Military; re-anchors bureau totals.",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #268 education-bureaus ---
    specs = [
        (
            "Office of Elementary and Secondary Education / Accelerating Achievement and Ensuring Equity",
            V(m, 149),
        ),
        (
            "Office of Elementary and Secondary Education / Impact Aid",
            V(m, 150),
        ),
        (
            "Office of Elementary and Secondary Education / Education Improvement Programs",
            V(m, 151),
        ),
        ("Office of Elementary and Secondary Education / Other", V(m, 152)),
        (
            "Total--Office of Elementary and Secondary Education",
            V(m, 153),
        ),
        (
            "Office of Postsecondary Education / Higher Education",
            V(m, 162),
        ),
        ("Office of Postsecondary Education / Other", V(m, 163)),
        ("Total--Office of Postsecondary Education", V(m, 164)),
        (
            "Office of Federal Student Aid / Student Financial Assistance",
            V(m, 166),
        ),
        (
            "Office of Federal Student Aid / Student Aid Administration",
            V(m, 167),
        ),
        (
            "Office of Federal Student Aid / Federal Student Loan Reserve Fund",
            V(m, 168),
        ),
        (
            "Office of Federal Student Aid / Federal Direct Student Loans",
            V(m, 169),
        ),
        (
            "Office of Federal Student Aid / Federal Family Education Loans",
            V(m, 170),
        ),
        ("Office of Federal Student Aid / Other", V(m, 171)),
        ("Total--Office of Federal Student Aid", V(m, 172)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-education-bureaus",
        "Department of Education (bureaus)",
        12,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 1/2 of Education.",
        specs,
        total_rows={5, 8, 15},
        rollups=[
            (5, [1, 2, 3, 4]),
            (8, [6, 7]),
            (15, [9, 10, 11, 12, 13, 14]),
        ],
    )

    # --- #269 education-departmental ---
    specs = [
        (
            "Total--Office of Elementary and Secondary Education",
            V(m, 153),
        ),
        ("Office of Innovation and Improvement", V(m, 154)),
        ("Office of English Language Acquisition", V(m, 155)),
        (
            "Office of Special Education and Rehabilitative Services / Special Education",
            V(m, 157),
        ),
        (
            "Office of Special Education and Rehabilitative Services / Rehabilitation Services and Disability Research",
            V(m, 158),
        ),
        (
            "Office of Special Education and Rehabilitative Services / Special Institutions for Persons with Disabilities",
            V(m, 159),
        ),
        ("Office of Vocational and Adult Education", V(m, 160)),
        ("Total--Office of Postsecondary Education", V(m, 164)),
        ("Total--Office of Federal Student Aid", V(m, 172)),
        ("Institute of Education Sciences", V(m, 173)),
        ("Departmental Management", V(m, 174)),
        ("Other", V(m, 175)),
        ("Proprietary Receipts from the Public", V(m, 176)),
        ("Intrabudgetary Transactions", V(m, 177)),
        ("Total--Department of Education", V(m, 178)),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-education-departmental",
        "Department of Education (departmental capstone)",
        12,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 2/2 of Education; re-anchors bureau totals.",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #270 energy ---
    # Skip all-omitted Defense Nuclear Waste Disposal (188)
    specs = [
        (
            "National Nuclear Security Administration / Naval Reactors",
            V(m, 181),
        ),
        (
            "National Nuclear Security Administration / Weapons Activities",
            V(m, 182),
        ),
        (
            "National Nuclear Security Administration / Defense Nuclear Nonproliferation",
            V(m, 183),
        ),
        ("National Nuclear Security Administration / Other", V(m, 184)),
        (
            "Environmental and Other Defense Activities / Defense Environmental Cleanup",
            V(m, 186),
        ),
        (
            "Environmental and Other Defense Activities / Other Defense Activities",
            V(m, 187),
        ),
        ("Energy Programs / Science", V(m, 191)),
        ("Energy Programs / Energy Supply", V(m, 192)),
        (
            "Energy Programs / Energy Efficiency and Renewable Energy",
            V(m, 193),
        ),
        (
            "Energy Programs / Fossil Energy Research and Development",
            V(m, 194),
        ),
        (
            "Energy Programs / Uranium Enrichment Decontamination and Decommissioning Fund",
            V(m, 195),
        ),
        (
            "Energy Programs / Advanced Technology Vehicles Manufacturing Loan Program",
            V(m, 196),
        ),
        (
            "Energy Programs / Title 17 Innovative Technology Loan Guarantee Program",
            V(m, 197),
        ),
        ("Energy Programs / Other", V(m, 198)),
        ("Total--Energy Programs", V(m, 199)),
        ("Power Marketing Administration", V(m, 200)),
        ("Departmental Administration", V(m, 201)),
        ("Proprietary Receipts from the Public", V(m, 202)),
        ("Intrabudgetary Transactions", V(m, 203)),
        ("Total--Department of Energy", V(m, 204)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-energy",
        "Department of Energy",
        12,
        "USD millions. ...... and (**) cells omitted (not zero). Defense Nuclear Waste Disposal all-omitted row skipped.",
        specs,
        total_rows={15, 20},
        rollups=[
            (15, list(range(7, 15))),
            (20, list(range(1, 7)) + [15] + list(range(16, 20))),
        ],
    )

    print("done")


if __name__ == "__main__":
    main()
