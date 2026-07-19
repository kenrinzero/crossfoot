import json
import sys
from pathlib import Path
from decimal import Decimal

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from reconcile import check

UNITS = {}

# ==========================================
# 152: hhs-trans
# ==========================================
UNITS["2026-05-table6-schedule-c-hhs-trans"] = {
    "title": "Table 6. Schedule C — Federal Agency Borrowing (HHS, DHS, HUD, Interior, Labor, State, Transportation)",
    "page": 26, # spans 26-28, starts p26
    "unit_note": "USD millions. Borrowing from the US Treasury under HHS, DHS, HUD, Interior, Labor, State, and Transportation. Blank (dotted-leader) and less-than-500k (**) cells omitted per project convention.",
    "rows": [
        "Borrowing from the US Treasury: Department of Health and Human Services: Consumer Operated and Oriented Plan",
        "Borrowing from the US Treasury: Department of Health and Human Services: Consumer Operated and Oriented Plan Program Contingency Fund",
        "Borrowing from the US Treasury: Department of Homeland Security: National Flood Insurance Fund",
        "Borrowing from the US Treasury: Department of Homeland Security: Disaster Assistance Loan Fund",
        "Borrowing from the US Treasury: Department of Housing and Urban Development: Public and Indian Housing Programs: Low-Rent Public Housing - Loans and Other Expenses",
        "Borrowing from the US Treasury: Department of Housing and Urban Development: Public and Indian Housing Programs: Native Hawaiian Housing Loans",
        "Borrowing from the US Treasury: Department of Housing and Urban Development: Housing Programs: Emergency Homeowners' Relief Fund",
        "Borrowing from the US Treasury: Department of Housing and Urban Development: Housing Programs: Federal Housing Administration",
        "Borrowing from the US Treasury: Department of Housing and Urban Development: Housing Programs: Home Ownership Preservation Equity Fund",
        "Borrowing from the US Treasury: Department of Housing and Urban Development: Housing Programs: Green Retrofit Program for Multifamily Housing-Recovery Act",
        "Borrowing from the US Treasury: Department of the Interior: Bureau of Reclamation Loan Fund",
        "Borrowing from the US Treasury: Department of the Interior: Assistance to American Samoa Loan Fund",
        "Borrowing from the US Treasury: Department of Labor: Black Lung Disability Trust Fund",
        "Borrowing from the US Treasury: Department of State: Repatriation Loans",
        "Borrowing from the US Treasury: Department of Transportation: Federal Highway Administration: Transportation Infrastructure Finance and Innovation Fund",
        "Borrowing from the US Treasury: Department of Transportation: Federal Railroad Administration: Railroad Rehabilitation and Improvement Loan Fund",
        "Borrowing from the US Treasury: Department of Transportation: Maritime Administration: Maritime Guaranteed Loan (Title XI) Fund",
        "Borrowing from the US Treasury: Department of Transportation: Maritime Administration: Maritime Guaranteed Loan (Title XI) FFB Financing Account"
    ],
    "data": {
        0: [None, None, None, "290", "290", "290"],
        1: [None, None, None, "68", "68", "68"],
        2: [None, None, "2000", "22525", "22525", "22525"],
        3: ["1", "2", "5", "8", "9", "10"],
        4: [None, None, None, "36", "36", "36"],
        5: [None, None, None, "6", "6", "6"],
        6: [None, None, None, "3", "3", "3"],
        7: [None, None, None, "143968", "143968", "143968"],
        8: [None, None, None, "6", "6", "6"],
        9: [None, "-20", "71", "336", "317", "317"],
        10: [None, None, None, "21", "21", "21"],
        11: [None, None, None, "5", "6", "6"],
        12: [None, None, None, "5213", "5213", "5213"],
        13: [None, "1", "2", "7", "8", "8"],
        14: ["22", "1961", "2205", "25389", "27327", "27349"],
        15: ["9", "509", "601", "3027", "3527", "3536"],
        16: [None, None, None, "6", "6", "6"],
        17: [None, None, None, "8", "8", "8"]
    },
    "tols": {}
}

# ==========================================
# 153: treas-vets
# ==========================================
UNITS["2026-05-table6-schedule-c-treas-vets"] = {
    "title": "Table 6. Schedule C — Federal Agency Borrowing (Treasury, Veterans)",
    "page": 27, # spans 27-28
    "unit_note": "USD millions. Borrowing from the US Treasury under Treasury and Veterans Affairs. Blank and less-than-500k (**) cells omitted.",
    "rows": [
        "Borrowing from the US Treasury: Department of the Treasury: Departmental Offices: Community Development Financial Institutions Fund",
        "Borrowing from the US Treasury: Department of the Treasury: Departmental Offices: Temporary Credit and Liquidity Program",
        "Borrowing from the US Treasury: Department of the Treasury: Departmental Offices: Small Business Lending Financing Fund",
        "Borrowing from the US Treasury: Department of the Treasury: Departmental Offices: ESF - Economic Stabilization Program",
        "Borrowing from the US Treasury: Department of the Treasury: Federal Financing Bank Revolving Fund",
        "Borrowing from the US Treasury: Department of Veterans Affairs: Veterans Housing Benefit Program Fund",
        "Borrowing from the US Treasury: Department of Veterans Affairs: Native American Veteran Housing Fund",
        "Borrowing from the US Treasury: Department of Veterans Affairs: Vocational Rehabilitation Loan Fund"
    ],
    "data": {
        0: [None, "8", "11", "117", "125", "125"],
        1: [None, None, None, "898", "898", "898"],
        2: [None, None, None, "33", "33", "33"],
        3: [None, "-1208", "-1498", "2714", "1507", "1507"],
        4: ["348", "4127", "32636", "210939", "214718", "215066"],
        5: [None, "-219", "7250", "8948", "8729", "8729"],
        6: [None, "10", "3", "99", "108", "108"],
        7: [None, "1", None, None, "1", "1"]
    },
    "tols": {}
}

