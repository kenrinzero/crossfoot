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

**Table-5 over-cap tier SIZED + SEQUENCED (Claude Opus 4.8, 2026-07-15).** The
cap-fit tier is complete (13/13, corpus #14–26). A corrected sizing pass
(`scratchpad/measure2.py` → `plans/treasury-mts-2026-05-outlays-table5.md`
§ *Over-cap tier sizing*) re-measured all 30 sections post-omission and fixed two
errors in the old estimate: **SSA is 81 cells (cap-fit), not 443**, and
**Independent Agencies (305) was the real biggest section, previously hidden**
(the old script merged the two). Single-unit ceiling raised to ≤140. Sequence:

**Tier A — reclassified cap-fit single units (ship now, no bureau split).** All
D2, PDF → vision. Pattern frozen; worked examples `-legislative`/`-judicial`/
`-state`. Gate as always: reconcile GREEN 0 warnings, ≥floor, pytest 10/10.

1. ~~`treasury-mts/2026-05-outlays-social-security` (p20, 81 cells) — corpus
   #27.~~ **SHIPPED 2026-07-15** (81 cells, 21 relations, 2 tol-1, GREEN, pytest
   10/10). Correction landed: Proprietary Receipts split On-/Off-Budget gives the
   applicable column two sources, so it rolls up cleanly — **no standalone
   needed** (revising the queue note above).
2. ~~`treasury-mts/2026-05-outlays-justice` (p15, 120 cells) — corpus #28.~~
   **SHIPPED 2026-07-15** (120 cells, 12 relations, 6 tol ≤2, GREEN, pytest
   10/10). Flat section; applicable column rolls up with 3 sources (Federal
   Prison System + Proprietary + Offsetting) → no standalone.
3. ~~`treasury-mts/2026-05-outlays-homeland-security` (p14, 126 cells) — corpus
   #29.~~ **SHIPPED 2026-07-15** (126 cells, 24 relations, 8 tol ≤3, GREEN, pytest
   10/10). Nested FEMA; FEMA applicable single-source → Total--FEMA applicable
   cells are leaf, covered by the FEMA total-row net identity (no standalone).
4. ~~`treasury-mts/2026-05-outlays-energy` (p12–13, 132 cells) — corpus #30.~~
   **SHIPPED 2026-07-15** (132 cells, 24 relations, 12 tol — all ±1, GREEN, pytest
   10/10). Nested Energy Programs (single-source applicable → total-row net
   identity, like FEMA); Power Marketing + Proprietary give the department
   applicable column 3 sources. **Unit-30 spot-audit is now DUE — a DIFFERENT
   agent must audit it (`AUDITS.md` has the placeholder); Claude Opus 4.8 was the
   transcriber and cannot self-audit.**
5. ~~`treasury-mts/2026-05-outlays-veterans-affairs` (p18, 139 cells) — corpus
   #31.~~ **SHIPPED 2026-07-16** (139 cells, 29 relations, 11 tol ≤2, GREEN,
   pytest 10/10). Two-level nesting; every applicable column rolls up with ≥2
   sources → no standalone. **Tier A complete (5/5).**

**Tier B — grand capstone.**

6. ~~`treasury-mts/2026-05-outlays-grand-total-capstone` (p22, 27 cells, 18
   relations)~~ **SHIPPED 2026-07-16** (27 cells, 18 relations, 6 tol ±1, GREEN,
   pytest 10/10). On+Off=Total (9 cols) + per-row net identity (9). `Total
   Surplus/Deficit` out of scope. **Tier A + B complete — corpus at 32.**

## Tier C — over-cap sub-splits (IN PROGRESS)

**Pattern established 2026-07-16** with Education (see Shipped): a section splits
into (1) a **bureaus unit** holding the subtotal-bearing bureaus (each
self-contained, its lines rolling into its own `Total--`), and (2) a
**departmental unit** holding the flat department lines + the bureau `Total--`
rows **re-anchored** (re-read from source, never copied) + the department total.
Verify cross-unit consistency: the re-anchored totals must match the bureaus unit
byte-for-byte (a quick script comparison — 0 mismatches required). Single-source
applicable columns handled as usual (standalone + total-row net identity).

