#!/usr/bin/env python3
"""Build June MTS Table 5 units #281–290 (Labor dept → Other Defense Civil)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_june_t5_261_270 import V, build_unit, extract_rows  # noqa: E402


def main():
    m = extract_rows(16, 19)

    # --- #281 labor-departmental ---
    specs = [
        ("Total--Employment and Training Administration", V(m, 18)),
        ("Pension Benefit Guaranty Corporation", V(m, 19)),
        ("Special Benefits", V(m, 21)),
        (
            "Energy Employees Occupational Illness Compensation Fund",
            V(m, 22),
        ),
        ("Special Benefits for Disabled Coal Miners", V(m, 23)),
        ("Black Lung Disability Trust Fund", V(m, 24)),
        ("Other", V(m, 25)),  # OWCP Other
        ("Wage and Hour Division", V(m, 26)),
        ("Occupational Safety and Health Administration", V(m, 27)),
        ("Mine Safety and Health Administration", V(m, 28)),
        ("Bureau of Labor Statistics", V(m, 29)),
        ("Departmental Management", V(m, 30)),
        ("Other", V(m, 31)),
        ("Proprietary Receipts from the Public", V(m, 32)),
        ("Intrabudgetary Transactions", V(m, 33)),
        ("Total--Department of Labor", V(m, 34)),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-labor-departmental",
        "Department of Labor (departmental capstone)",
        16,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 2/2 of Labor; re-anchors ETA total.",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #282 state ---
    # Skip all-omitted Andean Counterdrug Programs (48)
    specs = [
        (
            "Administration of Foreign Affairs / Diplomatic and Consular Programs",
            V(m, 37),
        ),
        (
            "Administration of Foreign Affairs / Educational and Cultural Exchange Programs",
            V(m, 38),
        ),
        (
            "Administration of Foreign Affairs / Embassy Security, Construction, and Maintenance",
            V(m, 39),
        ),
        (
            "Administration of Foreign Affairs / Payment to Foreign Service Retirement and Disability Fund",
            V(m, 40),
        ),
        (
            "Administration of Foreign Affairs / Foreign Service Retirement and Disability Fund",
            V(m, 41),
        ),
        ("Administration of Foreign Affairs / Other", V(m, 42)),
        ("Total--Administration of Foreign Affairs", V(m, 43)),
        ("International Organizations and Conferences", V(m, 44)),
        ("Global Health and Child Survival", V(m, 45)),
        ("Migration and Refugee Assistance", V(m, 46)),
        (
            "International Narcotics Control and Law Enforcement",
            V(m, 47),
        ),
        ("Other", V(m, 49)),
        ("Proprietary Receipts from the Public", V(m, 50)),
        ("Intrabudgetary Transactions", V(m, 51)),
        ("Total--Department of State", V(m, 52)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-state",
        "Department of State",
        16,
        "USD millions. ...... and (**) cells omitted (not zero). Andean Counterdrug Programs all-omitted row skipped.",
        specs,
        total_rows={7, 15},
        rollups=[
            (7, list(range(1, 7))),
            (15, [7] + list(range(8, 15))),
        ],
    )

    # --- #283 transportation-bureaus ---
    specs = [
        ("Operations", V(m, 56)),
        ("Grants-In-Aid for Airports", V(m, 58)),
        ("Facilities and Equipment", V(m, 60)),
        ("Research, Engineering, and Development", V(m, 61)),
        ("Trust Fund Share of FAA Operations", V(m, 62)),
        ("Total--Airport and Airway Trust Fund", V(m, 63)),
        ("Other", V(m, 64)),
        ("Total--Federal Aviation Administration", V(m, 65)),
        ("Federal-Aid Highways", V(m, 68)),
        ("Other", V(m, 69)),  # HTF Other
        ("Other Programs", V(m, 70)),
        ("Total--Federal Highway Administration", V(m, 71)),
        ("Formula Grants", V(m, 78)),
        ("Capital Investment Grants", V(m, 79)),
        ("Transit Formula Grants", V(m, 80)),
        ("Other", V(m, 81)),
        ("Total--Federal Transit Administration", V(m, 82)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-transportation-bureaus",
        "Department of Transportation (FAA/FHA/FTA bureaus)",
        16,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 1/2 of Transportation.",
        specs,
        total_rows={6, 8, 12, 17},
        rollups=[
            (6, [2, 3, 4, 5]),
            (8, [1, 6, 7]),
            (12, [9, 10, 11]),
            (17, [13, 14, 15, 16]),
        ],
    )

    # --- #284 transportation-departmental ---
    specs = [
        ("Total--Federal Aviation Administration", V(m, 65)),
        ("Total--Federal Highway Administration", V(m, 71)),
        ("Total--Federal Transit Administration", V(m, 82)),
        ("Office of the Secretary", V(m, 54)),
        ("Federal Motor Carrier Safety Administration", V(m, 72)),
        ("National Highway Traffic Safety Administration", V(m, 73)),
        ("Other", V(m, 75)),  # FRA Other
        ("Total--Federal Railroad Administration", V(m, 76)),
        ("Maritime Administration", V(m, 83)),
        ("Other", V(m, 84)),
        ("Proprietary Receipts from the Public", V(m, 85)),
        ("Other", V(m, 87)),  # Intrabudgetary Other
        ("Offsetting Governmental Receipts", V(m, 88)),
        ("Total--Department of Transportation", V(m, 89)),
    ]
    n = len(specs)
    # Department sources: bureau totals + lines, not FRA Other when Total FRA re-anchors
    # May: FAA, FHA, FTA, Sec, FMCSA, NHTSA, Total FRA, Maritime, Other, Prop, Intra Other, Offset
    # Exclude row 7 (FRA Other) to avoid double-count with Total FRA (8)
    build_unit(
        "treasury-mts/2026-06-outlays-transportation-departmental",
        "Department of Transportation (departmental capstone)",
        17,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 2/2 of Transportation; re-anchors bureau totals.",
        specs,
        total_rows={8, n},
        rollups=[
            (8, [7]),  # single-line FRA — may skip; Total FRA stays re-anchor
            (n, [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13]),
        ],
    )

    # --- #285 treasury-bureaus ---
    # Skip all-omitted Transportation Services (99)
    specs = [
        ("Departmental Offices: Exchange Stabilization Fund", V(m, 92)),
        (
            "Departmental Offices: Housing and Economic Recovery Programs",
            V(m, 93),
        ),
        (
            "Departmental Offices: ESF - Economic Stabilization Program",
            V(m, 94),
        ),
        ("Departmental Offices: Air Carrier Worker Support", V(m, 95)),
        ("Departmental Offices: Coronavirus Relief Fund", V(m, 96)),
        (
            "Departmental Offices: Emergency Capital Investment Program",
            V(m, 97),
        ),
        ("Departmental Offices: Emergency Rental Assistance", V(m, 98)),
        ("Departmental Offices: Other", V(m, 100)),
        (
            "Bureau of the Fiscal Service: Payment to the Resolution Funding Corporation",
            V(m, 102),
        ),
        (
            "Bureau of the Fiscal Service: Financial Agent Services",
            V(m, 103),
        ),
        (
            "Bureau of the Fiscal Service: Claims, Judgements, and Relief Acts",
            V(m, 104),
        ),
        ("Bureau of the Fiscal Service: Other", V(m, 105)),
        ("Total--Bureau of the Fiscal Service", V(m, 106)),
        (
            "Alcohol and Tobacco Tax and Trade Bureau: Salaries and Expenses",
            V(m, 109),
        ),
        (
            "Alcohol and Tobacco Tax and Trade Bureau: Internal Revenue Collections for Puerto Rico",
            V(m, 110),
        ),
        ("Bureau of Engraving and Printing", V(m, 111)),
        ("United States Mint", V(m, 112)),
    ]
    # Fiscal Service roll-up: rows 9-12 → 13 (after Transportation Services dropped)
    build_unit(
        "treasury-mts/2026-06-outlays-treasury-bureaus",
        "Department of the Treasury (bureaus excl. IRS)",
        17,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 1/3 of Treasury. Transportation Services all-omitted skipped.",
        specs,
        total_rows={13},
        rollups=[(13, [9, 10, 11, 12])],
    )

    # --- #286 treasury-irs ---
    # June splits Refundable Premium Tax Credits into Treasury + HHS lines
    specs = [
        ("Internal Revenue Service: Taxpayer Services", V(m, 114)),
        ("Internal Revenue Service: Enforcement", V(m, 115)),
        ("Internal Revenue Service: Operations Support", V(m, 116)),
        (
            "Internal Revenue Service: Build America Bond Payments, Recovery Act",
            V(m, 117),
        ),
        (
            "Internal Revenue Service: Refundable Premium Tax Credits and Cost Sharing Reductions, Treasury",
            V(m, 118),
        ),
        (
            "Internal Revenue Service: Refundable Premium Tax Credits and Cost Sharing Reductions, HHS",
            V(m, 119),
        ),
        (
            "Internal Revenue Service: Payment Where Earned Income Credit Exceeds Liability for Tax",
            V(m, 121),
        ),
        (
            "Internal Revenue Service: Payment Where Child Tax Credit Exceeds Liability for Tax",
            V(m, 122),
        ),
        (
            "Internal Revenue Service: Payment Where American Opportunity Tax Credit Exceeds Liability for Tax",
            V(m, 123),
        ),
        (
            "Internal Revenue Service: Refunding Internal Revenue Collections, Interest",
            V(m, 124),
        ),
        ("Internal Revenue Service: Other", V(m, 125)),
        ("Total--Internal Revenue Service", V(m, 126)),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-treasury-irs",
        "Department of the Treasury (Internal Revenue Service)",
        17,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 2/3 of Treasury. June splits Refundable Premium Tax Credits into Treasury/HHS lines.",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #287 treasury-departmental ---
    # Skip all-omitted Transportation Services
    specs = [
        ("Comptroller of the Currency", V(m, 127)),
        (
            "Interest on the Public Debt: Interest on Treasury Debt Securities (Gross): Public Issues (Accrual Basis)",
            V(m, 130),
        ),
        (
            "Interest on the Public Debt: Interest on Treasury Debt Securities (Gross): Special Issues (Cash Basis)",
            V(m, 131),
        ),
        (
            "Total--Interest on Treasury Debt Securities (Gross)",
            V(m, 132),
        ),
        ("Total--Interest on the Public Debt", V(m, 133)),
        ("Other", V(m, 134)),
        ("Proprietary Receipts from the Public", V(m, 135)),
        ("Intrabudgetary Transactions", V(m, 136)),
        ("Total--Department of the Treasury", V(m, 137)),
        ("Federal Financing Bank", V(m, 107)),
        ("Total--Internal Revenue Service", V(m, 126)),
        ("Total--Bureau of the Fiscal Service", V(m, 106)),
        ("Departmental Offices: Exchange Stabilization Fund", V(m, 92)),
        (
            "Departmental Offices: Housing and Economic Recovery Programs",
            V(m, 93),
        ),
        (
            "Departmental Offices: ESF - Economic Stabilization Program",
            V(m, 94),
        ),
        ("Departmental Offices: Air Carrier Worker Support", V(m, 95)),
        ("Departmental Offices: Coronavirus Relief Fund", V(m, 96)),
        (
            "Departmental Offices: Emergency Capital Investment Program",
            V(m, 97),
        ),
        ("Departmental Offices: Emergency Rental Assistance", V(m, 98)),
        ("Departmental Offices: Other", V(m, 100)),
        (
            "Alcohol and Tobacco Tax and Trade Bureau: Salaries and Expenses",
            V(m, 109),
        ),
        (
            "Alcohol and Tobacco Tax and Trade Bureau: Internal Revenue Collections for Puerto Rico",
            V(m, 110),
        ),
        ("Bureau of Engraving and Printing", V(m, 111)),
        ("United States Mint", V(m, 112)),
    ]
    # Interest: 2+3→4; 4→5 (or 4==5 when only securities); department uses 5 not 2-4
    # Dept sources: 1,5,6,7,8,10-24 (exclude 2,3,4 detail; exclude total 9)
    build_unit(
        "treasury-mts/2026-06-outlays-treasury-departmental",
        "Department of the Treasury (departmental capstone)",
        18,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 3/3 of Treasury; re-anchors IRS/Fiscal/DO lines.",
        specs,
        total_rows={4, 5, 9},
        rollups=[
            (4, [2, 3]),
            (5, [4]),  # may skip if single-source equality
            (
                9,
                [1, 5, 6, 7, 8]
                + list(range(10, 25)),
            ),
        ],
    )

    # --- #288 veterans-affairs ---
    # Skip all-omitted Veterans Choice Fund (141)
    specs = [
        ("Joint DOD-VA Medical Facility Demonstration Fund", V(m, 139)),
        ("Veterans Health Administration / Medical Services", V(m, 142)),
        (
            "Veterans Health Administration / Medical Support and Compliance",
            V(m, 143),
        ),
        ("Veterans Health Administration / Medical Facilities", V(m, 144)),
        ("Veterans Health Administration / Other", V(m, 145)),
        (
            "Benefits Programs / Public Enterprise Funds / Housing Accounts",
            V(m, 148),
        ),
        (
            "Benefits Programs / Public Enterprise Funds / Other",
            V(m, 149),
        ),
        ("Benefits Programs / Compensation and Pensions", V(m, 150)),
        ("Benefits Programs / Readjustment Benefits", V(m, 151)),
        (
            "Benefits Programs / Veterans Housing Benefit Program Fund",
            V(m, 152),
        ),
        (
            "Benefits Programs / Insurance Funds / National Service Life",
            V(m, 154),
        ),
        (
            "Benefits Programs / Insurance Funds / Veterans Special Life",
            V(m, 155),
        ),
        ("Benefits Programs / Other", V(m, 156)),
        ("Total--Benefits Programs", V(m, 157)),
        ("Departmental Administration / Construction", V(m, 159)),
        (
            "Departmental Administration / Information Technology Systems",
            V(m, 160),
        ),
        (
            "Departmental Administration / General Operating Expenses",
            V(m, 161),
        ),
        ("Departmental Administration / Other", V(m, 162)),
        (
            "Proprietary Receipts from the Public / National Service Life",
            V(m, 164),
        ),
        ("Proprietary Receipts from the Public / Other", V(m, 165)),
        ("Intrabudgetary Transactions", V(m, 166)),
        ("Total--Department of Veterans Affairs", V(m, 167)),
    ]
    # Benefits: 6-13 → 14; Dept: 1-5, 14, 15-18, 19-21 → 22 (auto per-col)
    build_unit(
        "treasury-mts/2026-06-outlays-veterans-affairs",
        "Department of Veterans Affairs",
        18,
        "USD millions. ...... and (**) cells omitted (not zero). Veterans Choice Fund all-omitted row skipped.",
        specs,
        total_rows={14, 22},
        rollups=[
            (14, list(range(6, 14))),
            (22, list(range(1, 6)) + [14] + list(range(15, 22))),
        ],
    )

    # --- #289 corps-engineers ---
    specs = [
        ("Construction", V(m, 169)),
        ("Operation and Maintenance", V(m, 170)),
        ("Flood Control and Coastal Emergencies", V(m, 171)),
        ("Harbor Maintenance Trust Fund", V(m, 172)),
        ("Rivers and Harbors Contributed Funds", V(m, 173)),
        ("Other", V(m, 174)),
        ("Proprietary Receipts from the Public", V(m, 175)),
        ("Intrabudgetary Transactions", V(m, 176)),
        ("Total--Corps of Engineers", V(m, 177)),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-corps-engineers",
        "Corps of Engineers",
        18,
        "USD millions. ...... and (**) cells omitted (not zero).",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #290 other-defense-civil ---
    specs = [
        ("Payment to Military Retirement Fund", V(m, 180)),
        ("Military Retirement Fund", V(m, 182)),
        (
            "Payment to Department of Defense Medicare-Eligible Retiree Health Care Fund",
            V(m, 184),
        ),
        (
            "Department of Defense Medicare-Eligible Retiree Health Care Fund",
            V(m, 185),
        ),
        ("Educational Benefits", V(m, 186)),
        ("Other", V(m, 187)),
        ("Proprietary Receipts from the Public", V(m, 188)),
        ("Intrabudgetary Transactions", V(m, 189)),
        ("Total--Other Defense Civil Programs", V(m, 190)),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-other-defense-civil",
        "Other Defense Civil Programs",
        19,
        "USD millions. ...... and (**) cells omitted (not zero).",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    print("done")


if __name__ == "__main__":
    main()
