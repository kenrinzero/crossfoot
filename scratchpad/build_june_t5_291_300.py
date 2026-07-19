#!/usr/bin/env python3
"""Build June MTS Table 5 units #291–300 (EPA → SSA + grand-total capstone)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_june_t5_261_270 import V, build_unit, extract_rows  # noqa: E402


def main():
    m = extract_rows(19, 23)

    # --- #291 epa ---
    specs = [
        ("Science and Technology", V(m, 11)),
        ("Environmental Programs and Management", V(m, 12)),
        ("State and Tribal Assistance Grants", V(m, 13)),
        ("Payment to the Hazardous Substance Superfund", V(m, 14)),
        ("Hazardous Substance Superfund", V(m, 15)),
        ("Other", V(m, 16)),
        ("Proprietary Receipts from the Public", V(m, 17)),
        ("Intrabudgetary Transactions", V(m, 18)),
        ("Offsetting Governmental Receipts", V(m, 19)),
        ("Total--Environmental Protection Agency", V(m, 20)),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-epa",
        "Environmental Protection Agency",
        19,
        "USD millions. ...... and (**) cells omitted (not zero).",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #292 gsa ---
    specs = [
        ("Real Property Activities", V(m, 30)),
        ("Supply and Technology Activities", V(m, 31)),
        ("General Activities", V(m, 32)),
        ("Proprietary Receipts from the Public", V(m, 33)),
        ("Intrabudgetary Transactions", V(m, 34)),
        ("Total--General Services Administration", V(m, 35)),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-gsa",
        "General Services Administration",
        19,
        "USD millions. ...... and (**) cells omitted (not zero).",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #293 international-assistance-bureaus ---
    specs = [
        (
            "International Security Assistance / Foreign Military Financing Program",
            V(m, 39),
        ),
        (
            "International Security Assistance / Economic Support Fund",
            V(m, 40),
        ),
        ("International Security Assistance / Other", V(m, 41)),
        (
            "International Security Assistance / Proprietary Receipts from the Public",
            V(m, 42),
        ),
        ("Total--International Security Assistance", V(m, 43)),
        (
            "Agency for International Development / Development Assistance Program",
            V(m, 50),
        ),
        (
            "Agency for International Development / Assistance for Europe, Eurasia and Central Asia",
            V(m, 51),
        ),
        (
            "Agency for International Development / International Disaster Assistance",
            V(m, 52),
        ),
        (
            "Agency for International Development / Operating Expenses",
            V(m, 53),
        ),
        ("Agency for International Development / Other", V(m, 54)),
        (
            "Agency for International Development / Proprietary Receipts from the Public",
            V(m, 55),
        ),
        (
            "Agency for International Development / Intrabudgetary Transactions",
            V(m, 56),
        ),
        ("Total--Agency for International Development", V(m, 57)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-international-assistance-bureaus",
        "International Assistance Programs (ISA and AID bureaus)",
        19,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 1/2 of International Assistance.",
        specs,
        total_rows={5, 13},
        rollups=[
            (5, [1, 2, 3, 4]),
            (13, list(range(6, 13))),
        ],
    )

    # --- #294 international-assistance-departmental ---
    # Skip all-omitted OPIC accounts/total (59-60)
    specs = [
        ("Millennium Challenge Corporation", V(m, 37)),
        ("Total--International Security Assistance", V(m, 43)),
        (
            "Multilateral Assistance / Contribution to the International Development Association",
            V(m, 45),
        ),
        ("Multilateral Assistance / Other", V(m, 46)),
        (
            "Multilateral Assistance / Proprietary Receipts from the Public",
            V(m, 47),
        ),
        ("Total--Multilateral Assistance", V(m, 48)),
        ("Total--Agency for International Development", V(m, 57)),
        ("Peace Corps", V(m, 62)),
        ("Peace Corps / Proprietary Receipts", V(m, 63)),
        ("International Monetary Programs", V(m, 64)),
        (
            "Military Sales Program / Foreign Military Sales Trust Fund",
            V(m, 66),
        ),
        ("Military Sales Program / Other", V(m, 67)),
        (
            "Military Sales Program / Proprietary Receipts from the Public",
            V(m, 68),
        ),
        ("Other", V(m, 69)),
        ("Total--International Assistance Programs", V(m, 70)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-international-assistance-departmental",
        "International Assistance Programs (departmental capstone)",
        20,
        "USD millions. ...... and (**) cells omitted (not zero). Unit 2/2 of International Assistance; re-anchors ISA/AID totals. OPIC all-omitted skipped.",
        specs,
        total_rows={6, 15},
        rollups=[
            (6, [3, 4, 5]),
            (15, [1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14]),
        ],
    )

    # --- #295 nasa ---
    specs = [
        ("Science", V(m, 72)),
        ("Aeronautics", V(m, 73)),
        ("Exploration", V(m, 74)),
        ("Cross Agency Support", V(m, 75)),
        ("Space Operations", V(m, 76)),
        ("Other", V(m, 77)),
        ("Proprietary Receipts from the Public", V(m, 78)),
        ("Intrabudgetary Transactions", V(m, 79)),
        (
            "Total--National Aeronautics and Space Administration",
            V(m, 80),
        ),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-nasa",
        "National Aeronautics and Space Administration",
        20,
        "USD millions. ...... and (**) cells omitted (not zero).",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #296 nsf ---
    specs = [
        ("Research and Related Activities", V(m, 82)),
        ("Education and Human Resources", V(m, 83)),
        ("Other", V(m, 84)),
        ("Proprietary Receipts from the Public", V(m, 85)),
        ("Total--National Science Foundation", V(m, 86)),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-nsf",
        "National Science Foundation",
        20,
        "USD millions. ...... and (**) cells omitted (not zero).",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #297 opm ---
    specs = [
        (
            "Government Payment for Annuitants, Employees Health and Life Insurance Benefits",
            V(m, 88),
        ),
        ("Postal Service Retiree Health Benefits Fund", V(m, 89)),
        ("Civil Service Retirement and Disability Fund", V(m, 90)),
        ("Employees Life Insurance Fund", V(m, 91)),
        (
            "Employees and Retired Employees Health Benefits Fund",
            V(m, 92),
        ),
        ("Other", V(m, 93)),
        ("Proprietary Receipts from the Public", V(m, 94)),
        (
            "Intrabudgetary Transactions--Postal Service Contributions",
            V(m, 96),
        ),
        (
            "Intrabudgetary Transactions--Civil Service Retirement and Disability Fund: Other",
            V(m, 98),
        ),
        ("Total--Office of Personnel Management", V(m, 99)),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-opm",
        "Office of Personnel Management",
        20,
        "USD millions. ...... and (**) cells omitted (not zero).",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #298 sba ---
    specs = [
        ("Salaries and Expenses", V(m, 101)),
        ("Business Loans Program", V(m, 102)),
        ("Disaster Loans Program", V(m, 103)),
        ("Other", V(m, 104)),
        ("Proprietary Receipts from the Public", V(m, 105)),
        ("Intrabudgetary Transactions", V(m, 106)),
        ("Total--Small Business Administration", V(m, 107)),
    ]
    n = len(specs)
    build_unit(
        "treasury-mts/2026-06-outlays-sba",
        "Small Business Administration",
        20,
        "USD millions. ...... and (**) cells omitted (not zero).",
        specs,
        total_rows={n},
        rollups=[(n, list(range(1, n)))],
    )

    # --- #299 social-security ---
    # June OASDI/DI totals include Payment to Railroad Retirement Account
    specs = [
        ("Payments to Social Security Trust Funds", V(m, 109)),
        ("Supplemental Security Income Program", V(m, 110)),
        (
            "Federal Old-Age and Survivors Insurance Trust Fund (Off-Budget) / Benefit Payments",
            V(m, 113),
        ),
        (
            "Federal Old-Age and Survivors Insurance Trust Fund (Off-Budget) / Administrative Expenses",
            V(m, 114),
        ),
        (
            "Federal Old-Age and Survivors Insurance Trust Fund (Off-Budget) / Payment to Railroad Retirement Account",
            V(m, 115),
        ),
        (
            "Total--Federal Old-Age and Survivors Insurance Trust Fund (Off-Budget)",
            V(m, 116),
        ),
        (
            "Federal Disability Insurance Trust Fund (Off-Budget) / Benefit Payments",
            V(m, 118),
        ),
        (
            "Federal Disability Insurance Trust Fund (Off-Budget) / Administrative Expenses",
            V(m, 119),
        ),
        (
            "Federal Disability Insurance Trust Fund (Off-Budget) / Payment to Railroad Retirement Account",
            V(m, 120),
        ),
        (
            "Total--Federal Disability Insurance Trust Fund (Off-Budget)",
            V(m, 121),
        ),
        ("Other", V(m, 123)),
        ("Proprietary Receipts from the Public / On-Budget", V(m, 125)),
        ("Proprietary Receipts from the Public / Off-Budget", V(m, 126)),
        ("Intrabudgetary Transactions / Off-Budget", V(m, 128)),
        ("Total--Social Security Administration", V(m, 129)),
    ]
    build_unit(
        "treasury-mts/2026-06-outlays-social-security",
        "Social Security Administration",
        20,
        "USD millions. ...... and (**) cells omitted (not zero). June OASDI/DI totals include Payment to Railroad Retirement Account lines.",
        specs,
        total_rows={6, 10, 15},
        rollups=[
            (6, [3, 4, 5]),
            (10, [7, 8, 9]),
            (15, [1, 2, 6, 10, 11, 12, 13, 14]),
        ],
    )

    # --- #300 grand-total-capstone ---
    # Total Outlays / On-Budget / Off-Budget with On+Off=Total per period column group
    # Columns: same 9-col Table 5 layout. Values at 253-255.
    specs = [
        ("Total Outlays", V(m, 253)),
        ("Total On-Budget", V(m, 254)),
        ("Total Off-Budget", V(m, 255)),
    ]
    # Relations: for each period, On + Off = Total (gross cols 1,4,7; applicable 2,5,8; net 3,6,9)
    # Also net identities on each total row when applicable present
    build_unit(
        "treasury-mts/2026-06-outlays-grand-total-capstone",
        "Table 5 grand-total capstone (On/Off/Total Outlays)",
        23,
        "USD millions. Capstone: Total Outlays = Total On-Budget + Total Off-Budget per column. ...... and (**) cells omitted (not zero).",
        specs,
        total_rows={1},
        rollups=[(1, [2, 3])],
    )

    print("done")


if __name__ == "__main__":
    main()