# ==========================================
# 154: epa-ind
# ==========================================
UNITS["2026-05-table6-schedule-c-epa-ind"] = {
    "title": "Table 6. Schedule C — Federal Agency Borrowing (EPA, International, SBA, Independent Agencies, Other)",
    "page": 27, # spans 27-28
    "unit_note": "USD millions. Borrowing from the US Treasury under EPA, International Assistance, SBA, Independent Agencies, and Other, plus the total borrowing lines for US Treasury and Federal Financing Bank (FFB) section totals. Blank and less-than-500k (**) cells omitted.",
    "rows": [
        "Borrowing from the US Treasury: Environmental Protection Agency: Water Infrastructure Finance and Innovation Loan Program",
        "Borrowing from the US Treasury: International Assistance Programs: International Security Assistance: Foreign Military Loan Program",
        "Borrowing from the US Treasury: International Assistance Programs: Agency for International Development: Development Credit Authority Loan Fund",
        "Borrowing from the US Treasury: International Assistance Programs: International Monetary Programs",
        "Borrowing from the US Treasury: International Assistance Programs: United States International Development Finance Corporation",
        "Borrowing from the US Treasury: Small Business Administration: Business Loan Fund",
        "Borrowing from the US Treasury: Small Business Administration: Disaster Loan Fund",
        "Borrowing from the US Treasury: Independent Agencies: Export-Import Bank of the United States",
        "Borrowing from the US Treasury: Independent Agencies: Federal Communications Commission: Spectrum Auction Loan Fund",
        "Borrowing from the US Treasury: Independent Agencies: Presidio Trust",
        "Borrowing from the US Treasury: Independent Agencies: Railroad Retirement Board: Social Security Equivalent Benefit Account",
        "Borrowing from the US Treasury: Other: Borrowing from the US Treasury - Other",
        "Total Borrowing from the US Treasury",
        "Total Borrowing from the Federal Financing Bank"
    ],
    "data": {
        0: ["327", "2049", "2573", "9721", "11442", "11769"],
        1: [None, None, "5884", "7852", "7852", "7852"],
        2: ["-189", "-189", "495", "781", "781", "592"],
        3: ["32", "7476", "3641", "4892", "12337", "12368"],
        4: ["82", "1895", "1395", "12678", "14491", "14573"],
        5: [None, "718", "425", "3503", "4221", "4221"],
        6: [None, "-1073", "-2169", "245833", "244760", "244760"],
        7: ["4", "756", "66", "9236", "9989", "9992"],
        8: [None, None, "3080", "3080", "3080", "3080"],
        9: [None, None, None, "245", "245", "245"],
        10: ["374", "3376", "3298", "4748", "7749", "8123"],
        11: [None, "1", None, "1", "2", "2"],
        12: ["-34241", "43463", "123376", "2201239", "2278943", "2244702"],
        13: ["346", "2993", "32387", "217753", "220400", "220746"]
    },
    "tols": {
        3: "1",  # International Monetary Programs
        7: "1"   # Export-Import Bank
    }
}

# ==========================================
# 155: schedule-d-federal-funds-agri-just
# ==========================================
UNITS["2026-05-table6-schedule-d-federal-funds-agri-just"] = {
    "title": "Table 6. Schedule D — Investments of Federal Government Accounts (Federal Funds: Agriculture through Justice)",
    "page": 29,
    "unit_note": "USD millions. Investments of Federal Funds under Agriculture through Justice. Blank and less-than-500k (**) cells omitted.",
    "rows": [
        "Federal Funds: Department of Agriculture",
        "Federal Funds: Department of Commerce",
        "Federal Funds: Department of Defense--Military Programs: Defense Cooperation Account",
        "Federal Funds: Department of Energy",
        "Federal Funds: Department of Health and Human Services",
        "Federal Funds: Department of Homeland Security",
        "Federal Funds: Department of Housing and Urban Development: Housing Programs: Federal Housing Administration Fund",
        "Federal Funds: Department of Housing and Urban Development: Government National Mortgage Association: Guarantees of Mortgage-Backed Securities",
        "Federal Funds: Department of the Interior",
        "Federal Funds: Department of Justice"
    ],
    "data": {
        0: [None, "11", "-89", "409", "419", "419"],
        1: [None, "2", "2", None, "2", "2"],
        2: [None, None, None, "10", "10", "10"],
        3: ["744", "6270", "6068", "80096", "85622", "86366"],
        4: ["74", "17532", "18207", None, "17458", "17532"],
        5: [None, None, "-4948", None, None, None],
        6: ["1248", "9771", "7726", "185047", "193570", "194818"],
        7: ["41", "1211", "2236", "29516", "30686", "30727"],
        8: ["62", "13", "1707", "32218", "32168", "32230"],
        9: ["1", "-2777", "-504", "3102", "324", "325"]
    },
    "tols": {}
}

