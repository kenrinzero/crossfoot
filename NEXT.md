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

### 1. treasury-mts/2026-05-outlays-legislative — **D2** · local-only (PDF, **vision agent**)
Flagship first Table-5 (Outlays) unit: **Legislative Branch** (page 10),
self-contained, full 9-column model. ≈**96 cells**, ≈**18 relations**
(floor **14**), **0 standalone waivers**. Sets the extraction pattern for
the whole Table-5 family — column model, the `(**)`-omission convention,
the per-line net identity + per-column roll-ups, and MTS-rounding-note
tolerances are all fixed in
[`plans/treasury-mts-2026-05-outlays-table5.md`](plans/treasury-mts-2026-05-outlays-table5.md).
**Vision-capable agent required** (render page 10, verify against the
cid-decoded text layer — negatives and `(**)` markers present). Re-read
values from the PDF, never copy. Corpus unit #14.

## Not yet sequenced

- treasury-mts/2026-05-outlays — **Table 5 sized 2026-07-14** (~4,247 cells /
  29 sections / ~35–45 units at full-9; see the plan doc). Flagship queued
  above; the remaining 28 sections + capstone grand-total unit are deferred
  pending a post-flagship reassess (cap-fit sections are cheap single units,
  16 giants sub-split by bureau).
- fec/2024-presidential-general, omb/budget-appendix-slice — D1 (web)
  vendoring first.

---

## Shipped

- 2026-07-14 · treasury-mts/2026-05-outlays — Table 5 sizing + pattern (D2, Claude Opus 4.8) —
  Sized MTS Table 5 (Outlays, pages 10–23): **~4,247 cells / 662 rows / 29 sections**, 9-column model
  (3 periods × Gross/Applicable/Net) → **~35–45 units** at full fidelity, an order of magnitude past
  Table 4. Fixed the whole-family extraction pattern in
  `plans/treasury-mts-2026-05-outlays-table5.md`: column model, relation families (per-line
  `Net+Applicable=Gross`, per-column roll-ups, department totals, capstone `Total Outlays` +
  On/Off-Budget), and conventions — **`(**)` omitted like `......`**, negatives as printed, tolerances
  quote the MTS "Details may not add to totals due to rounding" note. Per Kenrin: **flagship first**
  (Legislative Branch, queued item 1), full-9 columns; remaining 28 sections + capstone deferred to a
  post-flagship reassess. No table file written.

- 2026-07-14 · bls-cpi/relative-importance-2024-special-aggregates (D3, local-only HTML) —
  Added `tables/bls-cpi/relative-importance-2024-special-aggregates.cells.json` for the special-aggregates
  block plus 8 main-table re-anchors. The unit encodes 72 cells, 36 sum relations, 8 tol-0.001 cases
  with the BLS rounding rationale, and 8 standalone waivers; reconcile is GREEN and pytest remains 10/10.

- 2026-07-14 · bls-cpi/relative-importance-2024-special-aggregates-plan (D1, Claude Opus 4.8) —
  Relation-topology plan for the special-aggregates block (source rows 295–322, 28 rows / 56 cells).
  These are cross-cutting "less X" reclassifications, not a hierarchy; the schema has only `sum`
  (no subtraction), so each "less X" index is declared as `(index) + X = whole`, re-anchoring the
  excluded main-table component X as a leaf. Decided: **8 re-anchors** (Food, Shelter, Medical care,
  Alcoholic beverages, Apparel, Footwear, Medical care services, Energy services) = 16 cells →
  **72 cells** total; **8 standalone waivers** (Transportation services, Other services, Domestically
  produced farm food, Utilities and public transportation — no in-slice or single-component
  complement, decompositions checked and declined); **36 relations** (18 identities × 2 columns),
  floor **30**, of which **8 at tol-0.001** per the BLS cost-weights rounding note. Full spec frozen
  in `plans/relative-importance-2024-special-aggregates.md`; arithmetic + coverage machine-verified
  (all 36 relations foot, every cell covered, counts reconcile). Resulting D3 unit queued as item 1.
  No table file written.

- 2026-07-14 · bls-cpi/relative-importance-2024-education-other (D3, Mavis) — Education and communication + Other goods and services hierarchies: rows 252–294, 43 rows × 2 columns = **86 cells**, **26 sum relations** (13 per column; 9 with non-default tol-0.001–0.01 per BLS cost-weights rounding note — the r14 (Info & info processing) and r18 (IT) hierarchies carry tol-0.01 to absorb 0.009 rounding gaps beyond the typical 0.001), 2 standalone waivers (Haircuts one-child alias of Personal care services, which becomes a leaf feeding the Personal care roll-up), strict-default GREEN (0 warnings), 10/10 pytest pass. Commit `0a7244f`.

