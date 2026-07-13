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