# ==========================================
# 156: schedule-d-federal-funds-labor-totals
# ==========================================
UNITS["2026-05-table6-schedule-d-federal-funds-labor-totals"] = {
    "title": "Table 6. Schedule D — Investments of Federal Government Accounts (Federal Funds: Labor through Totals)",
    "page": 29, # spans 29-30
    "unit_note": "USD millions. Investments of Federal Funds under Labor through Totals. Blank and less-than-500k (**) cells omitted.",
    "rows": [
        "Federal Funds: Department of Labor",
        "Federal Funds: Department of State: Foreign Service Retirement and Disability Fund",
        "Federal Funds: Department of State: Other",
        "Federal Funds: Department of Transportation",
        "Federal Funds: Department of the Treasury",
        "Federal Funds: Department of Veterans Affairs: Veterans Reopened Insurance Fund",
        "Federal Funds: Department of Veterans Affairs: National Service Life Insurance",
        "Federal Funds: Department of Veterans Affairs: Servicemen'S Group Life Insurance Fund",
        "Federal Funds: Other Defense Civil Programs: Uniformed Services Retiree Health Care Fund",
        "Federal Funds: International Assistance Programs",
        "Federal Funds: Office of Personnel Management: Postal Service Contributions",
        "Federal Funds: Independent Agencies: Federal Deposit Insurance Corporation: Deposit Insurance Fund",
        "Federal Funds: Independent Agencies: Federal Deposit Insurance Corporation: FSLIC Resolution Fund",
        "Federal Funds: Independent Agencies: Federal Housing Finance Agency",
        "Federal Funds: Independent Agencies: National Credit Union Administration",
        "Federal Funds: Independent Agencies: Postal Service",
        "Federal Funds: Independent Agencies: Other: Treasury Securities",
        "Federal Funds: Other",
        "Total Treasury Securities",
        "Total Federal Funds"
    ],
    "data": {
        0: ["73", "1620", "2419", "73532", "75079", "75152"],
        1: ["6", "19", "19", "356", "369", "375"],
        2: [None, None, None, "21", "21", "21"],
        3: ["12", "76", "58", "2706", "2770", "2783"],
        4: ["-114", "2441", "7152", "27828", "30383", "30269"],
        5: ["-1", "-3", "-3", "19", "16", "16"],
        6: ["8", "72", "66", "152", "216", "224"],
        7: [None, "-24", "484", "4761", "4737", "4737"],
        8: ["3300", "39221", "28378", "416973", "452894", "456194"],
        9: ["22", "163", "395", "7067", "7208", "7230"],
        10: ["-421", "-3036", "-3108", "24067", "21453", "21032"],
        11: ["-156", "13328", "15009", "120552", "134036", "133880"],
        12: ["3", "26", "30", "1028", "1051", "1054"],
        13: ["-16", "58", "164", "303", "377", "361"],
        14: ["182", "1178", "1352", "25312", "26307", "26490"],
        15: ["248", "-1918", "-1029", "13708", "11542", "11789"],
        16: ["-14", "-59", "108", "13945", "13900", "13886"],
        17: ["-16", "3031", "2503", "1754", "4801", "4785"],
        18: ["5287", "88226", "84403", "1064480", "1147419", "1152706"],
        19: ["5287", "88226", "84403", "1064480", "1147419", "1152706"]
    },
    "tols": {
        3: "1",   # Department of Transportation
        5: "1",   # VA Veterans Reopened
        14: "1",  # NCUA
        15: "1"   # Postal Service
    }
}