- 2026-07-13 · bls-cpi/relative-importance-2024-medical-recreation (D3, Ring) —
  Medical care + Recreation hierarchies: rows 201–251, 51 rows × 2 columns =
  **102 cells**, **28 sum relations** (14 per column; 8 with tol-0.001–0.002
  per BLS cost-weights rounding note), 0 waivers, strict-default GREEN
  (0 warnings), 10/10 pytest pass. Commit `d10dceb`.

- 2026-07-13 · spot-audit/unit-10 (D3, Antigravity) — Non-arithmetic spot audit of BLS Apparel + Transportation unit #10 against source relative-importance-2024.htm: verified period, table title, column/row labels, and 10 sampled cells (100% match); logged results in AUDITS.md.

- 2026-07-13 · bls-cpi/relative-importance-2024-apparel-transportation (D3, Hunyuan/OpenClaw) — Apparel + Transportation hierarchies: full Apparel major group (Men's and boys' → Men's/Women's apparel, Footwear, Infants' and toddlers', Jewelry and watches) and full Transportation major group (Private: New/used motor vehicles, Motor fuel, Motor vehicle parts/equipment, Motor vehicle maintenance/repair, Motor vehicle insurance, Motor vehicle fees; Public: Airline fares, Other intercity, Intracity, Unsampled public). 54 rows × 2 columns = **108 cells**, **30 sum relations** (15 hierarchies × 2 columns; 9 with tol-0.001 quoting the BLS cost-weights page rounding note), 0 waivers, strict-default GREEN (0 warnings), 10/10 pytest pass. Source rows 146–200 (offset +6 from HTML segment positions; manifest labels the slice "147–200"). Corpus unit #10. Commit `0e42a46`.

- 2026-07-13 · bls-cpi/relative-importance-2024-food-remainder (D3, LongCat-2.0) —
  Food remainder: Fruits and vegetables through Other food at home,
  plus Food away from home and Alcoholic beverages, with Food at home /
  Food / Food and beverages re-anchored: 55 rows × 2 columns = **110
  cells**, **34 sum relations** (17 hierarchies × 2 columns; 10 with
  tol-0.001 per BLS rounding note), 0 waivers, strict-default GREEN
  (0 warnings), 10/10 pytest pass. All re-anchors re-read from the HTML,
  never copied from food-core. Commit `0e42a46`.

- 2026-07-13 · bls-cpi/relative-importance-2024-food-core (D3, Mistral Vibe) —
  Food at home, core branches: Cereals and bakery products through Dairy
  and related products (source rows 6-41, 36 rows × 2 columns = 72 cells, 22 sum
  relations, 4 with tol-0.001 per BLS rounding statement). Self-contained branch
  totals; Food-at-home parent not included. reconcile GREEN (0 warnings),
  pytest 10/10 pass. Commit `400238a`.

- 2026-07-13 · bls-cpi/relative-importance-2024-housing-rounding-repair (D3, Cline) —
  Replaced the Housing unit's 16 inferred tol-0.001 `why` strings with the
  exact rounding statement from the vendored BLS cost-weights page
  (`sources/bls-cpi/relative-importance-cost-weights.htm`): "just as with
  the officially published relative importance, due to rounding error these
  weights do not perfectly sum up to the total." Added `unit_note` field
  referencing the source. reconcile GREEN (0 warnings), pytest 10/10 pass.
  Commit `0c06898`.

- 2026-07-13 · bls-cpi/relative-importance-rounding-evidence (D2, Claude Opus 4.8) —
  Vendored the official BLS "CPI Cost Weights Homepage"
  (`https://www.bls.gov/cpi/tables/relative-importance/cost-weights.htm`)
  to `sources/bls-cpi/relative-importance-cost-weights.htm` (59,248 bytes,
  sha256 `c6108ce4…b3934186`) through the in-app browser — BLS Akamai-gates
  the page (403 to curl and Windows TLS). Captured the raw HTTP response
  body with `fetch(location.href).arrayBuffer()`, hashed the bytes
  in-browser, saved via a Blob download, and confirmed the on-disk sha256
  matched byte-for-byte before ledgering. Supplies the source-authorized
  rounding rationale ("just as with the officially published relative
  importance, due to rounding error these weights do not perfectly sum up
  to the total"), which unblocks the five sized BLS hierarchy units and
  the Housing `why`-field repair (now queue item 1). SOURCES.md ledgered;
  no table touched. Commit `02eee8b`.

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
