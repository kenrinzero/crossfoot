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

### 1. bls-cpi/relative-importance-rounding-evidence — **D2** · browser needed (web)
Vendor and ledger the official BLS `cost-weights.htm` page. It supplies
the missing source-authorized tolerance rationale: “just as with the
officially published relative importance, due to rounding error these
weights do not perfectly sum up to the total.” The decided URL is
`https://www.bls.gov/cpi/tables/relative-importance/cost-weights.htm`;
BLS may require the same browser/network-response capture used for the
2024 table. **Why D2:** source selection is settled; this is careful
browser capture + provenance verification. Do not edit a table in the
same vendoring unit.

### 2. bls-cpi/relative-importance-2024-housing-rounding-repair — **D3** · local-only · depends on item 1
Replace the Housing unit's 16 inferred tol-0.001 `why` strings with the
exact rounding statement from the newly vendored BLS page, referencing
that source in `unit_note`; reconcile + pytest. One existing table file
only. This closes the provenance gap before the pattern is copied.

### 3. bls-cpi/relative-importance-2024-food-core — **D3** · local-only (HTML) · depends on item 1
Cereals and bakery products through Dairy and related products: numeric
rows 5–40 of the source table, 36 rows × 2 columns = **72 cells**, min
18 sum relations, 0 waivers. Self-contained branch totals; do not add the
incomplete Food-at-home parent. Use the vendored rounding statement for
any tol-0.001 relation that needs it.

### 4. bls-cpi/relative-importance-2024-food-remainder — **D3** · local-only (HTML) · depends on item 1
Fruits and vegetables through Other food at home, then Food away from
home + Alcoholic beverages, with Food at home / Food / Food and beverages
re-anchored: numeric rows 2–4 and 41–92, 55 rows × 2 columns = **110
cells**, min 26 sum relations, 0 waivers. All re-anchors are re-read from
the HTML, never copied from another unit.

### 5. bls-cpi/relative-importance-2024-apparel-transportation — **D3** · local-only (HTML) · depends on item 1
Complete Apparel + Transportation hierarchies: numeric rows 147–200,
54 rows × 2 columns = **108 cells**, min 24 sum relations, 0 waivers.
This becomes corpus unit 10 if items 3–5 ship in order.

### 6. spot-audit/unit-10 — **D3** · local-only · different agent required
Immediately after corpus unit 10 ships, re-read labels, units, periods,
and 10 sampled cells against the vendored sources; append the result to
`AUDITS.md`. The auditor must be a **different agent from item 5's
transcriber**. This is non-arithmetic verification; do not modify the
audited table.

### 7. bls-cpi/relative-importance-2024-medical-recreation — **D3** · local-only (HTML) · depends on item 1
Complete Medical care + Recreation hierarchies: numeric rows 201–251,
51 rows × 2 columns = **102 cells**, min 20 sum relations, 0 waivers.

### 8. bls-cpi/relative-importance-2024-education-other — **D3** · local-only (HTML) · depends on item 1
Education and communication + Other goods and services: numeric rows
252–294, 43 rows × 2 columns = **86 cells**, min 18 sum relations.
Expected waivers: 2 cells for Haircuts and other personal care services,
whose identical one-child parent cannot be declared under sum minItems 2;
the parent remains a leaf feeding the wider Personal care roll-up.

### 9. bls-cpi/relative-importance-2024-special-aggregates-plan — **D2** · local-only (HTML)
Plan the relation topology for numeric rows 295–322: **28 rows / 56
cells** before re-anchors (correcting the earlier 27/54 estimate). These
are cross-cutting “less X” indexes rather than one hierarchy; decide the
main-table re-anchors, waiver count, final cap, and relation floor, then
append the resulting D3 transcription unit to this queue. No table file
in the planning session.

## Not yet sequenced

- treasury-mts/2026-05-outlays — Table 5 size/split decision (D2), then units.
- fec/2024-presidential-general, omb/budget-appendix-slice — D1 (web)
  vendoring first.
- Special-aggregates transcription becomes visible after queue item 9.

---

## Shipped

- 2026-07-13 · treasury-mts/2026-05-receipts-tax-detail (D3, Codex) —
  Final Table 4 slice: IIT gross subrows + complete Excise and Miscellaneous
  detail; 82 cells, 34 relations, 10 tol-1 with the page's quoted rounding
  note; strict-default GREEN and 82/82 decoded-source cross-check. Visual
  render resolved superscript footnote ²: printed All Other current-FYTD
  gross is 10,155, not text-layer 210,155. Commit `64ffb41`.

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