# ==========================================
# 157: schedule-d-trust-funds
# ==========================================
UNITS["2026-05-table6-schedule-d-trust-funds"] = {
    "title": "Table 6. Schedule D — Investments of Federal Government Accounts (Trust Funds: Legislative through Grand Total)",
    "page": 29, # spans 29-30
    "unit_note": "USD millions. Investments of Trust Funds under Legislative through Grand Total. Blank and less-than-500k (**) cells omitted.",
    "rows": [
        "Trust Funds: Legislative Branch: Library of Congress",
        "Trust Funds: Legislative Branch: United States Tax Court",
        "Trust Funds: Legislative Branch: Other",
        "Trust Funds: Judicial Branch: Judicial Retirement Funds",
        "Trust Funds: Department of Agriculture",
        "Trust Funds: Department of Defense--Military Programs: Voluntary Separation Incentive Fund",
        "Trust Funds: Department of Defense--Military Programs: Other",
        "Trust Funds: Department of Health and Human Services: Federal Supplementary Medical Insurance Trust Fund",
        "Trust Funds: Department of Health and Human Services: Other",
        "Trust Funds: Department of Homeland Security",
        "Trust Funds: Department of the Interior",
        "Trust Funds: Department of Labor: Unemployment Trust Fund",
        "Trust Funds: Department of Labor: Other",
        "Trust Funds: Department of State: Foreign Service Retirement and Disability Fund",
        "Trust Funds: Department of State: Other",
        "Trust Funds: Department of Transportation: Airport and Airway Trust Fund",
        "Trust Funds: Department of Transportation: Highway Trust Fund",
        "Trust Funds: Department of the Treasury",
        "Trust Funds: Department of Veterans Affairs: General Post Fund, National Homes",
        "Trust Funds: Department of Veterans Affairs: National Service Life Insurance",
        "Trust Funds: Department of Veterans Affairs: United States Government Life Insurance Fund",
        "Trust Funds: Department of Veterans Affairs: Veterans Special Life Insurance Fund",
        "Trust Funds: Corps of Engineers",
        "Trust Funds: Other Defense Civil Programs: Military Retirement Fund",
        "Trust Funds: Other Defense Civil Programs: Other",
        "Trust Funds: Environmental Protection Agency",
        "Trust Funds: National Aeronautics and Space Administration",
        "Trust Funds: Office of Personnel Management: Civil Service Retirement and Disability Fund: Treasury Securities",
        "Trust Funds: Office of Personnel Management: Employees Life Insurance Fund",
        "Trust Funds: Office of Personnel Management: Employees and Retired Employees Health Benefits Fund",
        "Trust Funds: Social Security Administration: Federal Old-Age and Survivors Insurance Trust Fund",
        "Trust Funds: Social Security Administration: Federal Disability Insurance Trust Fund",
        "Trust Funds: Independent Agencies: Harry S Truman Scholarship Foundation",
        "Trust Funds: Independent Agencies: Japan-United States Friendship Commission",
        "Trust Funds: Independent Agencies: Railroad Retirement Board: Treasury Securities",
        "Trust Funds: Independent Agencies: Railroad Retirement Board: Agency Securities",
        "Trust Funds: Independent Agencies: Other: Treasury Securities",
        "Total Trust Funds: Treasury Securities",
        "Total Trust Funds: Agency Securities",
        "Total Trust Funds",
        "Grand Total"
    ],
    "data": {
        0: ["4", "19", "6", "69", "84", "88"],
        1: [None, None, None, "14", "14", "14"],
        2: [None, "4", "2", "35", "38", "38"],
        3: ["14", "256", "249", "2374", "2616", "2629"],
        4: [None, None, "1", "7", "7", "7"],
        5: [None, "-3", "2", "30", "27", "27"],
        6: ["13", "122", "-331", "698", "808", "820"],
        7: ["-675", "33217", "-33376", "153844", "187736", "187061"],
        8: ["-5465", "21132", "-4001", "257452", "284048", "278583"],
        9: ["44", "302", "476", "13125", "13384", "13427"],
        10: ["256", "355", "105", "886", "985", "1241"],
        11: ["18452", "12119", "5325", "89394", "83061", "101513"],
        12: ["-6", "-5", "-7", "73", "74", "68"],
        13: ["-59", "-212", "4", "22277", "22123", "22064"],
        14: [None, None, None, "46", "46", "46"],
        15: ["1101", "2837", "-464", "18571", "20308", "21409"],
        16: ["670", "-9864", "-6770", "68941", "58408", "59078"],
        17: ["-65", "95", "145", "4768", "4928", "4863"],
        18: ["64", "7", "26", "147", "91", "154"],
        19: ["-13", "-94", "-131", "402", "321", "308"],
        20: [None, None, None, "1", "1", "1"],
        21: ["-11", "-74", "-86", "543", "479", "469"],
        22: ["248", "1441", "716", "10688", "11881", "12129"],
        23: ["11538", "301090", "194315", "1806919", "2096471", "2108009"],
        24: ["-17", "-77", "-46", "891", "830", "813"],
        25: ["166", "278", "164", "13315", "13427", "13593"],
        26: [None, None, None, "16", "16", "16"],
        27: ["-5333", "-18573", "-47944", "1106317", "1093077", "1087744"],
        28: ["48", "1380", "1559", "57976", "59308", "59356"],
        29: ["-262", "-1150", "421", "23340", "22451", "22189"],
        30: ["-30096", "-132016", "-115917", "2400808", "2298888", "2268792"],
        31: ["2721", "29832", "23280", "215352", "242462", "245183"],
        32: [None, None, "19", "56", "56", "56"],
        33: [None, "-1", None, "35", "34", "34"],
        34: ["-200", "-185", "309", "3516", "3531", "3331"],
        35: [None, "-3", "1", "8", "4", "4"],
        36: ["215", "65", "-410", "1858", "1707", "1922"],
        37: ["-6648", "242295", "17639", "6274783", "6523727", "6517078"],
        38: [None, "-3", "1", "8", "4", "4"],
        39: ["-6648", "242292", "17640", "6274791", "6523731", "6517083"],
        40: ["-1361", "330517", "102043", "7339271", "7671150", "7669789"]
    },
    "tols": {
        3: "1",   # Judicial Retirement
        6: "1",   # DoD Other
        9: "1",   # DHS
        18: "1",  # VA General Post Fund
        21: "1",  # VA Special
        37: "1"   # Total Trust Funds Treasury
    }
}

