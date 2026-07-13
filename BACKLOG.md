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

## Sized transcription units (sources vendored)

| unit | source | table | min relations | types | size cap | standalone waivers | status |
|---|---|---|---|---|---|---|---|
| treasury-mts/2026-05-receipts | `sources/treasury-mts/mts-202605.pdf` | Table 4 — Receipts of the U.S. Government (May FY2026) — major-classification slice (the full table is ~250 numeric cells, over the cap; see queued remainder) | 10 | sum | ≤ 120 cells | 0 | SHIPPED 2026-07-13 (87 cells, 42 relations, 11 tol-1 w/ quoted rounding note) |
| bls-cpi/relative-importance-2024-housing | `sources/bls-cpi/relative-importance-2024.htm` | Relative importance of components — Housing slice (shelter + fuels/utilities + household furnishings and operations; 2-column: CPI-U and CPI-W relative weights) | 12 | sum | ≤ 120 cells | 0 | SHIPPED 2026-07-13 (108 cells, 34 relations, strict-default GREEN) |
| bls-cpi/relative-importance-2024-food-core | `sources/bls-cpi/relative-importance-2024.htm` | Food at home, core branches: Cereals and bakery products through Dairy and related products (source numeric rows 5–40; two columns) | 18 | sum | ≤ 120 cells (72 sized) | 0 | READY (D3) — rounding source vendored 2026-07-13 (`sources/bls-cpi/relative-importance-cost-weights.htm`); quote it for any tol-0.001 relation |
| bls-cpi/relative-importance-2024-food-remainder | `sources/bls-cpi/relative-importance-2024.htm` | Food remainder: Fruits and vegetables through Other food at home, plus Food away from home and Alcoholic beverages; re-anchor Food at home, Food, and Food and beverages (source numeric rows 2–4 and 41–92; two columns) | 26 | sum | ≤ 120 cells (110 sized) | 0 | READY (D3) — rounding source vendored 2026-07-13 (`sources/bls-cpi/relative-importance-cost-weights.htm`); quote it for any tol-0.001 relation |
| bls-cpi/relative-importance-2024-apparel-transportation | `sources/bls-cpi/relative-importance-2024.htm` | Apparel + Transportation hierarchies (source numeric rows 147–200; two columns) | 24 | sum | ≤ 120 cells (108 sized) | 0 | READY (D3) — rounding source vendored 2026-07-13 (`sources/bls-cpi/relative-importance-cost-weights.htm`); quote it for any tol-0.001 relation |
| bls-cpi/relative-importance-2024-medical-recreation | `sources/bls-cpi/relative-importance-2024.htm` | Medical care + Recreation hierarchies (source numeric rows 201–251; two columns) | 20 | sum | ≤ 120 cells (102 sized) | 0 | READY (D3) — rounding source vendored 2026-07-13 (`sources/bls-cpi/relative-importance-cost-weights.htm`); quote it for any tol-0.001 relation |
| bls-cpi/relative-importance-2024-education-other | `sources/bls-cpi/relative-importance-2024.htm` | Education and communication + Other goods and services hierarchies (source numeric rows 252–294; two columns) | 18 | sum | ≤ 120 cells (86 sized) | 2 est. (Haircuts one-child alias) | READY (D3) — rounding source vendored 2026-07-13 (`sources/bls-cpi/relative-importance-cost-weights.htm`); quote it for any tol-0.001 relation |
| sec-10k/aapl-fy2023-balance-sheet | `sources/sec-10k/aapl-fy2023-balance-sheet-R5.htm` | Consolidated Balance Sheets (two fiscal-year columns; flagship: per-column roll-ups + assets = liabilities + equity) | 12 | sum | ≤ 140 cells | 4 (share-count) | SHIPPED 2026-07-13 (58 cells, 18 exact relations, 4 share-count standalones) |
| census-p60/2023-income-a1 | `sources/census/p60-282.pdf` | Table A-1 — Households by Total Money Income (income brackets sum to total; percent distribution closes to 100) | 8 | sum, percent-closure | ≤ 150 cells | 0 | SHIPPED 2026-07-13 (88 cells, 8 sum relations (6 with non-default tol 0.1), 8 percent-closure relations (6 with non-default tol 0.1)) |
| treasury-mts/2026-05-receipts-employment-retirement | `sources/treasury-mts/mts-202605.pdf` | Table 4 — Employment & General Retirement subtree (slice 2 of 4: OASI/DI/HI trust-fund pyramids + Railroad Retirement + subtree total; self-contained, no overlap with other units) | 30 | sum | ≤ 120 cells | 0 | SHIPPED 2026-07-13 (105 cells, 36 relations, 6 tol-1 w/ quoted rounding note) |
| treasury-mts/2026-05-receipts-si-remainder | `sources/treasury-mts/mts-202605.pdf` | Table 4 — Social Insurance remainder (slice 3 of 4): Unemployment Insurance + Other Retirement blocks, plus the E&GR total row (as leaf sources) and the SI&R grand total row (as targets) re-anchored — those two rows also appear in sibling units; re-transcribe, never copy | 25 | sum | ≤ 120 cells (planned ~66) | 0 | SHIPPED 2026-07-13 (66 cells, 33 relations, 6 tol-1 w/ quoted rounding note; footnote-marker hazard visually resolved) |
| treasury-mts/2026-05-receipts-tax-detail | `sources/treasury-mts/mts-202605.pdf` | Table 4 — tax detail (slice 4 of 4): Individual Income Tax sub-rows (gross columns only) + Excise Taxes + Miscellaneous Receipts sub-rows, with the IIT-total gross cells and the Excise/Misc total rows re-anchored (also present in the majors slice; re-transcribe, never copy) | 25 | sum | ≤ 120 cells | 0 | SHIPPED 2026-07-13 (82 cells, 34 relations, 10 tol-1 w/ quoted rounding note; footnote-marker hazard visually resolved) |

