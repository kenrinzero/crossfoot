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

| unit | source | table | min relations | types | size cap | status |
|---|---|---|---|---|---|---|
| treasury-mts/2026-05-receipts | `sources/treasury-mts/mts-202605.pdf` | Table 4 — Receipts of the U.S. Government (May FY2026) — major-classification slice (the full table is ~250 numeric cells, over the cap; see queued remainder) | 10 | sum | ≤ 120 cells | SHIPPED 2026-07-13 (87 cells, 42 relations, 11 tol-1 w/ quoted rounding note) |
| sec-10k/aapl-fy2023-balance-sheet | `sources/sec-10k/aapl-fy2023-balance-sheet-R5.htm` | Consolidated Balance Sheets (two fiscal-year columns; flagship: per-column roll-ups + assets = liabilities + equity) | 12 | sum | ≤ 140 cells | SHIPPED 2026-07-13 (58 cells, 18 exact relations, 4 share-count standalones) |
| census-p60/2023-income-a1 | `sources/census/p60-282.pdf` | Table A-1 — Households by Total Money Income (income brackets sum to total; percent distribution closes to 100) | 8 | sum, percent-closure | ≤ 150 cells | SHIPPED 2026-07-13 (88 cells, 8 sum relations (6 with non-default tol 0.1), 8 percent-closure relations (6 with non-default tol 0.1)) |

## Queued (need vendoring or sizing first)

| unit | note |
|---|---|
| bls-cpi/relative-importance-2024 | **Vendoring browser-gated** (bls.gov Akamai 403s curl AND Windows TLS — verified 2026-07-07). Needs Kenrin or a browser-capable session to save `https://www.bls.gov/cpi/tables/relative-importance/2024.htm` into `sources/bls-cpi/`. Superb crossfoot density (weights sum hierarchically to 100.000). |
| treasury-mts/2026-05-outlays | Same vendored PDF, Table 5 (outlays by agency) — size/split decision needed (may exceed cell cap → sub-table units). |
| treasury-mts/2026-05-receipts-detail | Remainder of Table 4 (p. 9): sub-classification rows under IIT / Social Insurance / Excise / Misc (~160 cells) — needs a slicing decision (likely 2 units: social-insurance subtree; everything-else). Sub-row footnote markers ¹² glue onto values in the text layer (¹5,514 / ²10,155) — transcriber must verify against a page render. Genuine source label typo on p. 9: "Adjustments Attrbutable to Prior Years-SECA" (OASI block) — transcribe as printed. |
| fec/2024-presidential-general | Election returns family; vendor the official FEC results PDF first (D1/web unit). |
| omb/budget-appendix-slice | Budget appendix family; pick one agency chapter, vendor, size-cap check. |

## Harness units (explicitly scoped; dispatch when needed)

| unit | note |
|---|---|
| tier1/strict-coverage-default | Flip `--strict-coverage` to the default; add a manifest column for granted `standalone` waivers. Do after the three starters are green. |
| tier4/weighted-average-relation | New relation type — only when a queued source actually needs it. |