# ==========================================
# 158: schedule-e-guaranteed
# ==========================================
UNITS["2026-05-table6-schedule-e-guaranteed"] = {
    "title": "Table 6. Schedule E — Guaranteed Loan Financing Activity (all agencies)",
    "page": 31, # spans 31-32
    "unit_note": "USD millions. Guaranteed Loan Financing Activity. Blank and less-than-500k (**) cells omitted.",
    "rows": [
        "Guaranteed Loan Financing Activity: Department of Agriculture: Office of the Secretary: Food Supply Chain and Agriculture Pandemic Response",
        "Guaranteed Loan Financing Activity: Department of Agriculture: Farm Service Agency: Commodity Credit Corporation Export Fund",
        "Guaranteed Loan Financing Activity: Department of Agriculture: Farm Service Agency: Agricultural Credit Insurance Fund",
        "Guaranteed Loan Financing Activity: Department of Agriculture: Rural Housing Service: Rural Community Facility Loans",
        "Guaranteed Loan Financing Activity: Department of Agriculture: Rural Housing Service: Rural Housing Insurance Fund",
        "Guaranteed Loan Financing Activity: Department of Agriculture: Rural Business - Cooperative Service: Rural Business and Industry Loans",
        "Guaranteed Loan Financing Activity: Department of Agriculture: Renewable Energy Guaranteed Loan Account",
        "Guaranteed Loan Financing Activity: Department of Agriculture: Biorefinery Assistance Loan Account",
        "Guaranteed Loan Financing Activity: Department of Agriculture: Rural Utilities Service: Rural Water and Waste Disposal Fund",
        "Guaranteed Loan Financing Activity: Department of Agriculture: National Forest System",
        "Guaranteed Loan Financing Activity: Department of Commerce: General Administration: Emergency Oil, Gas, and Steel Account",
        "Guaranteed Loan Financing Activity: Department of Defense--Military Programs",
        "Guaranteed Loan Financing Activity: Department of Education: Office of Student Financial Assistance: Federal Family Education Loans",
        "Guaranteed Loan Financing Activity: Department of Energy: Title 17 Innovative Technology Loans",
        "Guaranteed Loan Financing Activity: Department of Energy: Tribal Energy Direct Loan Financing Account",
        "Guaranteed Loan Financing Activity: Department of Health and Human Services: Health Resources and Services Administration: Health Center Loans",
        "Guaranteed Loan Financing Activity: Department of Health and Human Services: Health Resources and Services Administration: Health Education Assitance Loans",
        "Guaranteed Loan Financing Activity: Department of Housing and Urban Development: Public and Indian Housing Programs: Indian Housing Loans",
        "Guaranteed Loan Financing Activity: Department of Housing and Urban Development: Public and Indian Housing Programs: Native Hawaiian Housing Loans",
        "Guaranteed Loan Financing Activity: Department of Housing and Urban Development: Community Planning and Development: Community Development Loans",
        "Guaranteed Loan Financing Activity: Department of Housing and Urban Development: Housing Programs: FHA-Mutual Mortgage Insurance Loans",
        "Guaranteed Loan Financing Activity: Department of Housing and Urban Development: Housing Programs: FHA-General and Special Risk Fund",
        "Guaranteed Loan Financing Activity: Department of Housing and Urban Development: Housing Programs: Home Ownership Preservation Entity Fund",
        "Guaranteed Loan Financing Activity: Department of Housing and Urban Development: Guarantees of Mortgage-Backed Securities",
        "Guaranteed Loan Financing Activity: Department of the Interior: Bureau of Indian Affairs and Bureau of Indian Education",
        "Guaranteed Loan Financing Activity: Department of Transportation: Maritime Administration: Maritime Guaranteed Loan (Title XI) Fund",
        "Guaranteed Loan Financing Activity: Department of Veterans Affairs: Veterans Benefits Administration: Veterans Housing Benefit Program Fund",
        "Guaranteed Loan Financing Activity: Department of Veterans Affairs: Veterans Benefits Administration: Other",
        "Guaranteed Loan Financing Activity: International Assistance Programs: Agency for International Development: Ukraine Export Credit Insurance Fund",
        "Guaranteed Loan Financing Activity: International Assistance Programs: Agency for International Development: Loan Guarantees to Israel",
        "Guaranteed Loan Financing Activity: International Assistance Programs: Agency for International Development: Urban and Environmental Credit Guaranteed Loans",
        "Guaranteed Loan Financing Activity: International Assistance Programs: Agency for International Development: Development Credit Authority Loan Fund",
        "Guaranteed Loan Financing Activity: International Assistance Programs: Agency for International Development: Tunisia Loan Fund",
        "Guaranteed Loan Financing Activity: International Assistance Programs: Overseas Private Investment Corporation",
        "Guaranteed Loan Financing Activity: International Assistance Programs: United States International Development Finance Corporation",
        "Guaranteed Loan Financing Activity: International Assistance Programs: United States International Development Finance Corporation: Urban and Environmental Credit",
        "Guaranteed Loan Financing Activity: Small Business Administration: Business Loan Fund",
        "Guaranteed Loan Financing Activity: Independent Agencies: Export-Import Bank of the United States",
        "Net Activity, Guaranteed Loan Financing"
    ],
    "data": {
        0: [None, "1", "25", "6", "7", "7"],
        1: ["10", "-1", "-37", "-1", "-12", "-2"],
        2: ["-301", "-308", "307", "202", "194", "-107"],
        3: [None, "-1", "-2", "-4", "-5", "-5"],
        4: ["-24", "-62", "-92", "1869", "1831", "1807"],
        5: ["-6", "44", "106", "171", "220", "214"],
        6: ["2", "3", "3", "15", "17", "19"],
        7: [None, "-1", "-8", "21", "20", "20"],
        8: [None, None, None, "-25", "-25", "-25"],
        9: [None, "-2", None, "-3", "-4", "-4"],
        10: [None, None, None, "5", "5", "5"],
        11: [None, None, None, "-25", "-25", "-25"],
        12: ["112", "2233", "2384", "-14238", "-12116", "-12004"],
        13: ["11", "11", "-1", "-81", "-81", "-70"],
        14: [None, None, "-1", "-3", "-3", "-2"],
        15: [None, None, None, "-3", "-3", "-3"],
        16: [None, None, None, "-70", "-70", "-70"],
        17: ["-1", "-5", None, "-29", "-33", "-34"],
        18: [None, None, "-1", "-1", "-1", "-1"],
        19: [None, None, None, "-1", "-2", "-2"],
        20: ["-80", "-1436", "388", "91844", "90488", "90408"],
        21: ["-50", "-831", "-625", "12343", "11562", "11513"],
        22: [None, None, None, "3", "3", "3"],
        23: ["-176", "-1413", "-1096", "-4411", "-5648", "-5824"],
        24: [None, "-1", "-3", "-45", "-46", "-46"],
        25: [None, "2", None, "-217", "-215", "-215"],
        26: ["-73", "-1356", "4181", "-7826", "-9109", "-9182"],
        27: ["7", "6", "-19", "-20", "-20", "-13"],
        28: [None, None, None, "-267", "-267", "-267"],
        29: [None, None, None, "-612", "-612", "-612"],
        30: [None, None, None, "-38", "-38", "-38"],
        31: [None, None, None, "-99", "-99", "-99"],
        32: [None, None, None, "-595", "-595", "-595"],
        33: [None, None, None, "278", "278", "278"],
        34: ["-15", "163", "-116", "-253", "-75", "-90"],
        35: [None, "2", "2", "21", "23", "23"],
        36: ["-20", "204", "975", "-53662", "-53439", "-53458"],
        37: ["-91", "-414", "-302", "-6197", "-6520", "-6611"],
        38: ["-694", "-3161", "6067", "18056", "15588", "14894"]
    },
    "tols": {
        21: "1",  # HUD General & Special Risk
        36: "1"   # SBA Business
    }
}

