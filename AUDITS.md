# Crossfoot — Audit Logs

This file logs the non-arithmetic spot audits conducted on every 10th shipped transcription unit, as required by the Crossfoot Design Contract (DESIGN.md § 6). Spot audits verify that metadata, row/column labels, period designations, units, and sampled cell values are correct against the original vendored source documents. 

Audits must be performed by a different agent than the unit's transcriber.

---

## Spot-Audit: Unit 10 — Apparel + Transportation

- **Audit Date:** 2026-07-13
- **Auditor:** Antigravity (Gemini 3.5 Flash)
- **Transcriber:** Hunyuan/OpenClaw (commit `0e42a46`)
- **Table ID:** [bls-cpi/relative-importance-2024-apparel-transportation](file:///C:/Users/kenrin/Project/crossfoot/tables/bls-cpi/relative-importance-2024-apparel-transportation.cells.json)
- **Source Document:** [relative-importance-2024.htm](file:///C:/Users/kenrin/Project/crossfoot/sources/bls-cpi/relative-importance-2024.htm)
- **Status:** **GREEN** (All verification checks passed with 100% accuracy)

### 1. Metadata Verification
- **Table Title:** "Table 1 (2023 Weights). Relative importance of components in the Consumer Price Indexes: U.S. city average, December 2024"
  - *Result:* **PASS** (Matches verbatim in HTML `<title>` and table header text)
- **Period:** "December 2024"
  - *Result:* **PASS** (Matches the date in the source headers)
- **Units / Scale:** "Relative importance as percent of All items."
  - *Result:* **PASS** (Matched against the source structure and rounding rationale note)

### 2. Layout, Row, and Column Labels Verification
- **Columns:**
  - Column 1: "U.S. City Average, CPI-U"
  - Column 2: "U.S. City Average, CPI-W"
  - *Result:* **PASS** (Matches source HTML headers exactly)
- **Rows:** 
  - Checked all 54 transcribed rows side-by-side against the HTML segments. Apparel starts at row index 151 and Transportation starts at row index 177 in the parsed HTM (excluding the blank greenbar separator at segment 177). 
  - *Result:* **PASS** (All 54 row labels match the source text exactly, with zero mismatches or CJK/escaping errors)

### 3. Sampled Cells Verification (10 Randomly Sampled Cells)

We selected a randomized sample of 10 cells across the table's range (using seed 42) and verified them byte-for-byte against the original source HTM:

| Cell ID | Row Label | Column Label | Role | JSON Value | Source HTML Value | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `r41c2` | Motor vehicle body work | U.S. City Average, CPI-W | leaf | `0.052` | `0.052` | **PASS** |
| `r8c1` | Unsampled men's apparel | U.S. City Average, CPI-U | leaf | `0.015` | `0.015` | **PASS** |
| `r2c2` | Men's and boys' apparel | U.S. City Average, CPI-W | total | `0.821` | `0.821` | **PASS** |
| `r48c1` | Parking and other fees | U.S. City Average, CPI-U | leaf | `0.198` | `0.198` | **PASS** |
| `r18c2` | Footwear | U.S. City Average, CPI-W | total | `0.700` | `0.700` | **PASS** |
| `r16c2` | Unsampled women's apparel | U.S. City Average, CPI-W | leaf | `0.013` | `0.013` | **PASS** |
| `r15c1` | Women's underwear, nightwear, swimwear, and accessories | U.S. City Average, CPI-U | leaf | `0.301` | `0.301` | **PASS** |
| `r9c2` | Boys' apparel | U.S. City Average, CPI-W | leaf | `0.176` | `0.176` | **PASS** |
| `r7c2` | Men's pants and shorts | U.S. City Average, CPI-W | leaf | `0.170` | `0.170` | **PASS** |
| `r44c1` | Unsampled service policies | U.S. City Average, CPI-U | leaf | `0.062` | `0.062` | **PASS** |

### 4. Audit Conclusion
The transcription of `bls-cpi/relative-importance-2024-apparel-transportation` by `Hunyuan/OpenClaw` is clean and byte-faithful. No non-arithmetic errors, transposition mistakes, or label mismatches were found.

---

## Spot-Audit: Unit 20 — Executive Office of the President (Treasury MTS Table 5, Outlays)

- **Audit Date:** 2026-07-14
- **Auditor:** Claude Opus 4.8
- **Transcriber:** Codex (commit `312e269`)
- **Table ID:** [treasury-mts/2026-05-outlays-eop](file:///C:/Users/kenrin/Project/crossfoot/tables/treasury-mts/2026-05-outlays-eop.cells.json)
- **Source Document:** [mts-202605.pdf](file:///C:/Users/kenrin/Project/crossfoot/sources/treasury-mts/mts-202605.pdf), page 19 (Executive Office of the President section)
- **Method:** pypdfium2 page render (scale 3.0) cross-checked against the `(cid:NN)`→`chr(NN+29)`-decoded text layer.
- **Status:** **GREEN** (all verification checks passed)

### 1. Metadata Verification
- **Table Title:** "Table 5. Outlays of the U.S. Government, May 2026 and Other Periods"
  - *Result:* **PASS** (matches the page header verbatim; page prints "- Continued")
- **Period:** "May FY2026 (This Month = May 2026; Current FYTD = Oct 2025 - May 2026; Prior FYTD = Oct 2024 - May 2025)"
  - *Result:* **PASS** (matches the three period column-group headers)
- **Units / Scale:** USD millions ("[$ millions]" per table header)
  - *Result:* **PASS**

### 2. Layout, Row, and Column Labels Verification
- **Columns (9):** This Month / Current FYTD / Prior FYTD, each × Gross Outlays · Applicable Receipts · Outlays[net].
  - *Result:* **PASS** (matches the source's two-tier column header exactly)
- **Rows (7):** The White House; Office of Management and Budget; Unanticipated Needs; Other; Proprietary Receipts from the Public; Intrabudgetary Transactions; Total--Executive Office of the President.
  - *Result:* **PASS** (all 7 labels match the render exactly; no dropped or reordered rows)
- **Omission conventions:** `......` and `(**)` cells correctly omitted (Other Prior-FYTD Applicable `(**)`; Proprietary This-Month Applicable/Outlays `(**)`; Intrabudgetary This-Month Gross/Outlays `(**)`; Total This-Month Applicable `(**)`). Single-source Applicable column (only Proprietary) handled per the plan addendum: `r5c5`/`r5c8` standalone with `why`, section-total applicables (`r7c5`/`r7c8`) covered by the total-row net identity.
  - *Result:* **PASS**

### 3. Sampled Cells Verification (10 sampled cells, spanning rows/columns, negatives, standalone, and total)

Re-read from the page-19 render and confirmed against the JSON:

| Cell ID | Row Label | Column Label | Role | JSON Value | Source (render) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `r1c7` | The White House | Prior FYTD / Gross Outlays | leaf | `50` | `50` | **PASS** |
| `r2c4` | Office of Management and Budget | Current FYTD / Gross Outlays | leaf | `71` | `71` | **PASS** |
| `r3c1` | Unanticipated Needs | This Month / Gross Outlays | leaf | `-3` | `-3` | **PASS** |
| `r3c9` | Unanticipated Needs | Prior FYTD / Outlays | leaf | `15` | `15` | **PASS** |
| `r4c4` | Other | Current FYTD / Gross Outlays | leaf | `-77` | `-77` | **PASS** |
| `r5c5` | Proprietary Receipts from the Public | Current FYTD / Applicable Receipts | standalone | `1000` | `1,000` | **PASS** |
| `r5c9` | Proprietary Receipts from the Public | Prior FYTD / Outlays | leaf | `-500` | `-500` | **PASS** |
| `r6c7` | Intrabudgetary Transactions | Prior FYTD / Gross Outlays | leaf | `2` | `2` | **PASS** |
| `r7c6` | Total--Executive Office of the President | Current FYTD / Outlays | total | `-961` | `-961` | **PASS** |
| `r7c8` | Total--Executive Office of the President | Prior FYTD / Applicable Receipts | leaf | `500` | `500` | **PASS** |

### 4. Audit Conclusion
The transcription of `treasury-mts/2026-05-outlays-eop` by `Codex` is clean and faithful to the source. Metadata, all 7 row labels, the 9-column model, the `......`/`(**)` omission conventions, and all 10 sampled values match the page-19 render with zero discrepancies. No footnote-glue affects this section. **GREEN.**

### 5. Batch note — full Table-5 cap-fit tier cross-check
Alongside this formal audit, an independent positioned-word source cross-check was run over the entire 13-unit Table-5 cap-fit tier (corpus #14–26): for each unit, the multiset of transcribed cell values was compared to the numeric tokens printed in that section on the source page(s). **12/13 matched exactly.** The one flag, `treasury-mts/2026-05-outlays-other-defense-civil` (Codex, `8a3cd1a`), resolves to two text-layer footnote-glued cells that were **render-verified correct** (Other Current-FYTD Gross/Outlays `¹300`; Proprietary Current-FYTD Applicable `²24` — superscript footnote markers from p. 23 glued in the text layer only), plus a page-18 footer artifact of the checker's page-spanning logic. No transcription defect found in any unit. reconcile is GREEN with 0 warnings across all 13; pytest 10/10.

---

## Spot-Audit: Unit 30 — Department of Energy (Treasury MTS Table 5, Outlays)

- **Audit Date:** 2026-07-15
- **Auditor:** Grok (xAI / Grok Build)
- **Transcriber:** Claude Opus 4.8 (commit `46b4afc`)
- **Table ID:** [treasury-mts/2026-05-outlays-energy](file:///C:/Users/kenrin/Project/crossfoot/tables/treasury-mts/2026-05-outlays-energy.cells.json)
- **Source Document:** [mts-202605.pdf](file:///C:/Users/kenrin/Project/crossfoot/sources/treasury-mts/mts-202605.pdf), pages 12–13 (Department of Energy section; NNSA + Environmental and Other Defense Activities on p12, Energy Programs onward on p13)
- **Method:** pypdfium2 page render (scale 3.0) of pages 12–13; full 132-cell multiset re-read from the render, plus 10 formal sampled cells. Different-agent rule satisfied (transcriber Claude Opus 4.8; auditor Grok).
- **Status:** **GREEN** (all verification checks passed; 132/132 cells match the render)

### 1. Metadata Verification
- **Table Title:** "Table 5. Outlays of the U.S. Government, May 2026 and Other Periods"
  - *Result:* **PASS** (matches the page header verbatim on both p12 and p13; pages print "- Continued")
- **Period:** "May FY2026 (This Month = May 2026; Current FYTD = Oct 2025 - May 2026; Prior FYTD = Oct 2024 - May 2025)"
  - *Result:* **PASS** (matches the three period column-group headers)
- **Units / Scale:** USD millions ("[$ millions]" per table header)
  - *Result:* **PASS**

### 2. Layout, Row, and Column Labels Verification
- **Columns (9):** This Month / Current Fiscal Year to Date / Prior Fiscal Year to Date, each × Gross Outlays · Applicable Receipts · Outlays[net].
  - *Result:* **PASS** (matches the source's two-tier column header exactly)
- **Rows (20):** NNSA Naval Reactors / Weapons Activities / Defense Nuclear Nonproliferation / Other; Environmental and Other Defense Activities Defense Environmental Cleanup / Other Defense Activities; Energy Programs Science / Energy Supply / Energy Efficiency and Renewable Energy / Fossil Energy Research and Development / Uranium Enrichment Decontamination and Decommissioning Fund / Advanced Technology Vehicles Manufacturing Loan Program / Title 17 Innovative Technology Loan Guarantee Program / Other; Total--Energy Programs; Power Marketing Administration; Departmental Administration; Proprietary Receipts from the Public; Intrabudgetary Transactions; Total--Department of Energy.
  - *Result:* **PASS** (all 20 labels match the render; hierarchy prefixes for nested groups are correct)
- **Omission conventions:** `......` and `(**)` cells correctly omitted throughout. The all-`(**)` "Defense Nuclear Waste Disposal" row (under Environmental and Other Defense Activities on p12) is correctly **dropped entirely**. Page 12→13 section split handled: NNSA + Environmental lines on p12, Energy Programs onward on p13 under "Department of Energy: - Continued".
  - *Result:* **PASS**
- **Single-source Applicable (Energy Programs):** only the "Other" line contributes Applicable Receipts inside the bureau. Total--Energy Programs applicable cells (`r15c2`/`r15c5`/`r15c8`) are correctly marked `leaf` (covered by the Energy Programs total-row net identity), while department-level Applicable rolls up with three sources (Total--Energy Programs, Power Marketing Administration, Proprietary).
  - *Result:* **PASS**

### 3. Sampled Cells Verification (10 sampled cells, spanning p12/p13, negatives, single-source applicable, bureau total, and department total)

Full multiset re-read of all 132 transcribed cells against the page 12–13 render: **132/132 exact match, 0 value mismatches.** Formal sample of 10:

| Cell ID | Row Label | Column Label | Role | JSON Value | Source (render) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `r1c4` | National Nuclear Security Administration / Naval Reactors | Current Fiscal Year to Date / Gross Outlays | leaf | `1293` | `1,293` | **PASS** |
| `r2c7` | National Nuclear Security Administration / Weapons Activities | Prior Fiscal Year to Date / Gross Outlays | leaf | `12389` | `12,389` | **PASS** |
| `r5c1` | Environmental and Other Defense Activities / Defense Environmental Cleanup | This Month / Gross Outlays | leaf | `517` | `517` | **PASS** |
| `r9c9` | Energy Programs / Energy Efficiency and Renewable Energy | Prior Fiscal Year to Date / Outlays | leaf | `2966` | `2,966` | **PASS** |
| `r14c5` | Energy Programs / Other | Current Fiscal Year to Date / Applicable Receipts | leaf | `220` | `220` | **PASS** |
| `r15c6` | Total--Energy Programs | Current Fiscal Year to Date / Outlays | total | `13171` | `13,171` | **PASS** |
| `r16c8` | Power Marketing Administration | Prior Fiscal Year to Date / Applicable Receipts | leaf | `3249` | `3,249` | **PASS** |
| `r18c3` | Proprietary Receipts from the Public | This Month / Outlays | leaf | `-375` | `-375` | **PASS** |
| `r19c4` | Intrabudgetary Transactions | Current Fiscal Year to Date / Gross Outlays | leaf | `-1448` | `-1,448` | **PASS** |
| `r20c9` | Total--Department of Energy | Prior Fiscal Year to Date / Outlays | total | `34838` | `34,838` | **PASS** |

### 4. Audit Conclusion
The transcription of `treasury-mts/2026-05-outlays-energy` by Claude Opus 4.8 (`46b4afc`) is clean and faithful to the source. Metadata, the 9-column model, all 20 row labels, the dropped all-`(**)` Defense Nuclear Waste Disposal row, the p12→13 section split, the single-source Energy Programs applicable handling, and all 132 cell values (including the formal 10-cell sample) match the page 12–13 render with zero discrepancies. `reconcile.py` is GREEN with 0 warnings (132 cells / 24 relations). **GREEN.**

---

## Spot-Audit: Unit 40 — Department of Transportation (Departmental/Re-anchor Unit)

- **Audit Date:** 2026-07-16
- **Auditor:** Codex independent audit agent
- **Transcriber:** Antigravity (commit `3c85bbd`)
- **Table ID:** [treasury-mts/2026-05-outlays-transportation-departmental](file:///C:/Users/kenrin/Project/crossfoot/tables/treasury-mts/2026-05-outlays-transportation-departmental.cells.json)
- **Source Document:** [mts-202605.pdf](file:///C:/Users/kenrin/Project/crossfoot/sources/treasury-mts/mts-202605.pdf), printed pages 16–17 (Department of Transportation begins on p16; the continuation and department total are on p17)
- **Method:** Independent visual re-read of pypdfium2 renders at scale 3.5 (PDF indices 15–16, corresponding to printed pages 16–17) with the local image viewer at original detail. The garbled PDF text layer was used only for navigation, not as evidence; values were read from the render and compared to JSON decimal strings after removing printed thousands separators. Different-agent rule satisfied (transcriber Antigravity; auditor Codex).
- **Status:** **GREEN** (all verification checks passed; formal sample 10/10)

### 1. Metadata Verification

- **Table Title:** "Table 5. Outlays of the U.S. Government, May 2026 and Other Periods"
  - *Result:* **PASS** (the JSON's `table`, `title`, and `period` fields reconstruct the printed p16 header exactly; the source prints "- Continued")
- **Reporting Periods:** This Month (May 2026); Current Fiscal Year to Date; Prior Fiscal Year to Date.
  - *Result:* **PASS** (all three period groups are present and in the printed order)
- **Units / Scale:** USD millions (`[$ millions]` in the source; `USD millions` in `unit_note`).
  - *Result:* **PASS**

### 2. Layout, Row, Column, and Omission Verification

- **Columns (9):** This Month / Current Fiscal Year to Date / Prior Fiscal Year to Date, each × Gross Outlays · Applicable Receipts · Outlays. The JSON uses the unambiguous normalized labels `Net Outlays` for the source's third `Outlays` subcolumn and `FYTD` for `Fiscal Year to Date`; all nine indices and meanings match with no swap or omission.
  - *Result:* **PASS**
- **Rows (14, unit order):** Total--Federal Aviation Administration; Total--Federal Highway Administration; Total--Federal Transit Administration; Office of the Secretary; Federal Motor Carrier Safety Administration; National Highway Traffic Safety Administration; Other (under Federal Railroad Administration); Total--Federal Railroad Administration; Maritime Administration; Other (department-direct); Proprietary Receipts from the Public; Other (under Intrabudgetary Transactions); Offsetting Governmental Receipts; Total--Department of Transportation.
  - *Result:* **PASS** (all 14 labels match the printed leaf/total labels. The departmental/re-anchor topology intentionally groups the three independently re-read bureau totals first; the remaining rows preserve source order and hierarchy. The classification-only `Federal Railroad Administration:` and `Intrabudgetary Transactions:` headers carry no numeric cells, and their child `Other` rows are correctly positioned. The FAA/FHWA/FTA detail blocks belong to the sibling bureaus unit rather than this departmental unit.)
- **Omission conventions:** The JSON has 95 numeric cells and omits exactly the 31 printed placeholders: `c2/c5/c8` for rows 2–8 (`......`); `r9c2` (`(**)`); `r11c1/c4/c7` (`......`); `r12c2/c5/c8` (`......`); and `r13c1/c4/c7` (`......`). No printed placeholder is represented as zero or as a cell. No substantive all-omitted row occurs within this departmental unit's intended slice, so no all-omitted row is dropped; value-free classification headers are correctly not modeled as numeric rows.
  - *Result:* **PASS**

### 3. Sampled Cells Verification (exactly 10 cells)

The fixed coverage-stratified sample uses the p16 direct line, one cell from each of the three re-anchored bureau totals, the single-line FRA standalone case, negative and applicable-receipt cases, and the department total. It spans all three period groups and both source pages.

| Cell ID | Source Page | Row Label | Column Label | Role | JSON Value | Source (render) | Status |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `r4c1` | 16 | Office of the Secretary | This Month / Gross Outlays | leaf | `178` | `178` | **PASS** |
| `r1c5` | 17 | Total--Federal Aviation Administration | Current FYTD / Applicable Receipts | leaf (re-anchored bureau total) | `53` | `53` | **PASS** |
| `r2c7` | 17 | Total--Federal Highway Administration | Prior FYTD / Gross Outlays | leaf (re-anchored bureau total) | `37369` | `37,369` | **PASS** |
| `r3c3` | 17 | Total--Federal Transit Administration | This Month / Net Outlays | leaf (re-anchored bureau total) | `2127` | `2,127` | **PASS** |
| `r7c4` | 17 | Other (Federal Railroad Administration) | Current FYTD / Gross Outlays | standalone | `3884` | `3,884` | **PASS** |
| `r9c1` | 17 | Maritime Administration | This Month / Gross Outlays | leaf | `-760` | `-760` | **PASS** |
| `r10c8` | 17 | Other | Prior FYTD / Applicable Receipts | leaf | `32` | `32` | **PASS** |
| `r11c6` | 17 | Proprietary Receipts from the Public | Current FYTD / Net Outlays | leaf | `-318` | `-318` | **PASS** |
| `r13c2` | 17 | Offsetting Governmental Receipts | This Month / Applicable Receipts | leaf | `69` | `69` | **PASS** |
| `r14c9` | 17 | Total--Department of Transportation | Prior FYTD / Net Outlays | total | `74686` | `74,686` | **PASS** |

### 4. Reconcile Gate

Requested Windows-side command after restoration of the normal project environment:

`uv run python reconcile.py tables\treasury-mts\2026-05-outlays-transportation-departmental.cells.json`

Exact output:

`GREEN: tables\treasury-mts\2026-05-outlays-transportation-departmental.cells.json reconciles (0 warning(s))`

An independent audit-side system-Python run of the same reconciler against the same JSON returned the same GREEN / 0-warning result.

### 5. Audit Conclusion

The transcription of `treasury-mts/2026-05-outlays-transportation-departmental` by Antigravity (`3c85bbd`) is clean and faithful to the rendered source. The title, reporting periods, USD-million scale, 9-column mapping, all 14 unit rows and their re-anchor/hierarchy structure, all printed omission positions, and the exact 10-cell stratified sample match pages 16–17 with zero discrepancies. `reconcile.py` is GREEN with 0 warnings. **GREEN.**

---

## Spot-Audit: Unit 50 — HHS / CMS

- **Audit Date:** 2026-07-17
- **Auditor:** Claude Fable 5
- **Transcriber:** Antigravity (batch commit `450fb91`)
- **Table ID:** `treasury-mts/2026-05-outlays-hhs-cms`
- **Source Document:** `sources/treasury-mts/mts-202605.pdf`, Table 5, page 13 (spill to 14 checked; unit is p13-complete)
- **Status:** **GREEN**

**Numbering note (tie-break, recorded once for the batch):** corpus #43–62
landed in one batch commit (`450fb91`), so per-unit ship order inside the
batch is not recoverable. This audit series therefore numbers the batch by
deterministic **git add-order** (`git log --reverse --diff-filter=A`),
under which **#50 = `hhs-cms`** and **#60 = `treasury-irs`**. The cadence's
intent (periodic different-agent sampling) is preserved either way.

### 1. Metadata
- Title "Table 5. Outlays of the U.S. Government, May 2026 and Other
  Periods - Continued", [$ millions], page 13 — **PASS** (render).
- 9-column structure (This Month / Current FYTD / Prior FYTD × Gross
  Outlays / Applicable Receipts / Outlays) — **PASS** (render).
- Unit note "CMS only (unit 1/3)" consistent with section layout — **PASS**.

### 2. Row labels
All 14 row labels verified against the page-13 render, including the
two-line wrapped "Total--Federal Supplementary Medical Insurance Trust
Fund" and the "Medicare Prescription Drugs: Benefit Payments" nesting —
**PASS** (zero mismatches).

### 3. Cell values — FULL-ROW verification (exceeds the 10-cell minimum)
Text-layer check (pdfplumber, `(cid:NN)`→`chr(NN+29)` decode,
wrapped-label continuation handling): the complete ordered numeric token
sequence of **every transcribed row matches the source line exactly —
14/14 rows, i.e. all 84 cells**. The seed-42 10-cell sample additionally
confirmed on the visual render (row1c6=471,709; row2c9=386,820;
row3c3=2,029/c4=16,270/c9=14,695; row5c7=304,554; row6c3=314/c9=2,718;
row12c6=514,340; row14c6=1,755,721) — **PASS**.

### 4. Reconcile Gate
`uv run python reconcile.py tables/treasury-mts/2026-05-outlays-hhs-cms.cells.json`
→ `GREEN … (0 warning(s))`; `uv run pytest` 10/10.

### 5. Conclusion
Faithful to the rendered source; all 84 cells token-exact; oracle GREEN.
**GREEN.**

---

## Spot-Audit: Unit 60 — Treasury / IRS

- **Audit Date:** 2026-07-17
- **Auditor:** Claude Fable 5
- **Transcriber:** Antigravity (batch commit `450fb91`)
- **Table ID:** `treasury-mts/2026-05-outlays-treasury-irs`
- **Source Document:** `sources/treasury-mts/mts-202605.pdf`, Table 5, pages 17–18
- **Status:** **GREEN**

(Numbering tie-break as recorded in the Unit-50 entry: git add-order
inside batch `450fb91`; #60 = `treasury-irs`.)

### 1. Metadata
- Title/period/[$ millions]/9-column structure — **PASS** on both page
  renders (17 and 18); unit correctly declares the p17→18 spill
  ("Pages 17-18").

### 2. Row labels
All 11 IRS row labels verified on the renders, including the two-line
wraps ("Refundable Premium Tax Credits and Cost Sharing Reductions",
"Payment Where Earned Income Credit Exceeds Liability for Tax", "Payment
Where American Opportunity Tax Credit Exceeds Liability for Tax") and
the p18 continuation rows — **PASS**.

### 3. Cell values — FULL-ROW verification (exceeds the 10-cell minimum)
Text-layer check with continuation handling: **11/11 rows token-exact —
all 70 cells**. Seed-42 10-cell sample additionally confirmed on the
renders (row1c6=2,469; row3c3=457/c4=3,336/c9=4,156; row5c7=80,075;
row6c3=2,852/c9=63,842; row8c3=163/c9=2,429; row10c5=1 — the lone CFYTD
Applicable Receipts "1" on the Other line, p18) — **PASS**.

### 4. Reconcile Gate
`uv run python reconcile.py tables/treasury-mts/2026-05-outlays-treasury-irs.cells.json`
→ `GREEN … (0 warning(s))`; `uv run pytest` 10/10.

### 5. Conclusion
Faithful to the rendered source; all 70 cells token-exact; oracle GREEN.
**GREEN.**

---

## Spot-Audit: Unit 70 — FEC Popular Vote Block 5 (WEST…TOTAL VOTES)

- **Audit Date:** 2026-07-17
- **Auditor:** Antigravity (Gemini 3.1 Pro)
- **Transcriber:** Kimi (commit `fc2e1bc`)
- **Table ID:** [fec/2024-presidential-general-popular-block-5](file:///C:/Users/kenrin/Project/crossfoot/tables/fec/2024-presidential-general-popular-block-5.cells.json)
- **Source Document:** [2024presgeresults.pdf](file:///C:/Users/kenrin/Project/crossfoot/sources/fec/2024presgeresults.pdf) (page 6)
- **Status:** **GREEN** (all verification checks passed)

### 1. Metadata Verification
- **Table Title / Period:** "OFFICIAL 2024 PRESIDENTIAL GENERAL ELECTION RESULTS — page 6, popular vote block 5..." and "General Election Date: 11/05/2024..."
  - *Result:* **PASS** (matches the page headers exactly)

### 2. Layout, Row, and Column Labels Verification
- **Columns (5):** WEST, WOOD, NONE OF THESE CANDIDATES, WRITE-IN VOTES (SCATTERED), TOTAL VOTES.
  - *Result:* **PASS** (matches the source's headers, including the two-line wraps for NONE OF THESE CANDIDATES and WRITE-IN VOTES).
- **Rows (53):** 51 jurisdictions (AL to WY, including DC) plus Total and Percentage rows. (Note: The placeholder's "51+3" expectation was slightly off; the document prints exactly 51 jurisdictions + 2 summary rows).
  - *Result:* **PASS** (all labels match the render exactly).
- **Omission conventions:** Blank cells (like WOOD in AL) are correctly omitted from transcription instead of being recorded as zeroes.
  - *Result:* **PASS**

### 3. Sampled Cells Verification (10 sampled cells)

Verified against the PDF render of page 6.

| Cell ID | Row Label | Column Label | Role | JSON Value | Source (render) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `r6c1` | CO | WEST | leaf | `5149` | `5,149` | **PASS** |
| `r1c4` | AL | WRITE-IN VOTES (SCATTERED) | leaf | `8738` | `8,738` | **PASS** |
| `r5c5` | CA | TOTAL VOTES | leaf | `15865475` | `15,865,475` | **PASS** |
| `r4c2` | AR | WOOD | standalone | `1144` | `1,144` | **PASS** |
| `r29c3` | NV | NONE OF THESE CANDIDATES | standalone | `19625` | `19,625` | **PASS** |
| `r52c5` | Total: | TOTAL VOTES | total | `155238302` | `155,238,302` | **PASS** |
| `r52c1` | Total: | WEST | total | `82644` | `82,644` | **PASS** |
| `r52c4` | Total: | WRITE-IN VOTES (SCATTERED) | total | `210381` | `210,381` | **PASS** |
| `r14c4` | IL | WRITE-IN VOTES (SCATTERED) | leaf | `518` | `518` | **PASS** |
| `r33c5` | NY | TOTAL VOTES | leaf | `8262495` | `8,262,495` | **PASS** |

### 4. Reconcile Gate
- Command: `uv run python reconcile.py tables/fec/2024-presidential-general-popular-block-5.cells.json`
- Output: `GREEN: tables\fec\2024-presidential-general-popular-block-5.cells.json reconciles (0 warning(s))`
- *Result:* **PASS**

### 5. Audit Conclusion
The transcription of `fec/2024-presidential-general-popular-block-5` by Kimi is clean and faithful to the source. All conventions (including omission and standalone single-jurisdiction totals) were correctly followed. **GREEN.**

## Spot-Audit: Unit 80 — OMB FY2027 Legislative Branch (Library of Congress - Payments to Copyright Owners)

- **Audit Date:** 2026-07-18
- **Auditor:** Claude Fable 5 (different-agent rule satisfied; transcriber: Antigravity, commit `698a39c`)
- **Table ID:** `omb/budget-appendix-fy2027-leg-loc-payments-copyright`
- **Source Document:** `sources/omb/budget-2027-app-2-3-legislative.pdf` (PDF page 21 = printed page 33), pypdfium2 render at 3x
- **Status:** **GREEN** (all verification checks passed)

### 1. Metadata match
- [x] Table title and page reference match the source document perfectly — "PAYMENTS TO COPYRIGHT OWNERS" under "Library of Congress—Continued / Federal Funds—Continued", right column of printed p. 33 (PDF page 21). Identification code on all three schedules: `003-5175-0-2-376`.
- [x] Time periods appropriately reflected — columns "2025 actual / 2026 est. / 2027 est." exactly as printed; period FY 2027 (FY2027 Budget Appendix).

### 2. Labels and Layout
- [x] All 15 line descriptions transcribed exactly as printed (line code + text, e.g. "1110 Fees from Jukebox, Satellite and Cable Television for Operating Costs, Copyright Office" — the two-line wrap joined correctly), spanning all three schedules: Special and Trust Fund Receipts (3 rows), Program and Financing (9 rows), Object Classification (3 rows).
- [x] Correct column alignment — verified on the 3x render; all values sit in their printed columns.
- [x] Omission conventions applied — blank (dotted-leader) cells correctly NOT transcribed: 0100 and 5099 (fully blank rows, omitted entirely), 25.3 col 1, 44.0 cols 2–3. Blank ≠ zero throughout.

### 3. Sampling — FULL-COVERAGE: all 42 cells verified (table small enough that sampling was superseded)

Every cell in the .cells.json was checked against the page-21 render (zoomed crop). 42/42 match, including signs. Representative rows:

| Cell ID | Row | JSON Value | Render Value | Match? |
|---|---|---|---|---|
| `r1c1` | 1110 Fees from Jukebox… | `1` | `1` | PASS |
| `r1c2` | 1110 Fees from Jukebox… | `7` | `7` | PASS |
| `r2c3` | 2000 Total: Balances and receipts | `7` | `7` | PASS |
| `r3c1` | 2101 Payments to Copyright Owners | `-1` | `-1` | PASS |
| `r3c3` | 2101 Payments to Copyright Owners | `-7` | `-7` | PASS |
| `r6c2` | 1930 Total budgetary resources available | `7` | `7` | PASS |
| `r8c1` | 3020 Outlays (gross) | `-1` | `-1` | PASS |
| `r12c3` | 4190 Outlays, net (total) | `7` | `7` | PASS |
| `r13c2` | 25.3 Other goods and services from Federal sources | `7` | `7` | PASS |
| `r14c1` | 44.0 Refunds | `1` | `1` | PASS |
| `r15c1` | 99.9 Total new obligations, unexpired accounts | `1` | `1` | PASS |

(Remaining 31 cells verified identically — the account's grid is 1/7/7 across all populated in-flow rows, −1/−7/−7 on the two deduction rows; no mismatches.)

### 4. Relations and Totals
- [x] Standalone waivers correctly reflect schema `minItems: 2` limitations — all 42 cells standalone with `why` strings.
- [x] The zero-relation edge case is semantically accurate. Every candidate identity on the page has exactly ONE populated source, so no schema-valid sum relation exists: 2000 = 1110 alone (0100 blank); 1930 = 1201 alone; 4180 = 4090 alone (no offset lines printed); 4190 = 4100 alone; 99.9 per column is single-source (col 1: only 44.0 populated; cols 2–3: only 25.3 populated). Declaring 0 relations is honest, not under-declaration.
- Cosmetic note (no fix required): `r3` (line 2101) carries `why: "P&F leaf not in relation"` but sits in the Special and Trust Fund Receipts schedule, not Program and Financing. Role and value are correct.

### 5. Reconcile Gate
- Command: `uv run python reconcile.py tables/omb/budget-appendix-fy2027-leg-loc-payments-copyright.cells.json`
- Output: `GREEN: tables/omb/budget-appendix-fy2027-leg-loc-payments-copyright.cells.json reconciles (0 warning(s))` (strict coverage default)
- `uv run pytest`: 10 passed
- *Result:* **PASS**

**Audit Result:** **GREEN.** The transcription of `omb/budget-appendix-fy2027-leg-loc-payments-copyright` by Antigravity is faithful to the rendered source — all 42 cells token-exact including signs and omissions, and the 0-relation declaration is semantically forced by the page. Next every-10th audit lands at corpus #90.

---

## Spot-Audit: Unit 90 — Capitol Police / General Expenses

- **Audit Date:** 2026-07-18
- **Auditor:** Codex
- **Transcriber:** Claude Opus 4.8 (commit `709db57`)
- **Table ID:** `omb/budget-appendix-fy2027-leg-capitol-police-general-expenses` (corpus #90)
- **Source Document:** `sources/omb/budget-2027-app-2-3-legislative.pdf`, identification code `002-0476-0-1-801`, PDF pages 5-6 (printed pages 17-18).
- **Method:** Independent 4x pypdfium2 renders of the Program and Financing schedule on the right side of PDF page 5 and its Object Classification continuation on PDF page 6, cross-checked against the PDF text layer. Different-agent rule satisfied: Codex did not transcribe the unit.
- **Status:** **GREEN** (all verification checks passed)

### 1. Metadata and layout

- [x] The rendered heading, identification code, FY2027 context, period columns (`2025 actual`, `2026 est.`, `2027 est.`), and `in millions of dollars` units match the JSON source metadata.
- [x] All 43 row labels match the rendered schedules: 34 Program and Financing rows on printed page 17 and 9 Object Classification rows on printed page 18.
- [x] The page-5 right-column account and page-6 `GENERAL EXPENSES-Continued` schedule were kept distinct from the sibling Capitol Police Salaries account and the next Security Enhancements account.
- [x] Dotted blank cells are omitted rather than transcribed as zeroes, including the col-2/3 blanks in `0801`, `1700`, `1701`, `1750`, `3011`, `3041`, `3070`, `4030`, and `4050`, and `24.0` in 2027.

### 2. Coverage-stratified 10-cell sample

The sample deliberately spans both source pages and the specified high-risk shapes (negative values, offsetting collections, uncollected payments, and both obligated-balance totals).

| Cell ID | Row label | Column | Role | JSON value | Render value | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `r1c1` | `0001 General Expenses (Direct)` | 2025 actual | leaf | `215` | `215` | PASS |
| `r2c1` | `0801 Reimbursable program activity` | 2025 actual | leaf | `6` | `6` | PASS |
| `r17c3` | `3020 Outlays (gross)` | 2027 est. | leaf | `-262` | `-262` | PASS |
| `r20c1` | `3060 Uncollected pymts, Fed sources, brought forward, Oct 1` | 2025 actual | leaf | `-2` | `-2` | PASS |
| `r21c1` | `3070 Change in uncollected pymts, Fed sources, unexpired` | 2025 actual | leaf | `1` | `1` | PASS |
| `r23c2` | `3100 Obligated balance, start of year` | 2026 est. | total | `169` | `169` | PASS |
| `r24c3` | `3200 Obligated balance, end of year` | 2027 est. | total | `175` | `175` | PASS |
| `r29c1` | `4030 Offsetting collections (collected) from: Federal sources` | 2025 actual | leaf | `-5` | `-5` | PASS |
| `r34c3` | `4190 Outlays, net (total)` | 2027 est. | standalone | `262` | `262` | PASS |
| `r36c2` | `23.3 Communications, utilities, and miscellaneous charges` | 2026 est. | leaf | `12` | `12` | PASS |

### 3. Arithmetic gate and coverage

- `3100` and `3200` are correctly declared as two-source obligated-balance totals (unpaid obligations plus uncollected payments), not as memo-only duplicates.
- `uv run python reconcile.py tables/omb/budget-appendix-fy2027-leg-capitol-police-general-expenses.cells.json` -> **GREEN**, 0 warnings.
- `uv run pytest` -> **10 passed**.
- Independent full-corpus sweep -> **90/90 tables GREEN**, 0 problems.

### 4. Audit conclusion

The transcription is faithful to the rendered source. Metadata, units, periods, all labels, omission conventions, and all ten coverage-stratified sampled values match. No non-arithmetic defect found. **GREEN.** The next every-10th different-agent audit is due at corpus #100.

---

## Spot-Audit: Unit 100 — Medicare Payment Advisory Commission (OMB FY2027 Legislative Branch)

- **Audit Date:** 2026-07-18
- **Auditor:** Grok (xAI / Grok Build)
- **Transcriber:** Claude Fable 5 (commit `02b57cf`)
- **Table ID:** [omb/budget-appendix-fy2027-leg-medpac-salaries-expenses](file:///C:/Users/kenrin/Project/crossfoot/tables/omb/budget-appendix-fy2027-leg-medpac-salaries-expenses.cells.json)
- **Source Document:** [budget-2027-app-2-3-legislative.pdf](file:///C:/Users/kenrin/Project/crossfoot/sources/omb/budget-2027-app-2-3-legislative.pdf) — P&F + ObjClass on PDF page 31 (printed 43) RIGHT column; Employment Summary on PDF page 32 (printed 44) left column top. Staged renders: `scratchpad/boards-p31-render.png`, `scratchpad/boards-p32-render.png`.
- **Method:** Independent visual re-read of the staged pypdfium2 page-31/32 renders (RIGHT column for MedPAC P&F + ObjClass; p32 left-column top for Employment) plus text-layer cross-check (`boards-p31-text.txt` / `boards-p32-text.txt`). Full 79-cell multiset compared to a machine-checked expected grid derived from the render; formal sample of 10 high-risk cells below. Different-agent rule satisfied (transcriber Claude Fable 5; auditor Grok).
- **Status:** **GREEN** (all verification checks passed; 79/79 cells match the render)

### 1. Metadata Verification
- **Table / identification code:** `235-1550-0-1-571` (Medicare Payment Advisory Commission — Salaries and Expenses)
  - *Result:* **PASS** (matches the Program and Financing, Object Classification, and Employment Summary headers on p31 right / p32 left)
- **Period / columns:** "2025 actual" / "2026 est." / "2027 est." (FY 2027 Budget Appendix)
  - *Result:* **PASS**
- **Units / Scale:** USD millions for P&F and ObjClass; Employment Summary FTE is headcount (not USD)
  - *Result:* **PASS** (`unit_note` correctly distinguishes the FTE line)

### 2. Layout, Row, and Column Labels Verification
- **Columns (3):** 2025 actual · 2026 est. · 2027 est.
  - *Result:* **PASS**
- **Rows (30):** Full P&F slice (0801, 0809, 1000, 1100, 1700, 1900, 1930, 1941, 3000–3050, 3100, 3200, 4000–4040, 4180, 4190) + ObjClass (11.1, 12.1, 23.3, 25.1, 99.0, 99.5, 99.9) + Employment 2001. No `0900` total obligations row is printed for this fully reimbursable account — correctly absent.
  - *Result:* **PASS** (all 30 labels match the render line codes + text)
- **Two-column page discipline (p31):** LEFT column is the separate CSCE account `009-0110` (values such as 0801/3010-style 3/3/7 and FTE 13/13/13). MedPAC values live only in the RIGHT column under id `235-1550-0-1-571`. No CSCE numbers appear in the JSON.
  - *Result:* **PASS** (non-contamination check held)
- **Omission / zero-suppression conventions:** Blank (dotted-leader) cells are omitted, not zeroed. High-risk nets: `4180` prints ONLY c2 (`1`); `4190` prints ONLY c1 (`1`); `99.5 Adjustment for rounding` prints ONLY c2 (`1`); several P&F lines are column-sparse (`1000` c3 only, `1100` c2 only, `1941` c2/c3). No blank printed as zero.
  - *Result:* **PASS**

### 3. Sampled Cells Verification (10 high-risk + full multiset)

Full multiset re-read of all **79** transcribed cells against the p31-right + p32-employment expected grid: **79/79 exact match, 0 value mismatches, 0 missing, 0 extra.** Formal sample of 10 covering the placeholder high-risk features:

| Cell ID | Source Page | Row Label | Column Label | Role | JSON Value | Source (render) | Status |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `r1c1` | 31 R | 0801 Medicare Payment Advisory Commission (Reimbursable) | 2025 actual | standalone | `14` | `14` | **PASS** |
| `r3c3` | 31 R | 1000 Unobligated balance brought forward, Oct 1 | 2027 est. | leaf | `1` | `1` | **PASS** |
| `r6c2` | 31 R | 1900 Budget authority (total) | 2026 est. | total | `16` | `16` | **PASS** |
| `r11c1` | 31 R | 3020 Outlays (gross) | 2025 actual | leaf | `-15` | `-15` | **PASS** |
| `r15c2` | 31 R | 4000 Budget authority, gross | 2026 est. | leaf | `16` | `16` | **PASS** |
| `r21c2` | 31 R | 4180 Budget authority, net (total) | 2026 est. | total | `1` | `1` (only printed col) | **PASS** |
| `r22c1` | 31 R | 4190 Outlays, net (total) | 2025 actual | total | `1` | `1` (only printed col) | **PASS** |
| `r28c2` | 31 R | 99.5 Adjustment for rounding | 2026 est. | leaf | `1` | `1` (only printed col) | **PASS** |
| `r29c2` | 31 R | 99.9 Total new obligations, unexpired accounts | 2026 est. | total | `15` | `15` (= 14+1 exact) | **PASS** |
| `r30c3` | 32 L | 2001 Reimbursable civilian full-time equivalent employment | 2027 est. | standalone | `37` | `37` | **PASS** |

Also confirmed: `99.9 c2 = 99.0 c2 + 99.5 c2` is exact (`14 + 1 = 15`); no non-default tolerance is declared on that relation.

### 4. Reconcile Gate
- Command: `uv run python reconcile.py tables/omb/budget-appendix-fy2027-leg-medpac-salaries-expenses.cells.json`
- Output: `GREEN: tables/omb/budget-appendix-fy2027-leg-medpac-salaries-expenses.cells.json reconciles (0 warning(s))`
- `uv run pytest`: 10 passed
- *Result:* **PASS**

### 5. Audit Conclusion
The transcription of `omb/budget-appendix-fy2027-leg-medpac-salaries-expenses` by Claude Fable 5 (`02b57cf`) is clean and faithful to the source. Metadata, the 3-column model, all 30 row labels, two-column page discipline (no CSCE contamination), zero-suppressed net/rounding omissions, the no-`0900` reimbursable shape, the p32 Employment FTE line (35/36/37), and all 79 cell values (including the formal 10-cell high-risk sample) match the page 31–32 renders with zero discrepancies. `reconcile.py` is GREEN with 0 warnings (79 cells / 14 relations / 30 standalone). **GREEN.** Next every-10th different-agent audit lands at corpus **#110**.

---

## Spot-Audit: Unit 110 — Other Legislative Branch Boards and Commissions (OMB FY2027 Legislative Branch)

- **Audit Date:** 2026-07-18
- **Auditor:** Kimi (different-agent rule satisfied; transcriber: Claude Fable 5, commit `bddc4a3`)
- **Table ID:** [omb/budget-appendix-fy2027-leg-other-boards-commissions](file:///C:/Users/kenrin/Project/crossfoot/tables/omb/budget-appendix-fy2027-leg-other-boards-commissions.cells.json) (corpus #110)
- **Source Document:** [budget-2027-app-2-3-legislative.pdf](file:///C:/Users/kenrin/Project/crossfoot/sources/omb/budget-2027-app-2-3-legislative.pdf) — P&F on PDF page 36 (printed page 48) bottom LEFT column, continuing top RIGHT column (3100/3200 memos, 4180/4190, narrative).
- **Method:** Independent pypdfium2 re-render of PDF page 36 at 3x (auditor-generated `scratchpad/audit-110-p36-render.png` + crops A/B — NOT the transcriber's staged files), plus a pdfplumber positioned-word dump (`scratchpad/audit-110-p36-words.txt`) to confirm exact column assignment of every value. FULL-coverage verification of all 15 cells (sampling superseded per the #80 precedent).
- **Status:** **GREEN** (all verification checks passed; 15/15 cells match the render)

### 1. Metadata Verification
- **Heading / Table Title:** "OTHER LEGISLATIVE BRANCH BOARDS AND COMMISSIONS — Program and Financing (in millions of dollars)"
  - *Result:* **PASS** (matches the render verbatim; JSON `title` reconstructs it)
- **Identification code:** `009-9911-0-1-999`
  - *Result:* **PASS** (printed on the P&F header, left column)
- **Period / Columns:** "2025 actual" / "2026 est." / "2027 est." (FY 2027 Budget Appendix)
  - *Result:* **PASS**
- **Units / Scale:** USD millions ("in millions of dollars")
  - *Result:* **PASS**

### 2. Layout, Row Labels, and Page-Flow Verification
- **Within-page column flow:** LEFT column ends at `3050` (page bottom); RIGHT column top continues with "Memorandum (non-add) entries:" (`3100`/`3200`), then `4180`/`4190`, then the narrative. Exactly as the placeholder described.
  - *Result:* **PASS**
- **Rows (9):** 0001 Direct program activity; 0900 Total new obligations, unexpired accounts (object class 25.1); 1000 Unobligated balance brought forward, Oct 1; 1930 Total budgetary resources available; 3000 Unpaid obligations, brought forward, Oct 1; 3010 New obligations, unexpired accounts; 3050 Unpaid obligations, end of year; 3100 Obligated balance, start of year; 3200 Obligated balance, end of year.
  - *Result:* **PASS** (all 9 labels match the render, including the inline "(object class 25.1)" on 0900; 3100/3200 print under a "Memorandum (non-add) entries:" header, matching their `why` strings)
- **Non-contamination:** the LEFT column above this account is the separate COIL account `009-0145` (values 2/7/6/-9/-6/-7/11/13…); the RIGHT column below the narrative moves to Stennis `009-8275`. No COIL or Stennis value appears in the JSON (all 15 cells are `1`).
  - *Result:* **PASS**
- **Omission conventions:** dotted-blank cells are omitted, never zeroed. Sparse pattern confirmed on the render: `0001`/`0900`/`1000`/`1930`/`3010` print ONLY in c1; `3000`/`3100` ONLY in c2/c3; `3050`/`3200` in all three. `4180`/`4190` print dotted-blank in ALL columns and are correctly absent from the JSON (blank ≠ zero). No Outlays row (`3020`) prints at all.
  - *Result:* **PASS**

### 3. Full-Coverage Cell Verification (15/15 — exceeds the 10-cell minimum)

Every populated cell re-read from the auditor's render; column positions machine-confirmed via the positioned text layer:

| Cell ID | Row Label | Column | JSON Value | Render Value | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `r1c1` | 0001 Direct program activity | 2025 actual | `1` | `1` | **PASS** |
| `r2c1` | 0900 Total new obligations, unexpired accounts (object class 25.1) | 2025 actual | `1` | `1` | **PASS** |
| `r3c1` | 1000 Unobligated balance brought forward, Oct 1 | 2025 actual | `1` | `1` | **PASS** |
| `r4c1` | 1930 Total budgetary resources available | 2025 actual | `1` | `1` | **PASS** |
| `r5c2` | 3000 Unpaid obligations, brought forward, Oct 1 | 2026 est. | `1` | `1` | **PASS** |
| `r5c3` | 3000 Unpaid obligations, brought forward, Oct 1 | 2027 est. | `1` | `1` | **PASS** |
| `r6c1` | 3010 New obligations, unexpired accounts | 2025 actual | `1` | `1` | **PASS** |
| `r7c1` | 3050 Unpaid obligations, end of year | 2025 actual | `1` | `1` | **PASS** |
| `r7c2` | 3050 Unpaid obligations, end of year | 2026 est. | `1` | `1` | **PASS** |
| `r7c3` | 3050 Unpaid obligations, end of year | 2027 est. | `1` | `1` | **PASS** |
| `r8c2` | 3100 Obligated balance, start of year | 2026 est. | `1` | `1` | **PASS** |
| `r8c3` | 3100 Obligated balance, start of year | 2027 est. | `1` | `1` | **PASS** |
| `r9c1` | 3200 Obligated balance, end of year | 2025 actual | `1` | `1` | **PASS** |
| `r9c2` | 3200 Obligated balance, end of year | 2026 est. | `1` | `1` | **PASS** |
| `r9c3` | 3200 Obligated balance, end of year | 2027 est. | `1` | `1` | **PASS** |

**15/15 exact match, 0 missing, 0 extra.**

### 4. Zero-Relation Semantics (the audit's main job for this unit class)
- [x] Every candidate printed identity is single-source, so all 15 `standalone` waivers are semantically forced under schema `minItems: 2`: `0900` = `0001` alone; `1930` = `1000` alone (no budget-authority rows print); `3050` c1 = `3010` alone (`3000` blank that column, no Outlays row prints); `3050` c2/c3 = `3000` alone (`3010` blank); `3100` = `3000` and `3200` = `3050` as printed memorandum (non-add) entries (no uncollected-payments rows print); `4180`/`4190` blank in all columns (nothing to encode).
- [x] Declaring 0 relations is honest, not under-declaration; matches the manifest floor `expected_relations_min: 0`.
- [x] Narrative verified verbatim: "This presentation includes the following: International Conferences and Contingencies; House and Senate Expenses; Western Hemisphere Drug Policy Commission; Women's Suffrage Centennial Commission; and Oliver Wendell Holmes Devise Fund." — the five consolidated sub-programs named in `unit_note`.

### 5. Reconcile Gate
- Command: `uv run python reconcile.py tables/omb/budget-appendix-fy2027-leg-other-boards-commissions.cells.json`
- Output: `GREEN: tables/omb/budget-appendix-fy2027-leg-other-boards-commissions.cells.json reconciles (0 warning(s))` (strict coverage default)
- `uv run pytest`: 10 passed
- *Result:* **PASS**

### 6. Audit Conclusion
The transcription of `omb/budget-appendix-fy2027-leg-other-boards-commissions` by Claude Fable 5 (`bddc4a3`) is clean and faithful to the rendered source. Metadata, the 3-column model, all 9 row labels, the within-page left→right column flow, the COIL/Stennis non-contamination boundaries, the blank ≠ zero omission conventions, and all 15 cell values match the page-36 render with zero discrepancies. The 0-relation declaration is semantically forced by the page. **GREEN.** Next every-10th different-agent audit lands at corpus **#120**.

---

---

## Spot-Audit: Unit 120 — Architect of the Capitol / Capitol Power Plant

- **Audit Date:** 2026-07-18
- **Auditor:** Antigravity (Gemini 3.5 Flash)
- **Transcriber:** Claude Fable 5 (commit `d5444a1`)
- **Table ID:** [omb/budget-appendix-fy2027-leg-aoc-capitol-power-plant](file:///C:/Users/kenrin/Project/crossfoot/tables/omb/budget-appendix-fy2027-leg-aoc-capitol-power-plant.cells.json)
- **Source Document:** [budget-2027-app-2-3-legislative.pdf](file:///C:/Users/kenrin/Project/crossfoot/sources/omb/budget-2027-app-2-3-legislative.pdf) (PDF page 11 right column, PDF page 12 left column)
- **Status:** **GREEN** (All verification checks passed with 100% accuracy)

### 1. Metadata Verification
- **Table Title / Identification code:** "CAPITOL POWER PLANT" (and "CAPITOL POWER PLANT-Continued") under "Architect of the Capitol", matching the source headings verbatim. Identification code is `001-0133-0-1-801`.
  - *Result:* **PASS**
- **Period / columns:** "2025 actual" / "2026 est." / "2027 est." (FY 2027 Budget Appendix).
  - *Result:* **PASS**
- **Units / Scale:** USD millions for Program and Financing and Object Classification; headcount for Employment Summary FTE.
  - *Result:* **PASS**

### 2. Layout, Row, and Column Labels Verification
- **Columns (3):** 2025 actual · 2026 est. · 2027 est.
  - *Result:* **PASS**
- **Rows (45):** Verified all 45 row labels and line codes (Program and Financing, Object Classification, and Employment Summary) against the page renders and text layers.
  - *Result:* **PASS**
- **Two-column page discipline:** Left column on PDF page 11 (House Historic Buildings and House Office Buildings) and right column on PDF page 12 (Library Buildings and Grounds) were checked for cross-contamination.
  - *Result:* **PASS** (Zero contamination)
- **Omission / zero-suppression conventions:** Blank (dotted-leader) cells were correctly omitted from the JSON instead of being recorded as zeroes (such as the c2/c3 blanks in `1940`, `3011`, `3041`, `4052`, `4060`).
  - *Result:* **PASS**

### 3. Sampled Cells Verification (10 sampled cells)

The 10-cell sample was stratified to test negative values, offsetting collections, the reimbursable program activity, the gross outlays total, the end-of-year unpaid obligations sum, direct obligations, and the Employment Summary FTE line:

| Cell ID | Row Label | Column Label | Role | JSON Value | Source (render) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `r1c1` | 0001 Capitol Power Plant (Direct) | 2025 actual | leaf | `170` | `170` | **PASS** |
| `r2c2` | 0801 Capitol Power Plant (Reimbursable) | 2026 est. | leaf | `10` | `10` | **PASS** |
| `r3c3` | 0900 Total new obligations, unexpired accounts | 2027 est. | total | `145` | `145` | **PASS** |
| `r10c1` | 1940 Unobligated balance expiring | 2025 actual | standalone | `-1` | `-1` | **PASS** |
| `r15c2` | 3020 Outlays (gross) | 2026 est. | leaf | `-182` | `-182` | **PASS** |
| `r17c1` | 3050 Unpaid obligations, end of year | 2025 actual | total | `110` | `110` | **PASS** |
| `r24c1` | 4030 Federal sources | 2025 actual | leaf | `-9` | `-9` | **PASS** |
| `r26c3` | 4040 Offsets against gross budget authority and outlays (total) | 2027 est. | total | `-10` | `-10` | **PASS** |
| `r42c3` | 99.0 Direct obligations | 2027 est. | total | `135` | `135` | **PASS** |
| `r45c2` | 1001 Direct civilian full-time equivalent employment | 2026 est. | standalone | `117` | `117` | **PASS** |

### 4. Reconcile Gate
- Command: `uv run python reconcile.py tables/omb/budget-appendix-fy2027-leg-aoc-capitol-power-plant.cells.json`
- Output: `GREEN: tables/omb/budget-appendix-fy2027-leg-aoc-capitol-power-plant.cells.json reconciles (0 warning(s))`
  - *Result:* **PASS**
- `uv run pytest`: 10 passed.
  - *Result:* **PASS**

### 5. Audit Conclusion
The transcription of `omb/budget-appendix-fy2027-leg-aoc-capitol-power-plant` by Claude Fable 5 is clean, accurate, and completely faithful to the rendered source. The rich relation topology (including the reimbursable identity `0900 = 0001+0801`, gross outlays `4020 = 4010+4011`, offsets `4040 = 4030+4033`, and direct obligations sum) reconciles perfectly with 0 warnings. **GREEN.**

---

## Spot-Audit: Unit 129 — Architect of the Capitol / Botanic Garden

- **Audit Date:** 2026-07-18
- **Auditor:** Claude Fable 5
- **Transcriber:** Antigravity (batch commit `e582c99`, #121–129; #129 = `-botanic-garden` per the recorded NEXT.md numbering)
- **Cadence note:** Conducted at corpus #129, ONE UNIT EARLY, per Kenrin's explicit call (2026-07-18) — this audit satisfies the #130 every-10th slot; the next cadence fire is corpus **#140**.
- **Table ID:** [omb/budget-appendix-fy2027-leg-aoc-botanic-garden](file:///C:/Users/kenrin/Project/crossfoot/tables/omb/budget-appendix-fy2027-leg-aoc-botanic-garden.cells.json)
- **Source Document:** [budget-2027-app-2-3-legislative.pdf](file:///C:/Users/kenrin/Project/crossfoot/sources/omb/budget-2027-app-2-3-legislative.pdf), PDF page 16 (printed 28), right column (left column is Administrative Provisions legal text; Library of Congress chapter starts below)
- **Method:** fresh independent pypdfium2 4x render (`scratchpad/audit129-p16-4x.png`) + text-layer cross-check; FULL-coverage machine comparison of every transcribed cell against the render read (not a 10-cell sample), plus label/omission/metadata verification.
- **Status:** **GREEN after one completeness repair** (details below)

### 1. Verification results
- **Metadata / id / period:** id `009-0200-0-1-801`, three FY columns — **PASS**.
- **All 32 row labels:** match the render exactly, including the `1121 Appropriations transferred from other acct [001-0108]` cross-reference — **PASS**.
- **All 90 transcribed values:** machine-compared to the render read — **90/90 exact, zero mismatches**, negatives as printed (3020/3040), blank-vs-zero omissions all correct.
- **Cross-unit consistency:** `1121` (+2 c1) mirrors Capitol Grounds #117's `1120b` (-2 c1) transfer — **PASS**.
- **Arithmetic gate:** reconcile GREEN 0 warnings; pytest 10/10; full-corpus sweep 129/129 GREEN.

### 2. Finding and repair (the audit's catch)
- **Completeness defect:** the printed **`1001 Discretionary unobligated balance brought fwd, Oct 1` non-add memo row (17, c1 only)** — present in every sibling AoC unit — was missing from the transcription entirely (the unit had 90 of the 91 printed cells). Invisible to reconcile because the row is standalone-class (participates in no arithmetic).
- **Repair applied in this audit session** (per the #76 precedent: values untouched, mechanical insert): row added in print order as `standalone` with the standard memo `why`; all row indices/cell ids/relation references renumbered; unit_note carries the repair annotation. Post-repair: 91 cells / 17 relations, reconcile GREEN 0 warnings, sweep 129/129.

### 3. Audit conclusion
Antigravity's transcription is value-perfect (90/90 exact) with a single missing memo cell, now repaired. **GREEN.** Batch-shipped units remain auditable via the recorded NEXT.md numbering; the missing-memo-row failure mode (invisible to strict coverage) is exactly what this non-arithmetic cadence exists to catch — recommend transcribers cross-check row COUNTS against the print, not just relation closure. Next every-10th audit: corpus #140.