## Queued (need vendoring or sizing first)

| unit | standalone waivers (est.) | note |
|---|---|---|
| bls-cpi/relative-importance-rounding-evidence | — | **VENDORED 2026-07-13.** `sources/bls-cpi/relative-importance-cost-weights.htm` (59,248 bytes, sha256 `c6108ce4…b3934186`) captured through the in-app browser (Akamai bot-gated) and ledgered in SOURCES.md. It supplies the source-authorized rounding rationale: "just as with the officially published relative importance, due to rounding error these weights do not perfectly sum up to the total." Remaining gate step is the Housing `why`-field repair (separate D3 unit, NEXT.md item 1); the five sized BLS hierarchy units are now unblocked. |
| bls-cpi/relative-importance-2024-special-aggregates | TBD | Source numeric rows 295–322 are **28 rows / 56 cells** before any re-anchors (correcting the earlier 27/54 estimate). Needs a D1 relation-plan session: these are cross-cutting “less X” indexes rather than a single hierarchy, so decide which main-table components to re-anchor and size again before transcription. |
| treasury-mts/2026-05-outlays | TBD | Same vendored PDF, Table 5 (outlays by agency) — size/split decision needed (may exceed cell cap → sub-table units). |
| treasury-mts/2026-05-receipts-detail | — | **SPLIT + COMPLETE 2026-07-13** — the "likely 2 units" estimate became three slices once re-anchor rows were counted: `-employment-retirement` (105 cells), `-si-remainder` (66), and `-tax-detail` (82), all SHIPPED. The p. 9 label typo ("Attrbutable", OASI block) landed in the first slice, transcribed as printed. |
| fec/2024-presidential-general | TBD | Election returns family; vendor the official FEC results PDF first (D1/web unit). |
| omb/budget-appendix-slice | TBD | Budget appendix family; pick one agency chapter, vendor, size-cap check. |

## Harness units (explicitly scoped; dispatch when needed)

| unit | note |
|---|---|
| tier1/strict-coverage-default | **SHIPPED 2026-07-13** — flipped `--strict-coverage` to default; added manifest column for granted `standalone` waivers. |
| tier4/weighted-average-relation | New relation type — only when a queued source actually needs it. |