# ==========================================
# 159: schedule-e-direct-part1
# ==========================================
UNITS["2026-05-table6-schedule-e-direct-part1"] = {
    "title": "Table 6. Schedule E — Direct Loan Financing Activity (Agriculture through Energy)",
    "page": 32,
    "unit_note": "USD millions. Direct Loan Financing Activity under Agriculture through Energy. Blank and less-than-500k (**) cells omitted.",
    "rows": [
        "Direct Loan Financing Activity: Department of Agriculture: Farm Service Agency: Agricultural Credit Insurance Fund",
        "Direct Loan Financing Activity: Department of Agriculture: Farm Service Agency: Farm Storage Facility Loans",
        "Direct Loan Financing Activity: Department of Agriculture: Rural Housing Service: Rural Community Facility Loans Fund",
        "Direct Loan Financing Activity: Department of Agriculture: Rural Housing Service: Rural Housing Insurance Fund",
        "Direct Loan Financing Activity: Department of Agriculture: Rural Housing Service: Multifamily Housing Revitalization Loan Account",
        "Direct Loan Financing Activity: Department of Agriculture: Rural Business - Cooperative Service: Rural Business and Industry Loan Fund",
        "Direct Loan Financing Activity: Department of Agriculture: Rural Business - Cooperative Service: Rural Development Loan Fund",
        "Direct Loan Financing Activity: Department of Agriculture: Rural Business - Cooperative Service: Rural Economic Development Loan Fund",
        "Direct Loan Financing Activity: Department of Agriculture: Rural Business - Cooperative Service: Rural Microenterprise Investment Loans",
        "Direct Loan Financing Activity: Department of Agriculture: Rural Utilities Service: Rural Water and Waste Disposal Loans",
        "Direct Loan Financing Activity: Department of Agriculture: Rural Utilities Service: Rural Electrification and Telecommunications Fund",
        "Direct Loan Financing Activity: Department of Agriculture: Rural Utilities Service: Rural Telephone Bank",
        "Direct Loan Financing Activity: Department of Agriculture: Rural Utilities Service: Distance Learning and Telemedicine Program",
        "Direct Loan Financing Activity: Department of Agriculture: Rural Utilities Service: Rural Development Insurance Fund",
        "Direct Loan Financing Activity: Department of Agriculture: Foreign Agricultural Service: P.L. 480 Direct Loan Fund",
        "Direct Loan Financing Activity: Department of Agriculture: Foreign Agricultural Service: International Debt Reduction",
        "Direct Loan Financing Activity: Department of Commerce: National Oceanic and Atmospheric Administration: Fisheries Finance",
        "Direct Loan Financing Activity: Department of Defense--Military Programs",
        "Direct Loan Financing Activity: Department of Education: Office of Postsecondary Education: College Housing and Academic Facilities Loans",
        "Direct Loan Financing Activity: Department of Education: Office of Postsecondary Education: Historically Black College and University Capital Financing Fund",
        "Direct Loan Financing Activity: Department of Education: Office of Student Financial Assistance: Federal Direct Student Loans",
        "Direct Loan Financing Activity: Department of Education: Office of Student Financial Assistance: Teach Grant Loans",
        "Direct Loan Financing Activity: Department of Education: Office of Student Financial Assistance: Temporary Student Loan Purchase Authority",
        "Direct Loan Financing Activity: Department of Energy: Advanced Technology Vehicles Manufacturing Loans",
        "Direct Loan Financing Activity: Department of Energy: Title 17 Innovative Technology Loans"
    ],
    "data": {
        0: ["-20", "-15", "528", "18613", "18618", "18598"],
        1: ["-5", "-50", "8", "1475", "1430", "1425"],
        2: ["20", "-57", "365", "12622", "12545", "12566"],
        3: ["-82", "-761", "-332", "15455", "14775", "14693"],
        4: [None, None, None, "524", "524", "524"],
        5: [None, None, "-2", "-2", "-2", "-2"],
        6: ["-1", "-12", "-8", "234", "223", "222"],
        7: ["-1", "-5", "7", "225", "221", "219"],
        8: [None, "-1", "-1", "37", "36", "36"],
        9: ["-8", "-73", "248", "14155", "14091", "14082"],
        10: ["235", "1072", "2575", "65442", "66279", "66514"],
        11: [None, "-1", "-1", "35", "34", "34"],
        12: ["7", "32", "26", "670", "695", "703"],
        13: [None, None, None, "1065", "1065", "1065"],
        14: [None, "-37", "-18", "142", "104", "105"],
        15: ["-3", "-6", "-34", "-209", "-212", "-215"],
        16: ["27", "8", "-27", "442", "423", "450"],
        17: ["-8", "966", "-100", "2038", "3012", "3004"],
        18: [None, None, None, "1", "1", "1"],
        19: ["51", "280", "175", "838", "1066", "1117"],
        20: ["-837", "-6768", "10693", "856586", "850654", "849818"],
        21: ["2", "3", "9", "438", "439", "442"],
        22: ["66", "-837", "-568", "23931", "23028", "23093"],
        23: ["378", "1391", "8761", "9655", "10668", "11046"],
        24: ["81", "1891", "2679", "18294", "20104", "20185"]
    },
    "tols": {
        2: "1",   # Rural Community Facility
        7: "1",   # Rural Econ Dev
        9: "1",   # Rural Water
        12: "1",  # Distance Learning
        20: "1",  # Federal Direct Student
        21: "1",  # Teach Grant
        22: "1"   # Temporary Student Loan
    }
}

