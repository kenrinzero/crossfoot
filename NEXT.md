# NEXT — rolling dispatch queue

The routing view: the next few sessions, in suggested order, with
difficulty and harness needs. `BACKLOG.md` stays the unit manifest
(specs, caps, minimums); `DESIGN.md` the frozen contract. This file is
for deciding *who does what next*.

**Rolling rules:** take the topmost session that fits your harness; when
shipped, move its block to *Shipped* (bottom, newest first) and append
newly-visible sessions to the queue. Re-sequencing is allowed — note why.

**Difficulty labels — this repo says D, not T:** task difficulty is
written **D1/D2/D3**, mapping 1:1 to the CHARTER's fleet-wide T1/T2/T3
(D1 = needs real judgment, D2 = well-specified execution, D3 =
deterministic + instantly checkable). Renamed locally (Kenrin,
2026-07-13) because crossfoot's own docs use "Tier 1 / Tier 3 / Tier 4"
for project *stages* (strict-coverage flip / footnote pass / new
relation types), and the two axes collide. "Tier N" in this repo always
means a stage, never difficulty. If a stray "T2" survives in older
crossfoot text, read it as D2.

**Harness notes for transcribers:**
- Neither host has poppler; PDF units use `uv run --with pdfplumber` (text
  layer) + a pypdfium2 page render for visual verification. The MTS PDF's
  text layer emits `(cid:NN)` tokens — decode `chr(NN+29)`, then verify
  against the render (footnote markers glue onto values: see BACKLOG).
- PDF units therefore want a **vision-capable** agent (the render check is
  mandatory discipline, not decoration). HTML units (Apple, BLS) do not.
- The gate for every transcription: `uv run python reconcile.py <file>`
  GREEN with 0 warnings (strict coverage is now default), relations ≥ manifest
  minimum, `uv run pytest` still green, one new file only.

---

## Queue

### 1. treasury-mts/2026-05-receipts-tax-detail — **D3** · local-only · vision needed (PDF)
Decided slice (4 of 4) of Table 4: IIT sub-rows (gross columns only) +
Excise + Miscellaneous sub-rows + re-anchored parent totals (~83 cells,
~34 relations, ~10 tol-1). **Why D3:** same as slice 3. **Hazard:**
footnote marker ² glues onto All Other FYTD gross ("210,155" — printed
value is 10,155). Note: single-source decompositions (e.g. Misc refunds
columns where only All Other prints a value) cannot be declared (schema
minItems 2) — role such printed totals as leaves feeding row identities,
per the pattern set in the majors slice.

## Not yet sequenced

- Remaining BLS slices (~6 units after housing: Food×2-3, Apparel+Transport,
  Medical+Recreation, Education+Other, aggregates) — **D3 once housing
  settles the pattern**; split proposal in BACKLOG's queued row.
- treasury-mts/2026-05-outlays — Table 5 size/split decision (D2), then units.
- fec/2024-presidential-general, omb/budget-appendix-slice — D1 (web)
  vendoring first.
- **Spot-audit at unit 10 is approaching** — 6 units shipped; after the
  queue item above it's 7. The audit is **D3**, MUST be a different
  agent than the transcribers it samples (DESIGN § 6), non-arithmetic
  checks (labels/units/periods + 10 sampled cells vs source) → AUDITS.md.

---

## Shipped

- 2026-07-13 · treasury-mts/2026-05-receipts-si-remainder (D3, Codex) —
  Unemployment Insurance + Other Retirement with E&GR/SI&R re-anchors;
  66 cells, 33 relations, 6 tol-1 with the page's quoted rounding note;
  strict-default GREEN and 66/66 source cross-check. Footnote marker ¹
  visually resolved: printed FYTD gross is 5,514, not text-layer 15,514.
  Commit `087066b`.

- 2026-07-13 · bls-cpi/relative-importance-2024-housing (D2, Ring) —
  Housing slice: Shelter + Fuels & utilities + Household furnishings;
  54 rows × 2 columns = 108 cells, 34 sum relations; 0 warnings,
  strict-default GREEN. First BLS unit — sets the extraction pattern for
  ~6 remaining slices. Commit `dd99331`.

- 2026-07-13 · treasury-mts/2026-05-receipts-employment-retirement (D2,
  went to Claude Fable 5) — E&GR subtree slice; 105 cells, 36 relations
  (18 fund roll-ups, 9 subtree roll-ups, 9 row identities), 6 tol-1 with
  quoted rounding note; strict-default GREEN. Commit `3cd6da7`. Hindsight:
  D2 was right for the *slicing* (the queued "likely 2 units" became 3 —
  105/66/83 once re-anchor rows were counted); the two remaining slices
  are decided → queued as D3. Source's "Attrbutable" typo landed here,
  transcribed as printed.

- 2026-07-13 · bls-cpi/relative-importance-2024 vendoring (D1, Kimi Work) —
  Vendored `https://www.bls.gov/cpi/tables/relative-importance/2024.htm`
  via Kimi WebBridge (browser session; Akamai 403s curl and Windows TLS).
  Source saved to `sources/bls-cpi/relative-importance-2024.htm` (90,118
  bytes, sha256 `2de17050f2ada5de1eff78c03b3df7fe5550d5490b09be6a89e6aab1d802044d`).
  Content sanity: 1 table, 322 rows × 2 columns = ~644 numeric cells,
  "All items" = 100.000/100.000 confirmed. Sized manifest row added:
  Housing slice (108 cells) moved to starter units; remaining slices
  (Food/Apparel/Transportation/Medical/Recreation/Education/Other/
  Aggregates) stay queued with proposed split sizes.

- 2026-07-13 · tier1/strict-coverage-default (D2, harness, Zed) —
  Flipped `--strict-coverage` to default in `reconcile.py`; added
  `standalone waivers` column to BACKLOG.md manifest; all three shipped
  tables + fixtures pass strict coverage (mini-uncovered still RED under
  strict).

- 2026-07-13 · census-p60/2023-income-a1 (D2, Antigravity) —
  Households by Total Money Income (All Races slice); 88 cells, 8 sum
  relations (6 with non-default tol 0.1), 8 percent-closure relations (6
  with non-default tol 0.1); strict-coverage GREEN. Commit `9b99afa`.

- 2026-07-13 · sec-10k/aapl-fy2023-balance-sheet (D2, Codex) —
  Apple FY2023 Consolidated Balance Sheets; 58 cells, 18 exact relations,
  4 share-count standalones; strict-coverage GREEN. Commit `0d31947`.

- 2026-07-13 · treasury-mts/2026-05-receipts (D2, went to Claude Fable 5) —
  Table 4 major-classification slice; 87 cells, 42 relations, 11 tol-1
  with quoted rounding note; strict-coverage GREEN. Commit `069e687`.
  In hindsight D2 was right: the cid-font decode + slice decision needed
  judgment; future *decided* slices of the same PDF are D3-adjacent.
