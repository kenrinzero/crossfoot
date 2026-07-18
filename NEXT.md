# NEXT — rolling dispatch queue

The routing view: the next few sessions, in suggested order, with
difficulty and harness needs. `BACKLOG.md` stays the unit manifest
(specs, caps, minimums); `DESIGN.md` the frozen contract; the
control-plane project log (`.atelier/projects/coding/crossfoot/log.md`)
holds the per-session narrative. This file is only for deciding *who
does what next* — keep it lean: when a unit ships, drop it from the
Queue and add a one-line entry to *Shipped*, not a full write-up (the
detail already lives in BACKLOG + the project log).

**Rolling rules:** take the topmost session that fits your harness; when
shipped, remove its Queue block and prepend a one-liner to *Shipped*
(newest first). Append newly-visible sessions to the Queue.
Re-sequencing is allowed — note why.

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

**Completed so far — corpus #1–160, all reconcile GREEN under strict
coverage** (per-unit specs in `BACKLOG.md`, session detail in the
control-plane project log):

- **Treasury MTS Table 4 + Table 5, seed units (Apple, Census), BLS 2024
  CPI relative importance** — #1–63, complete (incl. the optional
  Table-5 grand-sum capstone #63).
- **FEC 2024 presidential general** — #64–74, complete (11 units).
- **OMB FY2027 Legislative Branch** — *in progress*: CBO #75; Library of
  Congress family 10/10 (#76–85); US Tax Court family 3/3 (#86–88);
  Capitol Police family 4/4 (#89–92); Office of Congressional Workplace
  Rights #93; GAO 2/2 (#94–95); GPO 4/4 (#96–99); **Boards and
  Commissions COMPLETE** — all 14 accounts + the chapter-closing
  General Fund Receipt Accounts listing, #100–114 (MedPAC, CSCE,
  MACPAC, US-China, USCIRF, CECC, HDP, Senate Preservation Fund,
  Semiquincentennial, COIL, Other Boards, Stennis, Capitol
  Preservation, Open World, GFRA); **Architect of the Capitol
  COMPLETE (15/15)** — Capital Construction and Operations #115,
  Capitol Building #116, Capitol Grounds #117, Senate Office Buildings
  #118, House Office Buildings #119, Capitol Power Plant #120.

Every-10th different-agent spot-audits GREEN through **#139**: #120
(Capitol Power Plant) audited by Antigravity; #129 (Botanic Garden,
transcriber Antigravity) audited by Claude Fable 5 ONE EARLY per
Kenrin's 2026-07-18 call — full-coverage 90/90 value match plus ONE
completeness repair (the printed 1001 memo row was missing; added,
values untouched; see `AUDITS.md`). That audit satisfies the #130
slot. **#139 (Table 7 Receipts Totals, Antigravity) audited ONE EARLY
by Grok** per Kenrin's 2026-07-18 call — full-coverage 54/54 exact
(satisfies the #140 slot); **#150 every-10th audit completed GREEN by Antigravity** (satisfies the #150 slot); **#160 every-10th audit DUE** (Antigravity transcribed #152–160; different-agent rule).
Lesson for transcribers: cross-check row COUNTS against the print — a
missing standalone-class row is invisible to strict coverage. In the OMB
chapter, Senate + House (pp1–4) carry **zero** P&F schedules (pure
appropriations language, out of scope) and pp38–40 are General
Provisions (legal text, out of scope).

### Live dispatch — Treasury MTS May 2026 remainder (PDF → vision, render-anchored)

Table 7 fully complete (#138–145). Table 6 main complete as liabilities + assets-financing + schedules A–E split (#146–160). **Unit-150 every-10th audit completed GREEN** (Antigravity audited Grok's agri unit). **Unit-160 every-10th audit DUE** (different agent than Antigravity).

All Schedule C / D / E units have been shipped.

Also available in already-vendored sources: a sizing survey of the Census **P60-282** report cross-tabs remains a parallel queue-refresh option.

- **GAO complete (2/2, #94–95).** Cross-schedule sanity verified at
  ship time: `0900`≡`99.9`, `0799`≡`99.0 Direct`, `0899`≡`99.0
  Reimbursable`. **GPO complete (4/4, #96–99):** the survey's "3
  accounts" became 4 units — Business Operations Revolving Fund
  (004-4505) measured 152 cells, over-cap, split by schedule per the
  GAO precedent. **Boards and Commissions complete (15 units,
  #100–114, all 2026-07-18):** the family's recurring wrinkles, now
  fully catalogued for future chapters — tiny accounts drop 0900/1900
  (sometimes 1000/3050/4020) rows entirely; columns that net to zero
  are zero-suppressed (blank != zero, and a fully-zero row vanishes);
  printed `99.5 Adjustment for rounding` lines sum EXACTLY (never a
  tolerance); trust funds carry 5000/5001 investment memos and
  combined same-id receipts schedules; duplicate printed row codes
  (Stennis's two 1140s) become distinct rows.

- **FEC footnote pages pp7-9** stay a Tier-3 stage concern (DESIGN §8) —
  not yet in scope.

---

## Shipped

One line per shipped unit/batch, newest first. Full specs in
`BACKLOG.md`; session narrative in the control-plane project log.

- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-e-direct-part2` — #160 (Antigravity). Schedule E Direct Loans Part 2; 175c/23r. **Every-10th audit DUE** (different agent).
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-e-direct-part1` — #159 (Antigravity). Schedule E Direct Loans Part 1; 136c/18r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-e-guaranteed` — #158 (Antigravity). Schedule E Guaranteed Loans; 181c/17r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-d-trust-funds` — #157 (Antigravity). Schedule D Trust Funds; 224c/30r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-d-federal-funds-labor-totals` — #156 (Antigravity). Schedule D Federal Funds Labor-Totals; 116c/18r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-d-federal-funds-agri-just` — #155 (Antigravity). Schedule D Federal Funds Agriculture-Justice; 48c/6r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-c-epa-ind` — #154 (Antigravity). Schedule C EPA-Independent; 73c/8r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-c-treas-vets` — #153 (Antigravity). Schedule C Treasury-Veterans; 35c/1r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-c-hhs-trans` — #152 (Antigravity). Schedule C HHS-Transportation; 68c/3r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-c-comm-energy` — #151 (Grok). Schedule C Commerce–Energy; 62c/5r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-c-agri` — #150 (Grok). Schedule C Agriculture; 93c/10r. **Every-10th audit DUE** (different agent).
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-b` — #149 (Grok). Agency securities under special financing; 15c/5r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-a` — #148 (Grok). Analysis of change in excess of liabilities; 31c/10r.
- 2026-07-18 · `treasury-mts/2026-05-table6-assets-financing` — #147 (Grok). Table 6 assets + Excess + Financing; Total Liability re-anchored; 125c/50r.
- 2026-07-18 · `treasury-mts/2026-05-table6-liabilities` — #146 (Grok). Table 6 liability accounts; 102c/41r. Cap-fit split of over-cap single Table 6.
- 2026-07-18 · `treasury-mts/2026-05-table7-outlays-uor-totals` — #145 (Grok). UOR + monthly totals this/prior year; 157c/46r. Cap-fit split of ssa-totals.
- 2026-07-18 · `treasury-mts/2026-05-table7-outlays-ssa-independents` — #144 (Grok). SSA + Independent Agencies; 87c/8r.
- 2026-07-18 · `treasury-mts/2026-05-table7-outlays-intl-sba` — #143 (Grok). International Assistance through SBA; 80c/8r.
- 2026-07-18 · `treasury-mts/2026-05-table7-outlays-state-gsa` — #142 (Grok). State through GSA (incl. VA on p35); 130c/13r.
- 2026-07-18 · `treasury-mts/2026-05-table7-outlays-edu-labor` — #141 (Grok). Education through Labor; 150c/15r.
- 2026-07-18 · `treasury-mts/2026-05-table7-outlays-leg-def` — #140 (Grok). Outlays Legislative through Total DoD Military; 150c/25r/6 standalone (Prior-FY on non-DoD lines). DoD bureau roll-ups + per-row Oct–May→YTD.
- 2026-07-18 · `treasury-mts/2026-05-table7-receipts-totals` — #139 audit: **GREEN** (Grok, one early per Kenrin; 54/54 values exact; `AUDITS.md`). Next audit #150.
- 2026-07-18 · `treasury-mts/2026-05-table7-receipts-totals` — #139 (Antigravity). Receipts Totals/Budget splits; 54c/18r/0 standalone.
- 2026-07-18 · `treasury-mts/2026-05-table7-receipts-detail` — #138 (Antigravity). Receipts Detail rows; 90c/0r/90 standalone.
- 2026-07-18 · `treasury-mts/2026-05-table8-investments` — #137 (Antigravity). Securities Held investments; 45c/3r/0 standalone.
- 2026-07-18 · `treasury-mts/2026-05-table8-activity` — #136 (Antigravity). Receipts/Outlays/Excess activity; 132c/60r/0 standalone.
- 2026-07-18 · `treasury-mts/2026-05-table9` — #135 (Antigravity). Summary of receipts by source, outlays by function; 90c/6r/0 standalone.
- 2026-07-18 · `treasury-mts/2026-05-table3-outlays-remainder` — #134 (Antigravity). Outlays Section remainder, totals, and deficits; 50c/20r/0 standalone.
- 2026-07-18 · `treasury-mts/2026-05-table3-outlays-departments` — #133 (Antigravity). Outlays Section: Legislative through OPM/SBA; 112c/0r/112 standalone.
- 2026-07-18 · `treasury-mts/2026-05-table3-receipts` — #132 (Antigravity). Summary of Receipts; 52c/12r/0 standalone.
- 2026-07-18 · `treasury-mts/2026-05-table2` — #131 (Antigravity). Budget/off-budget results and financing; 50c/28r/0 standalone.
- 2026-07-18 · `treasury-mts/2026-05-table1` — #130 (Antigravity). Summary of monthly receipts, outlays, deficit; 66c/28r/0 standalone.
- 2026-07-18 · `omb/…-aoc-botanic-garden` — #129 (Antigravity). Receives transfer from Capitol Grounds; 90c/17r/28 standalone.
- 2026-07-18 · `omb/…-aoc-judiciary-office-building` — #128 (Antigravity). Revolving fund; 91c/15r/34 standalone.
- 2026-07-18 · `omb/…-aoc-recyclable-materials-revolving` — #127 (Antigravity). Degenerate 3-row revolving fund; 9c/0r/9 standalone.
- 2026-07-18 · `omb/…-aoc-capitol-visitor-center-revolving` — #126 (Antigravity). CVC Revolving fund; 66c/12r/30 standalone.
- 2026-07-18 · `omb/…-aoc-capitol-visitor-center` — #125 (Antigravity). Receives transfer from Capitol Grounds; 78c/13r/28 standalone.
- 2026-07-18 · `omb/…-aoc-capitol-police-buildings` — #124 (Antigravity). Main security account; 107c/19r/33 standalone.
- 2026-07-18 · `omb/…-aoc-library-buildings-grounds` — #123 (Antigravity). Library of Congress buildings; 122c/30r/26 standalone.
- 2026-07-18 · `omb/…-aoc-house-office-buildings-fund` — #122 (Antigravity). Degenerate 4-cell HOB fund; 4c/0r/4 standalone.
- 2026-07-18 · `omb/…-aoc-house-historic-buildings` — #121 (Antigravity). Trust fund, receives HOB transfers; 51c/8r/26 standalone.
- 2026-07-18 · `omb/…-aoc-botanic-garden` — #129 audit: **GREEN after completeness repair** (Claude Fable 5, one early per Kenrin; 90/90 values exact, missing 1001 memo row added → 91 cells; `AUDITS.md`). Next audit #140.
- 2026-07-18 · `omb/…-aoc-capitol-power-plant` — #120 (Claude Fable 5). Richest AoC topology (reimbursable 0900, all-cols 1900/4040, dual 99.0); 123c/33r/21 standalone. **Every-10th audit GREEN** (Antigravity; `AUDITS.md`).
- 2026-07-18 · `omb/…-aoc-house-office-buildings` — #119 (Claude Fable 5). Transfer topology (1010/1120 out to 001-1833, 1121 in from 000-0400); 116c/22r/34 standalone.
- 2026-07-18 · `omb/…-aoc-senate-office-buildings` — #118 (Claude Fable 5). SPF transfer twin (1011 +4 c2); 116c/19r/32 standalone.
- 2026-07-18 · `omb/…-aoc-capitol-grounds` — #117 (Claude Fable 5). Two 1120 transfer rows (SPF-twin pattern); 90c/16r/26 standalone.
- 2026-07-18 · `omb/…-aoc-capitol-building` — #116 (Claude Fable 5). Incl. Flag Office Revolving fund; 6-source 3050 c1; 103c/18r/33 standalone.
- 2026-07-18 · `omb/…-aoc-capital-construction-ops` — #115 (Claude Fable 5). **AoC started (3/13).** Department starter; 101c/19r/30 standalone.
- 2026-07-18 · `omb/…-general-fund-receipts` — #114 (Claude Fable 5). Chapter-closing 2-cell receipts listing. **Boards and Commissions COMPLETE (15 units, #100–114); Legislative Branch chapter fully transcribed outside AoC (pp8–16) and the out-of-scope language pages.**
- 2026-07-18 · `omb/…-open-world-trust-fund` — #113 (Claude Fable 5). Trust fund + same-id receipts schedule; 92c/14r/44 standalone.
- 2026-07-18 · `omb/…-capitol-preservation-commission` — #112 (Claude Fable 5). Dormant trust fund; 22c/1r/19 standalone.
- 2026-07-18 · `omb/…-stennis-center` — #111 (Claude Fable 5). Trust fund, duplicate printed 1140 codes; 73c/12r/40 standalone.
- 2026-07-18 · `omb/…-other-boards-commissions` — #110 (Claude Fable 5). Zero-relation consolidated account; 15c/0r/15 standalone. **Every-10th audit GREEN** (Kimi, full 15/15 coverage; `AUDITS.md`).
- 2026-07-18 · `omb/…-coil-fund` — #109 (Claude Fable 5). Payment account, 3050 row absent; 44c/3r/35 standalone.
- 2026-07-18 · `omb/…-semiquincentennial-commission` — #108 (Claude Fable 5). Close-out commission, 4-source 3050 c1; 71c/12r/29 standalone.
- 2026-07-18 · `omb/…-senate-preservation-fund` — #107 (Claude Fable 5). Gift trust fund, no obligations section, negative 1010 transfer; 27c/2r/21 standalone.
- 2026-07-18 · `omb/…-house-democracy-partnership` — #106 (Claude Fable 5). New commission, entire 2025 column blank; 24c/2r/18 standalone.
- 2026-07-18 · `omb/…-cecc-salaries-expenses` — #105 (Claude Fable 5). 3050 row absent (nets zero); 43c/4r/31 standalone.
- 2026-07-18 · `omb/…-uscirf-salaries-expenses` — #104 (Claude Fable 5). Within-page column-flow P&F (starts bottom-left, continues top-right of p33); 65c/13r/27 standalone.
- 2026-07-18 · `omb/…-uscc-salaries-expenses` — #103 (Claude Fable 5). 99.5 rounding line all 3 cols, 99.9=99.0+99.5 exact each; 64c/14r/23 standalone.
- 2026-07-18 · `omb/…-macpac-salaries-expenses` — #102 (Claude Fable 5). No 0900/1000 rows; 3050 zero-suppressed c2/c3; 60c/7r/36 standalone.
- 2026-07-18 · `omb/…-csce-salaries-expenses` — #101 (Claude Fable 5). P&F spans p30 bottom-right → p31 top-left; 55c/9r/28 standalone.
- 2026-07-18 · `omb/…-medpac-salaries-expenses` — #100 (Claude Fable 5). First Boards and Commissions account; 79c/14r/30 standalone; no 0900 row, zero-suppressed nets. **Every-10th audit GREEN** (Grok, full 79/79 multiset + 10 high-risk sample; `AUDITS.md`).
- 2026-07-18 · `omb/…-gpo-business-operations-objclass` — #99 (Claude Fable 5). 45c/6r/6 standalone. **GPO complete, 4/4 (#96–99); account 004-4505 fully transcribed (152 cells).**
- 2026-07-18 · `omb/…-gpo-business-operations-pf` — #98 (Claude Fable 5). Revolving fund P&F, mandatory offsetting collections; 107c/38r/19 standalone; 4160 zero-suppressed all cols.
- 2026-07-18 · `omb/…-gpo-public-information` — #97 (Claude Fable 5). P&F + ObjClass + Employment; 75c/12r/24 standalone.
- 2026-07-18 · `omb/…-gpo-congressional-publishing` — #96 (Claude Fable 5). Sole-activity P&F-only account; 49c/6r/27 standalone.
- 2026-07-18 · `omb/…-gao-salaries-objclass` — #95 (Claude Fable 5). ObjClass + Employment; 66c/9r/6 standalone. **GAO complete, 2/2 (#94–95); account 005-0107 fully transcribed (195 cells).**
- 2026-07-18 · `omb/…-gao-salaries-pf` — #94 (Claude Fable 5). P&F with offsetting collections + uncollected payments; 129c/39r/16 standalone; spans p28 right col → p29 left col.
- 2026-07-18 · `omb/…-ocwr-salaries-expenses` — #93 (Codex). 27c/0r/27 standalone; every equality is single-source under `minItems: 2`.
- 2026-07-18 · `omb/…-capitol-police-mutual-aid` — #92 (Codex). 43c/5r/26 standalone. **Capitol Police family complete, 4/4 (#89–92).**
- 2026-07-18 · `omb/…-capitol-police-security-enhancements` — #91 (Codex). 9c/0r/9 standalone; degenerate one-source schedule.
- 2026-07-18 · `omb/…-capitol-police-general-expenses` — #90 (Claude Opus 4.8). Offsetting collections + uncollected payments; 106c/25r/32 standalone. **Every-10th audit GREEN** (Codex, `AUDITS.md`).
- 2026-07-18 · `omb/…-capitol-police-salaries` — #89 (Claude Opus 4.8). Clean discretionary account; 66c/12r/26 standalone.
- 2026-07-18 · `omb/…-tax-court-survivors-annuity` — #88 (Claude Opus 4.8). Trust Fund combined receipts+P&F; 73c/12r/45 standalone. **US Tax Court family complete, 3/3 (#86–88).**
- 2026-07-18 · `omb/…-tax-court-fees` — #87 (Claude Opus 4.7). Combined receipts+P&F; 30c/3r/24 standalone.
- 2026-07-18 · `omb/…-tax-court-salaries` — #86 (Claude Opus 4.6). Main account; 98c/16r/27 standalone.
- 2026-07-18 · `omb/…-loc-{crs,cooperative-acquisitions,gift-shop,fedlink,gift-trust}` — #81–85 (Claude Sonnet 5). **LoC family complete, 10/10 (#76–85).** Same session fixed a pre-existing coverage bug in #76 (rows 1940/1941 mislabeled `leaf`→`standalone`, commit `82f81f2`).
- 2026-07-18 · `omb/…-loc-{salaries,stewardship,copyright,blind,payments-copyright}` — #76–80 (Antigravity). 488c/100r. **Unit-80 audit GREEN** (Claude Fable 5, `AUDITS.md`).
- 2026-07-18 · `omb/…-cbo` — #75 (Antigravity). OMB family starter; 92c/14r.
- 2026-07-17 · `fec/…-popular-capstone-a…d` — #71–74 (Kimi). Cross-page per-state TOTAL VOTES re-anchor; 501/501 0-mismatch. **FEC family complete (11 units, #64–74).**
- 2026-07-17 · `fec/…-popular-block-1…5` (incl. the #67/68 ceiling split) — #65–70 (Kimi). Popular vote pp2–6; national TOTAL VOTES 155,238,302. **Unit-70 audit GREEN** (Antigravity, `AUDITS.md`).
- 2026-07-17 · `fec/…-electoral` — #64 (Kimi). FEC proof unit (p1 electoral votes, 538/312/226).
- **#1–63** (Treasury MTS Table 4 receipts + Table 5 outlays, seed units, BLS 2024 CPI relative importance) — shipped GREEN across 2026-07-13…16 by the fleet; **families complete**, per-unit specs in `BACKLOG.md`. Landmarks: Table-4 major slice #1; strict-coverage-default harness flip; BLS relative-importance hierarchy; Table-5 flagship #14 (legislative); first Tier-C over-cap split #33–34 (education); Table-5 grand-sum capstone #63.