# ==========================================
# 160: schedule-e-direct-part2
# ==========================================
UNITS["2026-05-table6-schedule-e-direct-part2"] = {
    "title": "Table 6. Schedule E — Direct Loan Financing Activity (HHS through Independent Agencies & Totals)",
    "page": 32, # spans 32-33
    "unit_note": "USD millions. Direct Loan Financing Activity under HHS through Independent Agencies & Totals. Blank and less-than-500k (**) cells omitted.",
    "rows": [
        "Direct Loan Financing Activity: Department of Health and Human Services: Consumer Operated and Oriented Plan",
        "Direct Loan Financing Activity: Department of Health and Human Services: Consumer Operated and Oriented Plan Program Contingency Fund",
        "Direct Loan Financing Activity: Department of Homeland Security: Disaster Assistance Loan Fund",
        "Direct Loan Financing Activity: Department of Housing and Urban Development: Housing Programs: Emergency Homeowners' Relief Fund",
        "Direct Loan Financing Activity: Department of Housing and Urban Development: Housing Programs: FHA-General and Special Risk Fund",
        "Direct Loan Financing Activity: Department of Housing and Urban Development: Housing Programs: Green Retrofit Program for Multifamily Housing Fund",
        "Direct Loan Financing Activity: Department of the Interior: Bureau of Reclamation",
        "Direct Loan Financing Activity: Department of the Interior: Assistance to American Samoa Loan Fund",
        "Direct Loan Financing Activity: Department of State: Administration of Foreign Affairs: Repatriation Loans",
        "Direct Loan Financing Activity: Department of Transportation: Federal Highway Administration: Transportation Infrastructure Finance and Innovation Fund",
        "Direct Loan Financing Activity: Department of Transportation: Federal Highway Administration: Tiger Tifia Loan Fund",
        "Direct Loan Financing Activity: Department of Transportation: Federal Railroad Administration: Railroad Rehabilitation and Improvement Loan Fund",
        "Direct Loan Financing Activity: Department of Transportation: Maritime Administration: Maritime Guaranteed Loan (Title XI) FFB Financing Account",
        "Direct Loan Financing Activity: Department of the Treasury: Departmental Offices: Community Development Financial Institutions Fund",
        "Direct Loan Financing Activity: Department of the Treasury: Departmental Offices: GSE Mortgage-Backed Securities Purchase Program",
        "Direct Loan Financing Activity: Department of the Treasury: Departmental Offices: Temporary Credit and Liquidity Program",
        "Direct Loan Financing Activity: Department of the Treasury: Departmental Offices: Small Business Lending Program",
        "Direct Loan Financing Activity: Department of the Treasury: Departmental Offices: ESF - Economic Stabilization Program",
        "Direct Loan Financing Activity: Department of Veterans Affairs: Veterans Benefits Administration: Veterans Housing Benefit Program Fund",
        "Direct Loan Financing Activity: Department of Veterans Affairs: Veterans Benefits Administration: Native American Veteran Housing Fund",
        "Direct Loan Financing Activity: Environmental Protection Agency: Water Infrastructure Finance and Innovation Loan Program",
        "Direct Loan Financing Activity: International Assistance Programs: International Security Assistance: Foreign Military Loan Program",
        "Direct Loan Financing Activity: International Assistance Programs: Agency for International Development: Development Credit Authority Loan Fund",
        "Direct Loan Financing Activity: International Assistance Programs: Agency for International Development: Sovereign Credit Direct Loan Financing Account",
        "Direct Loan Financing Activity: International Assistance Programs: Overseas Private Investment Corporation",
        "Direct Loan Financing Activity: International Assistance Programs: International Monetary Programs",
        "Direct Loan Financing Activity: International Assistance Programs: United States International Development Finance Corporation",
        "Direct Loan Financing Activity: International Assistance Programs: United States International Development Finance Corporation: International Debt Reduction",
        "Direct Loan Financing Activity: Small Business Administration: Business Loan Fund",
        "Direct Loan Financing Activity: Small Business Administration: Disaster Loan Fund",
        "Direct Loan Financing Activity: Independent Agencies: Export-Import Bank of the United States",
        "Net Activity, Direct Loan Financing"
    ],
    "data": {
        0: [None, "-32", "-30", "-34", "-66", "-66"],
        1: [None, None, "-34", "12", "12", "12"],
        2: ["-9", "-24", "-42", "-188", "-204", "-212"],
        3: [None, None, "-1", "2", "2", "2"],
        4: ["22", "311", "7", "3763", "4053", "4074"],
        5: ["1", "10", "5", "27", "36", "36"],
        6: [None, None, "-1", "22", "22", "22"],
        7: ["-1", "-1", "-1", "5", "5", "5"],
        8: [None, "-2", "-1", "2", "-1", None],
        9: ["-19", "1464", "1305", "21855", "23338", "23319"],
        10: [None, "-1", "-1", "60", "59", "59"],
        11: ["-10", "372", "521", "2553", "2935", "2925"],
        12: ["-1", "-54", "-12", "299", "246", "245"],
        13: ["-1", "-5", "130", "1575", "1572", "1570"],
        14: [None, None, None, "4613", "4613", "4613"],
        15: ["-29", "-94", "-41", "876", "811", "782"],
        16: [None, "-2", "-3", "-105", "-107", "-107"],
        17: ["-834", "-2104", "-2741", "2371", "1102", "268"],
        18: ["-61", "-546", "5960", "8475", "7990", "7929"],
        19: ["1", "-2", "-5", "73", "70", "71"],
        20: ["-9", "-97", "-73", "5207", "5119", "5110"],
        21: ["42", "-102", "-16", "-60", "-204", "-162"],
        22: ["-189", "-192", "494", "781", "778", "589"],
        23: ["-267", "-267", "19465", "19606", "19606", "19340"],
        24: [None, None, None, "2902", "2902", "2902"],
        25: ["-21", "7325", "3588", "4615", "11960", "11939"],
        26: ["-350", "-303", "69", "8169", "8217", "7866"],
        27: ["-23", "-51", "-75", "-360", "-389", "-411"],
        28: ["-2", "-15", "-9", "64", "51", "49"],
        29: ["-1548", "-13268", "-12161", "229683", "217963", "216414"],
        30: ["-16", "-786", "-688", "3650", "2879", "2863"],
        31: ["-3421", "-11446", "40591", "1363045", "1355019", "1351598"]
    },
    "tols": {
        2: "1",   # DHS Disaster Assistance
        4: "1",   # HUD General Risk
        5: "1",   # HUD Green Retrofit
        7: "1",   # Interior American Samoa
        13: "1",  # Treasury CDFI
        23: "1",  # AID Sovereign
        26: "1",  # US IDFC
        27: "1",  # US IDFC Debt
        29: "1"   # SBA Disaster
    }
}

