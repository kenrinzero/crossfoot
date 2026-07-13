# Crossfoot — Unit Manifest

One unit = ONE vendored source table → one `tables/<family>/<table-id>.cells.json`
that makes `python reconcile.py <file>` exit 0 **with zero coverage
warnings** and ≥ `expected_relations_min` declared relations. Transcription
units never edit `reconcile.py`, the schema, or vendored sources; new
relation types are separate harness units (DESIGN.md). Every 10th shipped
unit triggers a non-arithmetic spot-audit by a different agent (AUDITS.md).

Source vendoring is its own D1/web unit — a transcription unit only ever
reads `sources/` locally. (Difficulty is written D1/D2/D3 in this repo —
= CHARTER T1/T2/T3 — because "Tier N" here names project stages; see
NEXT.md.)

## Starter units (READY — sources vendored 2026-07-07)

| unit | source | table | min relations | types | size cap | standalone waivers | status |
|---|---|---|---|---|---|---|---|
| treasury-mts/2026-05-receipts | `sources/treasury-mts/mts-202605.pdf` | Table 4 — Receipts of the U.S. Government (May FY2026) — major-classification slice (the full table is ~250 numeric cells, over the cap; see queued remainder) | 10 | sum | ≤ 120 cells | 0 | SHIPPED 2026-07-13 (87 cells, 42 relations, 11 tol-1 w/ quoted rounding note) |
| bls-cpi/relative-importance-2024-housing | `sources/bls-cpi/relative-importance-2024.htm` | Relative importance of components — Housing slice (shelter + fuels/utilities + household furnishings and operations; 2-column: CPI-U and CPI-W relative weights) | 12 | sum | ≤ 120 cells | 0 | READY 2026-07-13 — source vendored; 54 rows = 108 cells. Dense sum structure: shelter subtotals, fuels/utilities subtotals, furnishings subtotals, all rolling up to Housing = 44.201 / 41.932. Part of larger table; other slices remain queued. |
| sec-10k/aapl-fy2023-balance-sheet | `sources/sec-10k/aapl-fy2023-balance-sheet-R5.htm` | Consolidated Balance Sheets (two fiscal-year columns; flagship: per-column roll-ups + assets = liabilities + equity) | 12 | sum | ≤ 140 cells | 4 (share-count) | SHIPPED 2026-07-13 (58 cells, 18 exact relations, 4 share-count standalones) |
| census-p60/2023-income-a1 | `sources/census/p60-282.pdf` | Table A-1 — Households by Total Money Income (income brackets sum to total; percent distribution closes to 100) | 8 | sum, percent-closure | ≤ 150 cells | 0 | SHIPPED 2026-07-13 (88 cells, 8 sum relations (6 with non-default tol 0.1), 8 percent-closure relations (6 with non-default tol 0.1)) |
| treasury-mts/2026-05-receipts-employment-retirement | `sources/treasury-mts/mts-202605.pdf` | Table 4 — Employment & General Retirement subtree (slice 2 of 4: OASI/DI/HI trust-fund pyramids + Railroad Retirement + subtree total; self-contained, no overlap with other units) | 30 | sum | ≤ 120 cells | 0 | SHIPPED 2026-07-13 (105 cells, 36 relations, 6 tol-1 w/ quoted rounding note) |
| treasury-mts/2026-05-receipts-si-remainder | `sources/treasury-mts/mts-202605.pdf` | Table 4 — Social Insurance remainder (slice 3 of 4): Unemployment Insurance + Other Retirement blocks, plus the E&GR total row (as leaf sources) and the SI&R grand total row (as targets) re-anchored — those two rows also appear in sibling units; re-transcribe, never copy | 25 | sum | ≤ 120 cells (planned ~66) | 0 | READY — **hazard:** footnote marker ¹ glues onto Federal Employees' Retirement FYTD gross in the text layer ("15,514"; printed value is 5,514) — verify against a page render |
| treasury-mts/2026-05-receipts-tax-detail | `sources/treasury-mts/mts-202605.pdf` | Table 4 — tax detail (slice 4 of 4): Individual Income Tax sub-rows (gross columns only) + Excise Taxes + Miscellaneous Receipts sub-rows, with the IIT-total gross cells and the Excise/Misc total rows re-anchored (also present in the majors slice; re-transcribe, never copy) | 25 | sum | ≤ 120 cells (planned ~83) | 0 | READY — **hazard:** footnote marker ² glues onto All Other FYTD gross in the text layer ("210,155"; printed value is 10,155) — verify against a page render |

## Queued (need vendoring or sizing first)

| unit | standalone waivers (est.) | note |
|---|---|---|
| bls-cpi/relative-importance-2024 | TBD | **VENDORED 2026-07-13** via Kimi WebBridge (browser session). Source: `sources/bls-cpi/relative-importance-2024.htm` (90,118 bytes, sha256 `2de17050...`). Table: 322 rows × 2 columns = ~644 numeric cells, well over the 120-cell cap. Requires slicing into ≤120-cell units. Proposed split (verify before trusting): Housing (54 rows = 108 cells, self-contained); Apparel+Transportation (54 rows = 108 cells); Medical care+Recreation (51 rows = 102 cells); Education/communication+Other goods (44 rows = 88 cells); Cross-cutting aggregates (27 rows = 54 cells); Food and beverages (91 rows = 182 cells — needs 2-3 sub-slices, e.g. Food at home split into two ~40-row halves + Food away+Alcohol). The "All items" total (100.000/100.000) is verified. Superb crossfoot density (weights sum hierarchically to 100.000). |
| treasury-mts/2026-05-outlays | TBD | Same vendored PDF, Table 5 (outlays by agency) — size/split decision needed (may exceed cell cap → sub-table units). |
| treasury-mts/2026-05-receipts-detail | — | **SPLIT 2026-07-13** — the "likely 2 units" estimate didn't survive contact (remainder + re-anchor rows ≈ 105+66+83 cells): now three slices in the starter table — `-employment-retirement` (SHIPPED), `-si-remainder` (READY), `-tax-detail` (READY). The p. 9 label typo ("Attrbutable", OASI block) landed in the shipped slice, transcribed as printed. |
| fec/2024-presidential-general | TBD | Election returns family; vendor the official FEC results PDF first (D1/web unit). |
| omb/budget-appendix-slice | TBD | Budget appendix family; pick one agency chapter, vendor, size-cap check. |

## Harness units (explicitly scoped; dispatch when needed)

| unit | note |
|---|---|
| tier1/strict-coverage-default | **SHIPPED 2026-07-13** — flipped `--strict-coverage` to default; added manifest column for granted `standalone` waivers. |
| tier4/weighted-average-relation | New relation type — only when a queued source actually needs it. |