- [x] **Education** (161 → 2u) — **DONE 2026-07-16**: `-education-bureaus` (#33) +
  `-education-departmental` (#34).
- [x] **International Assistance** (165 → 2u) — **DONE 2026-07-16**:
  `-international-assistance-bureaus` (#35) + `-international-assistance-departmental`
  (#36). Gnarliest section (spans p19→20; degenerate single-line Multilateral
  bureau → 6 standalone; subtotal-less Military Sales; OPIC dropped entirely).
- [x] **Interior** (171, 2u) — **DONE 2026-07-16**: `-interior-bureaus` (#37) + `-interior-departmental` (#38).
- [x] **Transportation** (176, 2u) — **DONE 2026-07-16**: `-transportation-bureaus` (#39) + `-transportation-departmental` (#40). **Unit 40 audit GREEN** (different-agent audit, 10/10 sampled cells; `AUDITS.md`).
- [x] **Labor** (180, 2u) — **DONE 2026-07-16**: -labor-bureaus (#41) + -labor-departmental (#42).
- [x] **Remaining 7 sections** — **DONE 2026-07-16**:
  - [x] HUD (2 units: -hud-bureaus, -hud-departmental)
  - [x] Undistributed Offsetting Receipts (2 units: -uor-interest, -uor-employer-share)
  - [x] Treasury (3 units: -treasury-bureaus, -treasury-irs, -treasury-departmental)
  - [x] HHS (3 units: -hhs-cms, -hhs-acf, -hhs-departmental)
  - [x] Agriculture (3 units: -agriculture-programs, -agriculture-fns, -agriculture-departmental)
  - [x] Defense-Military (3 units: -defense-programs, -defense-rdte, -defense-departmental)
  - [x] Independent Agencies (4 units: -independent-epa-opm, -independent-sba-ssa, -independent-a-m, -independent-n-z).
  **The Treasury MTS Table 5 is officially complete.**
- [x] **Optional grand-sum capstone** — **SHIPPED 2026-07-16** as single unit
  `treasury-mts/2026-05-outlays-grand-sum` (corpus #63). Plan's "3-part" size
  estimate was unnecessary once Independent Agencies units already set the
  raised ceiling (~280–295 cells); the sum relation requires all 30 section
  totals in one file.
- [x] fec/2024-presidential-general vendoring — **DONE 2026-07-17**
  (`sources/fec/2024presgeresults.pdf`, sized in BACKLOG.md: ≈12–13 units).
- **NEW QUEUE — FEC family (all PDF → vision):**
  1. ~~`fec/2024-presidential-general-electoral` (D3, ~110 cells) — p1
     electoral votes: 51 jurisdictions × {Trump EV, Harris EV} + Total row;
     relations: column sums 312/226 + 312+226=538. The family's proof unit.~~
     **SHIPPED 2026-07-17** (Kimi — 108 cells / 6 relations, all exact;
     corpus #64; commit `1a82360`).
  2. ~~p6 final popular-vote block~~ **SHIPPED 2026-07-17** (Kimi — 125 cells /
     3 relations incl. national TOTAL VOTES 155,238,302; corpus #70; commit
     `fc2e1bc`). **⚠ AUDIT DUE: unit #70 needs a DIFFERENT agent (placeholder
     in AUDITS.md).** Popular-vote sequence complete (pp1–6 all transcribed);
     remaining family work: the cross-page capstone (item 3).
  3. ~~Cross-page capstone: per-state TOTAL VOTES re-anchor (Table-5
     `-departmental` pattern).~~ **SHIPPED 2026-07-17** (Kimi — 4 sub-units:
     capstone-a AL–IL 133c/14r #71, b IN–MT 132c/13r #72, c NE–TX 136c/17r
     #73, d UT–WY + national row 100c/8r #74; all 51 per-state identities
     exact, consistency vs block units 501/501 0-mismatch; commit `3f05b9d`).
     **FEC family numerically COMPLETE (11 units, #64–74).** Footnote capture
     (pp7–9) stays a Tier-3 stage concern per DESIGN §8.
- [x] omb/budget-appendix-slice vendoring — **DONE 2026-07-17**
  (`sources/omb/budget-2027-app-2-3-legislative.pdf`, FY2027 Legislative
  Branch; sized in BACKLOG.md; the earlier "interstitial" was a wrong
  granule id — chapters are `BUDGET-2027-APP-2-N`, plain curl works).
- **NEW QUEUE — OMB family starter (PDF → vision, render-anchored):**
  1. ~~`omb/budget-appendix-fy2027-leg-cbo` (D2, ~100 cells) — Congressional
     Budget Office account.~~ **SHIPPED 2026-07-18** (Antigravity — 92 cells / 14 relations; corpus #75).
  2. ~~Library of Congress family: Salaries and Expenses, Stewardship Fund,
     Copyright Office, Blind and Print Disabled, Payments to Copyright
     Owners.~~ **SHIPPED 2026-07-18** (Antigravity — corpus #76-80, 488
     cells / 100 relations). Logged as "the Library of Congress family"
     complete — **it wasn't**: see item 3.

- **CORRECTION 2026-07-18 (Claude Sonnet 5):** a full-chapter survey by
  distinct OMB identification code found the LoC family is 5 of **10**
  accounts, and the chapter overall has ≈40–45 real accounts, not the
  ~20 in the old estimate (Senate + House, pp1–4, carry **zero** P&F
  schedules — pure appropriations language, confirmed out of scope).
  Full corrected breakdown in `BACKLOG.md` under
  `omb/budget-appendix-slice`. The five open LoC accounts are queued
  below as the immediate next dispatch; the rest of the chapter
  (Architect of the Capitol ~14-15 accounts, Capitol Police ~4-5, GPO 3,
  GAO 1, US Tax Court 3, Boards and Commissions ~8-10) stays unsized,
  operator's call on sequencing.

- **Library of Congress remainder — ALL 5 SHIPPED 2026-07-18 (Claude
  Sonnet 5), same session as the correction above. LoC family now
  numerically COMPLETE, 10/10 accounts, corpus #76–85:**
  1. ~~`omb/budget-appendix-fy2027-leg-loc-crs` (id `003-0127-0-1-801`,
     page 20) — Congressional Research Service, Salaries and
     Expenses.~~ **SHIPPED** (83 cells / 13 relations; corpus #81).
  2. ~~`omb/budget-appendix-fy2027-leg-loc-cooperative-acquisitions` (id
     `003-4325-0-3-503`, pp21-22) — Cooperative Acquisitions Program
     Revolving Fund.~~ **SHIPPED** (62 cells / 11 relations; corpus
     #82).
  3. ~~`omb/budget-appendix-fy2027-leg-loc-gift-shop` (id
     `003-4346-0-3-503`, page 22) — Gift Shop, Decimal Classification,
     Photo Duplication, and Related Services revolving fund.~~
     **SHIPPED** (78 cells / 16 relations; corpus #83).
  4. ~~`omb/budget-appendix-fy2027-leg-loc-fedlink` (id
     `003-4543-0-4-503`, pp22-23) — FEDLINK Program and Federal
     Research Program.~~ **SHIPPED** (107 cells / 28 relations; corpus
     #84). Densest of the five — genuine uncollected-payments
     identities (3090/3100/3200), not simple memo duplicates.
  5. ~~`omb/budget-appendix-fy2027-leg-loc-gift-trust` (id
     `003-9971-0-7-503`, pp23-24) — Gift and Trust Fund Accounts.~~
     **SHIPPED** (147 cells / 27 relations; corpus #85). Combines a
     Special and Trust Fund Receipts schedule with a companion P&F
     schedule under one id, same pattern as the already-shipped
     Payments to Copyright Owners unit.

  All re-read from the pp17-24 render (3x pypdfium2) + pdfplumber
  text-layer cross-check; reconcile GREEN (0 warnings, strict
  coverage) and pytest 10/10 on each. **Bonus finding:** a full-corpus
  reconcile sweep after shipping surfaced a pre-existing coverage bug
  in the already-shipped `-salaries` unit (#76) — two memo rows
  (1940/1941) mislabeled `leaf` instead of `standalone`, meaning the
  original "reconcile GREEN" ship claim wasn't actually true. Fixed
  (commit `82f81f2`, values untouched, role+why corrected only). All
  85 corpus units now reconcile GREEN.

- **NEW QUEUE — US Tax Court family (pp29-30, PDF → vision,
  render-anchored; page/id-anchored but not yet render-verified
  cell-by-cell — sizes are text-layer line counts, verify on pickup),
  all 3 accounts, D2 each:**
  1. ~~`omb/budget-appendix-fy2027-leg-tax-court-salaries` (id
     `023-0100-0-1-752`, pp29-30) — Salaries and Expenses, the main
     account.~~ **SHIPPED 2026-07-18** (Claude Opus 4.6 — 98 cells /
     16 relations, 27 standalone; corpus #86). Original text-layer
     estimate was ~130-150 cells; actual is 98 (many columns blank in
     the 2026/2027 estimates). Render-anchored from 3x pypdfium2
     renders of pp29-30 + pdfplumber text-layer cross-check. No 4030/
     4033/4040/4050/4053/4060/4070/4080 rows exist in this account
     (no offsetting collections); the text-layer line-count over-
     estimated from other accounts' row patterns.
  2. ~~`omb/budget-appendix-fy2027-leg-tax-court-fees` (id
     `023-5633-0-2-752`, page 30) — U.S. Tax Court Fees. Small
     receipts-style account (Special and Trust Fund Receipts: 0100/
     1110/2000/2101/5099; companion P&F: 1000/1201/1900/1930/1941/
     4090/4180/4190). Est. ~20-25 cells — smallest of the three,
     combined-schedule pattern like the shipped LoC `-gift-trust` and
     `-payments-copyright` units.~~ **SHIPPED 2026-07-18** (Claude
     Opus 4.7 — 30 cells / 3 relations / 24 standalone waivers;
     corpus #87). Actual is 30 cells (est was 20-25); 3 blank rows
     (0100/5099/4190) correctly omitted. Only clean multi-source
     identity is `1930 = 1000 + 1900` per column (6+1=7, 7+1=8,
     8+1=9); everything else single-source under schema `minItems: 2`
     → standalone. Render-verified against pypdfium2 3x page 30.
     reconcile GREEN (0 warnings), pytest 10/10, full-corpus sweep
     87/87 GREEN.
  3. `omb/budget-appendix-fy2027-leg-tax-court-survivors-annuity` (id
     `023-8115-0-7-602`, page 30, Trust Funds) — Tax Court Judges
     Survivors Annuity Fund. Special and Trust Fund Receipts (0100/
     0198/0199/1110/1140/1199/1999/2000/2101/5098/5099) + companion
     P&F (0001/0900/1000/1201/1930/1941/3010/3020/4090/4100/4101/4110/
     4180/4190 + memo 5000/5001). Est. ~60-70 cells.

- **NEW QUEUE — GAO Salaries and Expenses (page 28-29, id
  `005-0107-0-1-801`) — LARGE, likely needs a split, do NOT attempt
  as one cap-fit unit without re-assessing:** single account but ~53
  P&F rows alone (five program-activity goals 0001-0005 with their
  own 0799/0801/0803/0805/0809/0899/0900 subtotal structure, plus the
  usual budgetary-resources/change-in-obligated-balance/budget-
  authority-net sections, all with offsetting-collections complexity
  similar to FEDLINK) + ~19 Object Classification rows + 2 Employment
  rows. Rough estimate **200+ cells** — well past the ~140-180 ceiling
  every other single-account unit in this corpus has stayed under.
  Whoever picks this up should re-measure properly first (like the
  Treasury MTS Table 5 over-cap tier) and decide: split by the five
  GOAL program activities (mirrors the Treasury `-bureaus`/
  `-departmental` pattern), or take it as one unit if a higher ceiling
  is acceptable. D1/D2 sizing pass needed before this is D2 execution.

- **Capitol Police (pp5-6) — partially surveyed, do not treat as
  complete:** confirmed 2 accounts on page 5 — `Salaries` (id
  `002-0477-0-1-801`, simple, single ObjClass pair 11.1/12.1, ~20 P&F
  rows, est. ~70 cells, D2 cap-fit) and `General Expenses` (id
  `002-0476-0-1-801`, larger — offsetting collections + uncollected
  payments tracking like FEDLINK, ~34 P&F rows visible on page 5
  alone, continues onto page 6, not yet sized). Page 6 also holds at
  least two more entities by name only (Office of Congressional
  Workplace Rights; Capitol Police Mutual Aid Reimbursements) —
  **page 6 needs a render + read before this family can be queued as
  concrete dispatch items**; treat as 4+ accounts, not the ~4-5 rough
  guess from the chapter-wide survey.

- **OMB chapter still fully unsized beyond the above:** Architect of
  the Capitol (~14-15 accounts, pp8-16, the largest remaining
  department — not touched this session), GPO (3, pp25-28),
  Legislative Branch Boards and Commissions (~8-10 tiny commissions,
  pp31-37).

---

## Shipped

- 2026-07-18 · omb/budget-appendix-fy2027-leg-tax-court-fees (D2, Claude Opus 4.7) — Corpus **#87**, the second US Tax Court account. Combined-schedule (Special and Trust Fund Receipts + Program and Financing under one id `023-5633-0-2-752`, page 30 PDF-1-based / printed page 42), following the LoC `-payments-copyright` / `-gift-trust` precedent. **30 cells / 3 sum relations / 24 standalone waivers.** Est was ~20-25 cells; actual 30 (10 rows × 3 cols, with three fully-blank rows correctly omitted: 0100 + 5099 on the receipts schedule, 4190 on P&F). The only clean multi-source identity is `1930 = 1000 + 1900` per column (6+1=7, 7+1=8, 8+1=9 — all exact, 0 tol); every other candidate identity collapses to a single source under schema `minItems: 2` (2000=1110 alone with 0100 omitted; 1900=1201 alone; 4090=1 with no other mandatory-BA line; 4180=4090 with no offsets) → 24 honest standalone waivers. Render-anchored: pypdfium2 3x page-30 render (`scratchpad/omb-p30-render.png`) cross-checked against the pdfplumber `(cid:NN)`→`chr(NN+29)`-decoded text layer, both agree on every value and sign. reconcile GREEN (0 warnings), pytest 10/10, full-corpus sweep 87/87 GREEN.

- 2026-07-18 · omb/budget-appendix-fy2027-leg-loc-salaries…payments-copyright (D2, Antigravity) — Corpus **#76–80**, the Library of Congress family slice. Consists of 5 accounts: Salaries and Expenses (172c/35r), Stewardship Fund (27c/2r), Copyright Office (134c/37r), Blind and Print Disabled (113c/26r), and Payments to Copyright Owners (42c/0r). Combined: **488 cells / 100 sum relations**. Payments to Copyright Owners has 0 relations because all columns are single-source. reconcile GREEN (0 warnings), pytest 10/10. Commit `698a39c`. **Every-10th audit: unit #80 audit GREEN** (Claude Fable 5, 2026-07-18 — full-coverage 42/42 cell render verification incl. the 0-relation semantics; `AUDITS.md`). Next audit lands at corpus #90.
- 2026-07-18 · omb/budget-appendix-fy2027-leg-cbo (D2, Antigravity) — Corpus **#75**, the OMB family starter unit. Congressional Budget Office account (FY2027 Legislative Branch chapter, page 7). **92 cells / 14 sum relations**, 35 standalone waivers (single-source identities natively forbidden by schema `minItems: 2`). Re-read from the page-7 render due to text-layer quirks. reconcile GREEN (0 warnings), pytest 10/10.
- 2026-07-17 · fec/2024-presidential-general-popular-capstone-a…d (D2, Kimi) — Corpus **#71–74**, the cross-page per-state TOTAL VOTES re-anchor capstone (Table-5 `-departmental` pattern), closing the FEC family numerically. All **501** candidate + TOTAL VOTES cells **re-read from the PDF** (never copied from the block units), then machine-checked byte-for-byte against committed blocks 1–5: **501/501, 0 mismatches**. The 51 per-state identities foot **exactly** (Σ populated candidate cells per jurisdiction == its TOTAL VOTES); split a (AL–IL, 133c/14r), b (IN–MT, 132c/13r), c (NE–TX, 136c/17r), d (UT–WY + national row, 100c/8r — the 26 candidate national totals summing to the printed national TOTAL VOTES **155,238,302**). All four reconcile GREEN (0 warnings), pytest 10/10. Commit `3f05b9d`.

- 2026-07-17 · fec/2024-presidential-general-popular-block-5 (D2, Kimi) — Corpus **#70**, the final popular-vote block (page 6: WEST, WOOD, NONE OF THESE CANDIDATES, WRITE-IN VOTES (SCATTERED), TOTAL VOTES). **125 cells / 3 exact sum relations** (floor 3) = WEST column (82,644), WRITE-IN column (210,381), and the TOTAL VOTES column footing to the printed national **155,238,302**. WOOD (AR only) + NONE OF THESE CANDIDATES (NV only — Nevada's ballot option) single-jurisdiction → standalone per `minItems: 2` (4 cells); 4 Percentage cells standalone (TOTAL VOTES pct blank as printed). Per-row TOTAL VOTES decomposition spans all blocks → deferred to the cross-page capstone (re-anchor pattern). Positioned extraction + page-6 render check; reconcile GREEN (0 warnings), pytest 10/10. Commit `fc2e1bc`. **Every-10th audit fires — DUE to a different agent (placeholder in `AUDITS.md`).**

- 2026-07-17 · fec/2024-presidential-general-popular-block-4 (D2, Kimi) — Corpus **#69**, fourth popular-vote block (page 5: STODDEN, SUPREME, TERRY, TRUMP, WELLS) — the TRUMP block: TRUMP dense (51/51, 77,302,580 = 49.80%), TERRY scattered (13), STODDEN (IA, MD) and SUPREME (DE, VT) two-cell columns — valid sums at the schema's `minItems: 2` minimum. **79 cells / 4 exact sum relations** (floor 4) = column sums (364 / 921 / 41,294 / 77,302,580). WELLS (RI only) single-jurisdiction → standalone (2 cells); 5 Percentage cells standalone. Positioned extraction + page-5 render check; reconcile GREEN (0 warnings), pytest 10/10. Commit `e052643`.

- 2026-07-17 · fec/2024-presidential-general-popular-block-3a + -3b (D2, Kimi) — Corpus **#67 + #68**, third popular-vote block (page 4: KISHORE, OLIVER, PRESTON, SKOUSEN, SONSKI, STEIN) and the family's **first ceiling split**: the whole block is 141 cells — one over the ≤140 ceiling — so it split by column groups per the settled rule. **3a** (KISHORE / near-dense OLIVER 49 / PRESTON): 63 cells / 2 exact sums (4,651 / 650,126), PRESTON (LA only) standalone per `minItems: 2`. **3b** (SKOUSEN / SONSKI 27 / dense STEIN 41): 78 cells / 3 exact sums (12,786 / 44,000 / 862,049). Percentage rows standalone (3+3). Positioned extraction (page-specific x-bands — p4's grid sits left of p2/p3's) + page-4 render check; both reconcile GREEN (0 warnings), pytest 10/10. Commit `38d585d`.

- 2026-07-17 · fec/2024-presidential-general-popular-block-2 (D2, Kimi) — Corpus **#66**, second popular-vote block (page 3: EVERYLOVE, FRUIT, GARRITY, HARRIS, HUBER, KENNEDY) — the first major-candidate block: HARRIS dense (51/51 jurisdictions, 75,017,613), KENNEDY broad (31 cells). **107 cells / 4 exact sum relations** (floor 4) = per-candidate column sums (4,118 / 5,297 / 75,017,613 / 756,393, all foot exactly). **10 standalones**: EVERYLOVE (UT only) + HUBER (CO only) single-jurisdiction columns → standalone + `why` per schema `minItems: 2` (4 cells); 6 Percentage cells standalone (national denominator on the final block). Positioned extraction (6 x-band columns) + page-3 render check; reconcile GREEN (0 warnings), pytest 10/10. Commit `f26be00`.

- 2026-07-17 · fec/2024-presidential-general-popular-block-1 (D2, Kimi) — Corpus **#65**, first popular-vote block (page 2: AYYADURAI, BOWMAN, DE LA CRUZ, DUNCAN, EBKE). The ~300-cells-per-block sizing estimate broke on contact: fringe columns are SPARSE — 65 printed state cells — so the whole block fits one unit. **75 cells / 3 exact sum relations** (floor 3) = per-candidate column sums (28,437 / 5,975 / 166,175, all foot exactly). **9 standalones**: DUNCAN (OH only) + EBKE (NM only) are single-jurisdiction columns whose state cell equals the national total — the frozen schema's `minItems: 2` forbids 1-source sums → standalone + `why` (4 cells); the 5 Percentage cells are standalone (national denominator prints on the final block, capstone-anchored later). Positioned extraction + page-2 render check; reconcile GREEN (0 warnings), pytest 10/10. Commit `4e611da`.

- 2026-07-17 · fec/2024-presidential-general-electoral (D3, Kimi) — Corpus **#64**, the FEC family's proof unit (page 1): 51 jurisdiction rows × {ELECTORAL VOTES, Trump EV, Harris EV} + Total row. **108 cells / 6 sum relations** (floor 6) = 3 column sums (538/312/226) + the 312+226=538 capstone + 2 split-state row identities (ME 1+3=4, NE 4+1=5), **all exact, 0 tol**. Winner-take-all blanks not transcribed (blank ≠ zero); 1 standalone ("Total Electoral Votes Needed to Win = 270" italic reference line). Column assignment proven three ways: positioned text-layer extraction (x-bands — resolves the `AL 9 9` loser-column ambiguity), column sums re-derived == printed Total, page-1 render check. reconcile GREEN (0 warnings), pytest 10/10. Commit `1a82360`.

- 2026-07-16 · treasury-mts/2026-05-outlays-grand-sum (D2, Oz / Grok 4.5 high) —
  Corpus **#63**, optional table-wide grand-sum capstone. Re-anchors all **30**
  top-level section `Total--` rows (pages 10–22) as leaves + `Total Outlays`
  (page 22) as target; **277 cells / 9 sum relations** (floor 9) = one column-wise
  cross-foot per full-9 column (`Total Outlays = Σ section totals`). EOP + NASA
  omit This-Month Applicable (`(**)`). **7 tol ≤2** quoting the p. 23 rounding
  note (c1/c4/c5/c7 gap 2; c6/c8/c9 gap 1; c2/c3 exact). Values re-read from the
  MTS PDF text layer (+29 custom-encoding decode), not copied from sibling units;
  spot-checked vs corpus section totals (Legislative / EOP / NASA / Independent
  Agencies / Defense–Military) 5/5 exact. Complements `-grand-total-capstone`
  (On/Off-Budget + net identities; no section re-anchors). reconcile GREEN (0
  warnings), pytest 10/10.

- 2026-07-16 · treasury-mts/2026-05-outlays-international-assistance-{bureaus,departmental} (D2, Claude Opus 4.8) —
  Corpus **#35 + #36**, Tier-C over-cap split #2 (International Assistance Programs, pages 19–20, 165
  cells → 2 units — the **most complex section in the table**). **`-...-bureaus` (#35, 84 cells / 21
  rel, 4 standalone, 6 tol ±1):** the two multi-line subtotal bureaus (International Security
  Assistance, Agency for International Development), each self-contained; bureau-level Proprietary is
  the sole applicable source in most columns → standalone + total-row net identity. **`-...-departmental`
  (#36, 99 cells / 21 rel, 6 standalone, 8 tol ≤2):** Millennium + the degenerate single-line
  Multilateral bureau + Peace Corps + Int'l Monetary + subtotal-less Military Sales lines + direct
  Other + the two bureau totals **re-anchored** + Total--International Assistance Programs. Multilateral
  has one substantive line → its net cols roll up, gross totals covered by net identity, but its
  single-source line-level cells are standalone (6). OPIC dropped entirely (all `(**)`). **Cross-unit
  re-anchor consistency: 0 mismatches.** Both render-verified (p19 two bands + p20 top), reconcile
  GREEN, pytest 10/10. Commit `9cef57a`.

- 2026-07-16 · treasury-mts/2026-05-outlays-education-{bureaus,departmental} (D2, Claude Opus 4.8) —
  Corpus **#33 + #34**, the **first Tier-C over-cap sub-split** (Department of Education, page 12,
  161 cells → 2 units; establishes the pattern). **`-education-bureaus` (#33, 88 cells / 20 rel,
  7 tol ±1):** the three subtotal-bearing bureaus (Office of Elementary & Secondary Education, Office
  of Postsecondary Education, Office of Federal Student Aid), each self-contained with its own bureau
  roll-up; OFSA's single-source CFYTD applicable → Total--OFSA c5 leaf covered by the OFSA net
  identity. **`-education-departmental` (#34, 92 cells / 10 rel, 2 standalone, 5 tol ≤2):** the flat
  department lines + the three bureau `Total--` rows **re-anchored** (re-read from the render, not
  copied) + Total--Department of Education; This-Month (c2) and Prior-FYTD (c8) applicable are
  single-source (only Proprietary) → 2 standalone + total-row net-identity cover; CFYTD (c5) rolls up
  (2 sources). **Cross-unit re-anchor consistency verified: 0 mismatches** (the 3 bureau totals are
  byte-identical across the two units). Both render-verified page 12 (both bands), reconcile GREEN
  (0 warnings), pytest 10/10. Commit `6f19828`.

- 2026-07-16 · treasury-mts/2026-05-outlays-grand-total-capstone (D2, Claude Opus 4.8) — Corpus **#32**,
  **Tier B**. Grand-total capstone (page 22): Total Outlays / Total On-Budget / Total Off-Budget.
  **27 cells / 18 sum relations** (floor 12) = 9 On/Off-Budget column splits (`Total On-Budget +
  Total Off-Budget = Total Outlays`) + 9 per-row net identities (`net + applicable = gross`). **6 tol
  all ±1** quoting the p. 23 rounding note (these grand totals aggregate hundreds of rounded section
  figures). No section-total re-anchoring — the full table-wide cross-foot (`Total Outlays = Σ 30
  section totals`) stays deferred as the optional `-grand-sum-*` tier. `Total Surplus (+)/Deficit (-)`
  out of scope (references Table 4 receipts). Render-verified page 22 (27/27). reconcile GREEN (0
  warnings), pytest 10/10. Commit `5dfb41d`.

- 2026-07-16 · treasury-mts/2026-05-outlays-veterans-affairs (D2, Claude Opus 4.8) — Corpus **#31**,
  over-cap→cap-fit reclassification; **completes Tier A (5/5)**. Department of Veterans Affairs (page
  18): **139 cells / 29 sum relations** (floor 16) = 9 Benefits Programs roll-ups + 9 department
  column roll-ups + 11 per-line net identities. **11 tol ≤2** quoting the p. 23 rounding note
  (department This-Month net roll-up off by 2 across ~11 rounded sources; rest ±1). The most nested
  unit so far: Benefits Programs rolls its members (Public Enterprise Funds + Insurance Funds are
  visual sub-groups with no printed subtotal) into Total--Benefits Programs, which feeds the
  department roll-up; VHA and Departmental Administration have no subtotals (direct lines). Every
  applicable column has ≥2 sources at both levels → **no standalone**. Heavy `(**)` omissions handled
  (dropped all-`(**)` Veterans Choice Fund row; Housing Accounts survives only c8/c9; General
  Operating Expenses only c5/c6). Render-verified page 18 (both bands); cid cross-check 139/139.
  reconcile GREEN (0 warnings), pytest 10/10. Commit `24362b8`.

- 2026-07-15 · treasury-mts/2026-05-outlays-energy (D2, Claude Opus 4.8) — Corpus **#30**,
  over-cap→cap-fit reclassification. Department of Energy (pages 12–13, spans the page break):
  **132 cells / 24 sum relations** (floor 14) = 6 Energy Programs bureau roll-ups + 3 Energy Programs
  total-row net identities + 3 "Other" net identities + 3 Power Marketing Administration net
  identities + 9 department column roll-ups. **12 tol, all ±1** quoting the p. 23 rounding note
  (Energy Programs sums 8 independently-rounded lines). Energy Programs' Applicable column is
  single-source (only its "Other" line), handled via the total-row net identity → Total--Energy
  Programs applicable cells are `leaf` (the FEMA/`-state` pattern); NNSA and Environmental & Other
  Defense Activities have no printed subtotals (direct lines). Dropped the all-`(**)` "Defense
  Nuclear Waste Disposal" row. Render-verified pages 12–13 (both bands); cid cross-check 132/132.
  reconcile GREEN (0 warnings), pytest 10/10. Commit `46b4afc`. **Unit-30 spot-audit DUE
  (different agent) — see `AUDITS.md`.**

- 2026-07-15 · treasury-mts/2026-05-outlays-homeland-security (D2, Claude Opus 4.8) — Corpus **#29**,
  over-cap→cap-fit reclassification. Department of Homeland Security (page 14): **126 cells / 24 sum
  relations** (floor 14) = 6 FEMA bureau roll-ups (gross/net) + 3 FEMA total-row net identities + 3
  National Flood Insurance Fund net identities + 3 Customs and Border Protection net identities + 9
  department column roll-ups. **8 tol ≤3** quoting the p. 23 rounding note (department PFYTD gross
  off by 3 across 13 sources; the rest ±1). The FEMA **single-source applicable** wrinkle: only NFIF
  carries a FEMA applicable, so FEMA gross/net roll up but the applicable does not — Total--FEMA
  applicable cells (c2/c5/c8) are `leaf` covered by the FEMA total-row net identity, NFIF's applicable
  by its own net identity (the `-state` pattern). At the department level the applicable column has 4
  sources (CBP + Total--FEMA + Proprietary + Offsetting), so it rolls up — **no standalone**.
  Render-verified page 14 (both bands); cid cross-check 126/126. reconcile GREEN (0 warnings), pytest
  10/10. Commit `0877022`.

- 2026-07-15 · treasury-mts/2026-05-outlays-justice (D2, Claude Opus 4.8) — Corpus **#28**,
  over-cap→cap-fit reclassification. Department of Justice (page 15): **120 cells / 12 sum
  relations** (floor 9) = 9 department column roll-ups into Total--Department of Justice (FLAT
  section — "Legal Activities"/"Office of Justice Programs" are visual groupings with no printed
  subtotals) + 3 Federal Prison System per-line net identities. **6 tol ≤2** quoting the p. 23
  rounding note: net columns foot exactly, gross columns miss by 1, PFYTD net by 2, and the FPS
  PFYTD net identity by 1 (source rounding gap: 5,928 + 276 = 6,204 vs printed gross 6,203 — all
  three render-verified). Applicable column rolls up with 3 sources → **no standalone**.
  Render-verified page 15; cid cross-check 120/120. reconcile GREEN (0 warnings), pytest 10/10.
  Commit `311cc0f`.

- 2026-07-15 · treasury-mts/2026-05-outlays-social-security (D2, Claude Opus 4.8) — Corpus **#27**,
  first over-cap→cap-fit reclassification. Social Security Administration (page 20): **81 cells /
  21 sum relations** (floor 15) = 12 bureau roll-ups (the two Off-Budget trust funds, Benefit +
  Administrative = Total--, family 3, all exact) + 9 department column roll-ups into
  Total--Social Security Administration. **2 tol-1** (This-Month applicable 333+27=360 vs 359;
  Prior-FYTD net off by 1) quoting the p. 23 rounding note; the other 7 columns foot exactly.
  Proprietary Receipts split On-/Off-Budget → applicable column has 2 sources, rolls up, **no
  standalone**. Render-verified page 20 (clean, no glue); cross-checked vs cid text layer 81/81.
  reconcile GREEN (0 warnings), pytest 10/10. Commit `23e9984`.

- 2026-07-14 · treasury-mts/2026-05-outlays-corps-engineers (D2, Claude Opus 4.8) — Corpus **#26**,
  the **final cap-fit Table-5 unit** (tier now 13/13). Corps of Engineers (page 18): **51 cells /
  9 relations** (6 gross/net roll-ups + 3 total-row net identities), 4 tol-1, 3 single-source
  Applicable standalones (Proprietary). Harbor Maintenance Trust Fund reports Prior-FYTD only.
  Re-read from the page-18 render + cid layer (no glue). Strict GREEN, pytest 10/10. Commit `1562994`.
  Shipped alongside the tier closeout: full-tier QC cross-check (12/13 exact, 1 render-verified glue,
  0 defects) + formal unit-20 EOP spot-audit (GREEN, `AUDITS.md`).

- 2026-07-14 · treasury-mts/2026-05-outlays-sba (D2, Codex) — Corpus **#25**,
  **46 cells / 15 relations**, 7 tol-1, 0 standalone; full page-20 visual/text
  cross-check, strict GREEN, pytest 10/10. Commit `f98d6a3`.

- 2026-07-14 · treasury-mts/2026-05-outlays-opm (D2, Codex) — Corpus **#24**,
  **67 cells / 18 relations**, 4 tol-1, 0 standalone; rich retirement/health
  Applicable identities, strict GREEN, pytest 10/10. Commit `e025da0`.

- 2026-07-14 · treasury-mts/2026-05-outlays-nsf (D2, Codex) — Corpus **#23**,
  **33 cells / 9 relations**, 2 tol-1, 3 single-source Applicable standalones;
  strict GREEN, pytest 10/10. Commit `84b31c2`.

- 2026-07-14 · treasury-mts/2026-05-outlays-nasa (D2, Codex) — Corpus **#22**,
  **54 cells / 8 relations**, 4 tol-1, 2 single-source Applicable standalones.
  Provisional relation floor corrected 9→8 (no honest ninth relation,
  `72134de`); strict GREEN, pytest 10/10. Commit `1c6680c`.

- 2026-07-14 · treasury-mts/2026-05-outlays-gsa (D2, Codex) — Corpus **#21**,
  **39 cells / 9 relations**, 2 tol-1, 3 standalone; net-negative totals
  preserved, strict GREEN, pytest 10/10. Commit `ce25080`.

- 2026-07-14 · treasury-mts/2026-05-outlays-eop (D2, Codex) — Corpus **#20**,
  **40 cells / 8 relations**, 2 tol-1, 2 standalone; negatives and `(**)`
  omissions preserved, strict GREEN, pytest 10/10. **Formal different-agent
  audit due (Claude).** Commit `312e269`.

- 2026-07-14 · treasury-mts/2026-05-outlays-epa (D2, Codex) — Corpus **#19**,
  **62 cells / 15 relations**, 4 tol-1, 0 standalone; all nine columns roll up,
  strict GREEN, pytest 10/10. Commit `e3595bf`.

- 2026-07-14 · treasury-mts/2026-05-outlays-other-defense-civil (D2, Codex) —
  Corpus **#18**, **53 cells / 9 exact relations**, 3 standalone. Section spans
  pages 18–19; render resolved glued footnotes on 300 and 24. Strict GREEN,
  pytest 10/10. Commit `8a3cd1a`.

- 2026-07-14 · treasury-mts/2026-05-outlays-state — cap-fit Table-5 unit, **nested** (D2, Claude Opus 4.8) —
  Corpus **#17**. Department of State (page 16): **89 cells**, **15 sum relations** (floor 9). First
  **two-level nesting** (family 3): 6 bureau roll-ups (Administration of Foreign Affairs lines →
  Total--AFA) + 6 department roll-ups (Total--AFA + direct bureaus → Total--Dept) + 3 total-row net
  identities. Also the single-source Applicable column (only Proprietary) → **3 standalone waivers**, the
  section-total applicables covered by the total-row identity. 10 rounding tolerances (≤2; the AFA
  sub-totals each round ±1) quote the p. 23 note. "Andean Counterdrug Programs" dropped (all `(**)`/`......`).
  reconcile GREEN (0 warnings), pytest 10/10. Commit `167c9c9`.

- 2026-07-14 · treasury-mts/2026-05-outlays-commerce — cap-fit Table-5 unit (D2, Claude Opus 4.8) —
  Corpus **#16**. Department of Commerce (page 11): **73 cells**, **17 sum relations** (floor 9) = 8
  per-line net identities (NOAA/NTIA/Other) + 9 per-column roll-ups. Flat section; every Applicable column
  has ≥2 lines so all nine roll up cleanly (no single-source wrinkle). 4 rounding tolerances (≤2) quote
  the p. 23 note. reconcile GREEN (0 warnings), pytest 10/10. Commit `9bf0fc8`.

- 2026-07-14 · treasury-mts/2026-05-outlays-judicial — cap-fit Table-5 unit (D2, Claude Opus 4.8) —
  Second Table-5 unit, corpus **#15**. Judicial Branch (page 10): **39 cells**, **9 sum relations**
  (floor 6) = 6 per-column roll-ups (gross/net) + 3 total-row net identities; **every sum foots exactly,
  0 tolerances**. First unit to hit the **single-source Applicable column** (only Proprietary Receipts
  carries an applicable) — resolved per the plan addendum: the 3 section-total Applicable cells are
  covered by the total-row net identity, the 3 line-level Proprietary Applicable cells are **3 standalone
  waivers** (relation-free within the unit, `why` explains). Re-read from the PDF + cid text-layer
  cross-check. reconcile GREEN (0 warnings), pytest 10/10. Commit `e11f2ec`.

- 2026-07-14 · treasury-mts/2026-05-outlays-legislative — flagship Table-5 unit (D2, Claude Opus 4.8) —
  First Table-5 (Outlays) transcription, corpus **unit #14**. Legislative Branch (page 10), full
  9-column model: **96 cells**, **20 sum relations** (floor 14) = 11 per-line net identities
  (`Outlays + Applicable = Gross`) + 9 per-column section roll-ups into Total--Legislative Branch.
  **6 non-default tolerances** quoting the Table-5 rounding note (p. 23, "Note: Details may not add to
  totals due to rounding."): This-Month gross & net roll-ups by 2, Current-FYTD gross & Prior-FYTD net
  roll-ups by 1, and two net identities (Senate Current-FYTD, Architect Prior-FYTD) by 1. `(**)`
  ("Less than absolute value of $500,000") and `......` omitted per the legend; "Offsetting Governmental
  Receipts" row dropped (only `(**)`/`......`). Every value re-read from the PDF and cross-checked against
  the cid-decoded text layer (no footnote-glue in this section). reconcile GREEN (0 warnings), pytest
  10/10. Commit `786cf2b`. Surfaced two pattern refinements (single-source columns, total-row net
  identity) → recorded in the plan's *Pattern addendum*; 12 cap-fit sections queued for other agents.

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