COLUMNS = [
    {"index": 1, "label": "This Month (Transactions)"},
    {"index": 2, "label": "Fiscal Year to Date This Year (Transactions)"},
    {"index": 3, "label": "Fiscal Year to Date Prior Year (Transactions)"},
    {"index": 4, "label": "Beginning of This Year (Account Balance)"},
    {"index": 5, "label": "Close of This Month — open/prior (Account Balance)"},
    {"index": 6, "label": "Close of This Month — end (Account Balance)"}
]

for table_id, cfg in UNITS.items():
    rows_def = [{"index": i, "label": r} for i, r in enumerate(cfg["rows"], 1)]
    cells = []
    relations = []
    
    # We build a list of target cells and source cells to assign roles correctly.
    targets = set()
    sources = set()
    
    # Identify relations: row-wise roll forwards
    # relation is built for row idx (0-indexed) if col 1, col 5, col 6 are non-None
    for idx, vals in cfg["data"].items():
        if vals[0] is not None and vals[4] is not None and vals[5] is not None:
            # We have a roll-forward relation: rXc5 + rXc1 = rXc6
            row_idx = idx + 1
            targets.add((row_idx, 6))
            sources.add((row_idx, 1))
            sources.add((row_idx, 5))
            
            rel = {
                "type": "sum",
                "sources": [f"r{row_idx}c5", f"r{row_idx}c1"],
                "target": f"r{row_idx}c6",
                "note": f"balance roll-forward: begin-month + this-month = end-month ({cfg['rows'][idx][:40]})"
            }
            if idx in cfg["tols"]:
                rel["tol"] = cfg["tols"][idx]
                rel["why"] = 'Page prints: "Note: Details may not add to totals due to rounding."'
            relations.append(rel)
            
    # Now build cells
    for idx, vals in cfg["data"].items():
        row_idx = idx + 1
        for col_idx, val in enumerate(vals, 1):
            if val is None:
                continue
            
            cell_id = f"r{row_idx}c{col_idx}"
            cell = {
                "id": cell_id,
                "row": row_idx,
                "col": col_idx,
                "value": val
            }
            
            # Role assignment
            if (row_idx, col_idx) in targets:
                cell["role"] = "total"
            elif (row_idx, col_idx) in sources:
                cell["role"] = "leaf"
            else:
                cell["role"] = "standalone"
                cell["why"] = "No multi-source arithmetic partner in this unit (schema minItems:2)"
            cells.append(cell)
            
    doc = {
        "table_id": table_id,
        "source": {
            "path": "sources/treasury-mts/mts-202605.pdf",
            "table": cfg["title"],
            "page": cfg["page"],
            "title": cfg["title"],
            "period": "May FY2026"
        },
        "unit_note": cfg["unit_note"],
        "columns": COLUMNS,
        "rows": rows_def,
        "cells": cells,
        "relations": relations
    }
    
    out_path = root / f"tables/treasury-mts/{table_id}.cells.json"
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
        
    print(f"Wrote {table_id}.cells.json: {len(cells)} cells, {len(relations)} relations")
