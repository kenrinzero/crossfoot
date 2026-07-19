#!/usr/bin/env python3
"""Build June MTS Table 5 units #271–280 (HHS → Labor bureaus)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_june_t5_261_270 import V, build_unit, extract_rows  # noqa: E402


def main():
    m = extract_rows(13, 17)

    # --- #271 hhs-cms ---
    specs = [
        (
            "Centers for Medicare and Medicaid Services: Grants to States for Medicaid",
            V(m, 25),
        ),
        (
            "Centers for Medicare and Medicaid Services: Payments to Health Care Trust Funds",
            V(m, 26),
        ),
        (
            "Centers for Medicare and Medicaid Services: Children's Health Insurance Fund",
            V(m, 27),
        ),
        (
            "Centers for Medicare and Medicaid Services: State Grants and Demonstrations",
            V(m, 28),
        ),
        ("Federal Hospital Insurance Trust Fund: Benefit Payments", V(m, 30)),
        (
            "Federal Hospital Insurance Trust Fund: Administrative Expenses",
            V(m, 31),
        ),
        ("Total--Federal Hospital Insurance Trust Fund", V(m, 32)),
        (
            "Centers for Medicare and Medicaid Services: Health Care Fraud and Abuse Control",
            V(m, 33),
        ),
        (
            "Federal Supplementary Medical Insurance Trust Fund: Benefit Payments",
            V(m, 35),
        ),
        (
            "Federal Supplementary Medical Insurance Trust Fund: Administrative Expenses",
            V(m, 36),
        ),
        ("Medicare Prescription Drugs: Benefit Payments", V(m, 38)),
        (
            "Total--Federal Supplementary Medical Insurance Trust Fund",
            V(m, 39),
        ),
        ("Centers for Medicare and Medicaid Services: Other", V(m, 40)),
        ("Total--Centers for Medicare and Medicaid Services", V(m, 41)),
    ]
    # HI: 5+6→7; SMI: 9+10+11→12; CMS: 1-4,7,8,12,13→14
    build_unit(
        "treasury-mts/2026-06-outlays-hhs-cms",
        "Department of Health and Human Services (CMS)",
        13,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 1/3 of HHS.",
        specs,
        total_rows={7, 12, 14},
        rollups=[
            (7, [5, 6]),
            (12, [9, 10, 11]),
            (14, [1, 2, 3, 4, 7, 8, 12, 13]),
        ],
    )

    # --- #272 hhs-acf ---
    specs = [
        ("Food and Drug Administration", V(m, 17)),
        ("Health Resources and Services Administration", V(m, 18)),
        ("Indian Health Service", V(m, 19)),
        ("Centers for Disease Control and Prevention", V(m, 20)),
        ("National Institutes of Health", V(m, 21)),
        (
            "Substance Abuse and Mental Health Services Administration",
            V(m, 22),
        ),
        ("Agency for Healthcare Research and Quality", V(m, 23)),
        (
            "Administration for Children and Families: Temporary Assistance for Needy Families",
            V(m, 43),
        ),
        (
            "Administration for Children and Families: Contingency Fund",
            V(m, 44),
        ),
        (
            "Administration for Children and Families: Payments to States for Child Support Enforcement and Family Support Programs",
            V(m, 45),
        ),
        (
            "Administration for Children and Families: Low Income Home Energy Assistance",
            V(m, 46),
        ),
        (
            "Administration for Children and Families: Refugee and Entrant Assistance",
            V(m, 47),
        ),
        (
            "Administration for Children and Families: Child Care Entitlement to States",
            V(m, 48),
        ),
        (
            "Administration for Children and Families: Payments to States for the Child Care and Development Block Grant",
            V(m, 49),
        ),
        (
            "Administration for Children and Families: Social Services Block Grant",
            V(m, 50),
        ),
        (
            "Administration for Children and Families: Children and Families Services Programs",
            V(m, 51),
        ),
        (
            "Administration for Children and Families: Payments to States for Foster Care and Adoption Assistance",
            V(m, 52),
        ),
        ("Administration for Children and Families: Other", V(m, 53)),
        ("Total--Administration for Children and Families", V(m, 54)),
        ("Administration for Community Living", V(m, 55)),
        ("Departmental Management", V(m, 56)),
        ("Other", V(m, 57)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-hhs-acf",
        "Department of Health and Human Services (ACF and small agencies)",
        13,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 2/3 of HHS.",
        specs,
        total_rows={19},
        rollups=[(19, list(range(8, 19)))],
    )

    # --- #273 hhs-departmental ---
    specs = [
        ("Total--Centers for Medicare and Medicaid Services", V(m, 41)),
        ("Total--Administration for Children and Families", V(m, 54)),
        ("Food and Drug Administration", V(m, 17)),
        ("Health Resources and Services Administration", V(m, 18)),
        ("Indian Health Service", V(m, 19)),
        ("Centers for Disease Control and Prevention", V(m, 20)),
        ("National Institutes of Health", V(m, 21)),
        (
            "Substance Abuse and Mental Health Services Administration",
            V(m, 22),
        ),
        ("Agency for Healthcare Research and Quality", V(m, 23)),
        ("Administration for Community Living", V(m, 55)),
        ("Departmental Management", V(m, 56)),
        ("HHS Departmental: Other", V(m, 57)),
        ("Proprietary Receipts from the Public", V(m, 59)),
        (
            "Intrabudgetary Transactions: Payments for Health Insurance for the Aged: Federal Supplementary Medical Insurance Trust Fund",
            V(m, 62),
        ),
        (
            "Intrabudgetary Transactions: Payments for Tax and Other Credits: Federal Hospital Insurance Trust Fund",
            V(m, 64),
        ),
        ("Intrabudgetary Transactions: Other", V(m, 65)),
        ("Total--Department of Health and Human Services", V(m, 66)),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-hhs-departmental",
        "Department of Health and Human Services (departmental capstone)",
        14,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 3/3 of HHS; re-anchors CMS/ACF totals.",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #274 homeland-security ---
    specs = [
        ("Departmental Management and Operations", V(m, 68)),
        ("Citizenship and Immigration Services", V(m, 69)),
        ("United States Secret Service", V(m, 70)),
        ("Transportation Security Administration", V(m, 71)),
        ("Immigration and Customs Enforcement", V(m, 72)),
        ("U.S. Customs and Border Protection", V(m, 73)),
        ("United States Coast Guard", V(m, 74)),
        ("National Protection and Programs Directorate", V(m, 75)),
        ("Federal Emergency Management Agency / Disaster Relief", V(m, 77)),
        (
            "Federal Emergency Management Agency / National Flood Insurance Fund",
            V(m, 78),
        ),
        ("Federal Emergency Management Agency / Other", V(m, 79)),
        ("Total--Federal Emergency Management Agency", V(m, 80)),
        ("Science and Technology", V(m, 81)),
        ("Domestic Nuclear Detection Office", V(m, 82)),
        ("Other", V(m, 83)),
        ("Proprietary Receipts from the Public", V(m, 84)),
        ("Intrabudgetary Transactions", V(m, 85)),
        ("Offsetting Governmental Receipts", V(m, 86)),
        ("Total--Department of Homeland Security", V(m, 87)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-homeland-security",
        "Department of Homeland Security",
        14,
        "USD millions. ...... and (**) cells omitted (not zero).",
        specs,
        total_rows={12, 19},
        rollups=[
            (12, [9, 10, 11]),
            (19, list(range(1, 9)) + [12] + list(range(13, 19))),
        ],
    )

    # --- #275 hud-bureaus ---
    specs = [
        (
            "Public and Indian Housing Programs: Tenant Based Rental Assistance",
            V(m, 90),
        ),
        (
            "Public and Indian Housing Programs: Housing Certificate Fund",
            V(m, 91),
        ),
        (
            "Public and Indian Housing Programs: Public Housing Capital Fund",
            V(m, 92),
        ),
        (
            "Public and Indian Housing Programs: Public Housing Operating Fund",
            V(m, 93),
        ),
        (
            "Public and Indian Housing Programs: Revitalization of Severely Distressed Public Housing (Hope VI)",
            V(m, 94),
        ),
        (
            "Public and Indian Housing Programs: Native American Housing Block Grant",
            V(m, 95),
        ),
        ("Public and Indian Housing Programs: Other", V(m, 96)),
        ("Total--Public and Indian Housing Programs", V(m, 97)),
        (
            "Community Planning and Development: Housing Opportunities for Persons with AIDS",
            V(m, 99),
        ),
        (
            "Community Planning and Development: Community Development Fund",
            V(m, 100),
        ),
        (
            "Community Planning and Development: Home Investment Partnership Program",
            V(m, 101),
        ),
        (
            "Community Planning and Development: Neighborhood Stabilization Program",
            V(m, 102),
        ),
        (
            "Community Planning and Development: Homeless Assistance Grants",
            V(m, 103),
        ),
        ("Community Planning and Development: Other", V(m, 104)),
        ("Total--Community Planning and Development", V(m, 105)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-hud-bureaus",
        "Department of Housing and Urban Development (bureaus)",
        14,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 1/2 of HUD.",
        specs,
        total_rows={8, 15},
        rollups=[(8, list(range(1, 8))), (15, list(range(9, 15)))],
    )

    # --- #276 hud-departmental ---
    specs = [
        ("Total--Public and Indian Housing Programs", V(m, 97)),
        ("Total--Community Planning and Development", V(m, 105)),
        (
            "Housing Programs: Credit Accounts: FHA-Mutual Mortgage Insurance Fund, Program Account",
            V(m, 108),
        ),
        (
            "Housing Programs: Credit Accounts: FHA-Mutual Mortgage Insurance Capital Reserve Account",
            V(m, 109),
        ),
        (
            "Housing Programs: Credit Accounts: FHA-Mutual Mortgage and Cooperative Housing Insurance Fund, Liquidating Account",
            V(m, 110),
        ),
        (
            "Housing Programs: Credit Accounts: FHA-General and Special Risk Fund, Liquidating Account",
            V(m, 111),
        ),
        (
            "Housing Programs: Credit Accounts: Housing for the Elderly or Handicapped Fund, Liquidating Account",
            V(m, 112),
        ),
        (
            "Housing Programs: HUD Project-Based Rental Assistance",
            V(m, 113),
        ),
        ("Housing Programs: Housing for the Elderly", V(m, 114)),
        (
            "Housing Programs: Housing for Persons with Disabilities",
            V(m, 115),
        ),
        (
            "Housing Programs: Other Assisted Housing Programs",
            V(m, 116),
        ),
        ("Housing Programs: Other", V(m, 117)),
        ("Total--Housing Programs", V(m, 118)),
        (
            "Government National Mortgage Association: Guarantees of Mortgage-Backed Securities",
            V(m, 121),
        ),
        ("Management and Administration", V(m, 122)),
        ("Other", V(m, 123)),
        (
            "Proprietary Receipts from the Public: FHA-General and Special Risk Fund",
            V(m, 125),
        ),
        ("Proprietary Receipts from the Public: Other", V(m, 126)),
        ("Intrabudgetary Transactions", V(m, 127)),
        ("Offsetting Governmental Receipts", V(m, 128)),
        (
            "Total--Department of Housing and Urban Development",
            V(m, 129),
        ),
    ]
    # Housing Programs roll-up: rows 3-12 → 13; department: 1,2,13,14-20 → 21
    build_unit(
        "treasury-mts/2026-06-outlays-hud-departmental",
        "Department of Housing and Urban Development (departmental capstone)",
        15,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 2/2 of HUD; re-anchors bureau totals.",
        specs,
        total_rows={13, 21},
        rollups=[
            (13, list(range(3, 13))),
            (21, [1, 2, 13] + list(range(14, 21))),
        ],
    )

    # --- #277 interior-bureaus ---
    specs = [
        ("Management of Lands and Resources", V(m, 133)),
        ("Other", V(m, 134)),  # BLM Other
        ("Bureau of Ocean Energy Management", V(m, 135)),
        (
            "Office of Surface Mining Reclamation and Enforcement",
            V(m, 136),
        ),
        ("Total--Land and Minerals Management", V(m, 137)),
        ("Water and Related Resources", V(m, 140)),
        ("Other", V(m, 141)),  # Reclamation Other
        ("Central Utah Project", V(m, 142)),
        ("United States Geological Survey", V(m, 143)),
        ("Total--Water and Science", V(m, 144)),
        ("United States Fish and Wildlife Service", V(m, 146)),
        ("National Park Service", V(m, 147)),
        ("Total--Fish and Wildlife and Parks", V(m, 148)),
        ("Mineral Leasing and Associated Payments", V(m, 153)),
        ("Other", V(m, 154)),  # Dept Offices Other
        ("Insular Affairs", V(m, 155)),
        (
            "Office of the Special Trustee for American Indians",
            V(m, 156),
        ),
        ("Department-Wide Programs", V(m, 157)),
        ("Total--Departmental Offices", V(m, 158)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-interior-bureaus",
        "Department of the Interior (bureaus)",
        15,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 1/2 of Interior.",
        specs,
        total_rows={5, 10, 13, 19},
        rollups=[
            (5, [1, 2, 3, 4]),
            (10, [6, 7, 8, 9]),
            (13, [11, 12]),
            (19, [14, 15, 16, 17, 18]),
        ],
    )

    # --- #278 interior-departmental ---
    specs = [
        ("Total--Land and Minerals Management", V(m, 137)),
        ("Total--Water and Science", V(m, 144)),
        ("Total--Fish and Wildlife and Parks", V(m, 148)),
        ("Total--Departmental Offices", V(m, 158)),
        (
            "Bureau of Indian Affairs and Bureau of Indian Education",
            V(m, 150),
        ),
        ("Total--Indian Affairs", V(m, 151)),
        ("Other", V(m, 159)),
        ("Proprietary Receipts from the Public", V(m, 160)),
        ("Intrabudgetary Transactions", V(m, 161)),
        ("Total--Department of the Interior", V(m, 162)),
    ]
    # Indian Affairs: 5→6 single-source often; department roll-up uses totals carefully
    # May uses Total Indian Affairs (not BIA leaf + Total double). Sources for Total Interior:
    # LMM, Water, FWP, DeptOff, Indian total, Other, Prop, Intra
    # BIA leaf may be standalone or only feed Total Indian
    # Single-line Indian Affairs bureau: BIA is standalone; Total--Indian Affairs
    # re-anchors into department roll-up (May minItems:2 pattern).
    build_unit(
        "treasury-mts/2026-06-outlays-interior-departmental",
        "Department of the Interior (departmental capstone)",
        15,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 2/2 of Interior; re-anchors bureau totals. Single-line Indian Affairs bureau as standalone.",
        specs,
        total_rows={10},
        rollups=[(10, [1, 2, 3, 4, 6, 7, 8, 9])],
    )

    # --- #279 justice ---
    specs = [
        ("General Administration", V(m, 164)),
        (
            "Legal Activities and U.S. Marshals / General Legal Activities",
            V(m, 166),
        ),
        (
            "Legal Activities and U.S. Marshals / United States Attorneys",
            V(m, 167),
        ),
        (
            "Legal Activities and U.S. Marshals / United States Marshals Service",
            V(m, 168),
        ),
        (
            "Legal Activities and U.S. Marshals / Assets Forfeiture Fund",
            V(m, 169),
        ),
        ("Legal Activities and U.S. Marshals / Other", V(m, 170)),
        ("Federal Bureau of Investigation", V(m, 171)),
        ("Drug Enforcement Administration", V(m, 172)),
        (
            "Bureau of Alcohol, Tobacco, Firearms, and Explosives",
            V(m, 173),
        ),
        ("Federal Prison System", V(m, 174)),
        (
            "Office of Justice Programs / State and Local Law Enforcement Assistance",
            V(m, 176),
        ),
        (
            "Office of Justice Programs / Community Oriented Policing Services",
            V(m, 177),
        ),
        ("Office of Justice Programs / Crime Victims Fund", V(m, 178)),
        ("Office of Justice Programs / Other", V(m, 179)),
        ("Other", V(m, 180)),
        ("Proprietary Receipts from the Public", V(m, 181)),
        ("Intrabudgetary Transactions", V(m, 182)),
        ("Offsetting Governmental Receipts", V(m, 183)),
        ("Total--Department of Justice", V(m, 184)),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-justice",
        "Department of Justice",
        15,
        "USD millions. ...... and (**) cells omitted (not zero).",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #280 labor-bureaus ---
    specs = [
        ("Training and Employment Services", V(m, 187)),
        ("Office of Job Corps", V(m, 188)),
        ("Community Service Employment for Older Americans", V(m, 189)),
        ("Federal Unemployment Benefits and Allowances", V(m, 190)),
        (
            "Federal Additional Unemployment Compensation Program-Recovery Act",
            V(m, 191),
        ),
        (
            "State Unemployment Insurance and Employment Service Operations",
            V(m, 192),
        ),
        ("Payments to the Unemployment Trust Fund", V(m, 193)),
        ("Program Administration", V(m, 194)),
        ("State Unemployment Benefits", V(m, 197)),
        ("State Administrative Expenses", V(m, 198)),
        ("Federal Administrative Expenses", V(m, 199)),
        ("Other", V(m, 200)),  # UTF Other
        ("Total--Unemployment Trust Fund", V(m, 201)),
        ("Other", V(m, 202)),  # ETA Other
        ("Total--Employment and Training Administration", V(m, 203)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-labor-bureaus",
        "Department of Labor (Employment and Training Administration)",
        16,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 1/2 of Labor.",
        specs,
        total_rows={13, 15},
        rollups=[
            (13, [9, 10, 11, 12]),
            (15, list(range(1, 9)) + [13, 14]),
        ],
    )

    print("done")


if __name__ == "__main__":
    main()
