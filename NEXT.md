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
- ⚠ **Recurring venv breaker:** if EVERY `uv run` fails with `failed to
  remove .venv/lib64: Access is denied (os error 5)`, a POSIX-side
  session has left a stray `lib64 -> lib` symlink in `.venv`. Fix:
  `rm .venv/lib64` — uv then rebuilds cleanly. Happened twice on
  2026-07-18; a full-corpus sweep run through a broken uv reports
  every unit RED, so fix the venv BEFORE believing a red sweep.
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

**Completed so far — corpus #1–200, all reconcile GREEN under strict
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
- **Census P60-282 Table A-2 continuation COMPLETE** — #161–200: ALL RACES
  completed through 1967, modern WHITE ALONE completed through 2002,
  historical WHITE completed through 1967, both WHITE NOT HISPANIC
  groups completed, both modern BLACK groups completed, and historical
  BLACK completed through 1967; both modern ASIAN groups and the
  historical ASIAN AND PACIFIC ISLANDER group completed; AMERICAN
  INDIAN AND ALASKA NATIVE ALONE OR IN COMBINATION completed; and
  AMERICAN INDIAN AND ALASKA NATIVE ALONE and its historical predecessor
  completed; TWO OR MORE RACES completed; and HISPANIC (ANY RACE) completed
  through 1972. Together with the legacy-named seed unit #3, all 41 A-2
  source-native units are shipped.

Every-10th different-agent spot-audits GREEN through **#250**: #120
(Capitol Power Plant) audited by Antigravity; #129 (Botanic Garden,
transcriber Antigravity) audited by Claude Fable 5 ONE EARLY per
Kenrin's 2026-07-18 call — full-coverage 90/90 value match plus ONE
completeness repair (the printed 1001 memo row was missing; added,
values untouched; see `AUDITS.md`). That audit satisfies the #130
slot. **#139 (Table 7 Receipts Totals, Antigravity) audited ONE EARLY
by Grok** per Kenrin's 2026-07-18 call — full-coverage 54/54 exact
(satisfies the #140 slot); **#150 every-10th audit completed GREEN by Antigravity** (satisfies the #150 slot); **#160 every-10th audit completed GREEN after completeness repair by Grok** (Antigravity transcribed #152–160; different-agent rule; two missing standalone rows repaired — see `AUDITS.md`). Corpus **#170 is audited and GREEN by Antigravity**. Corpus **#180 is audited and GREEN by Antigravity**; #181 is unblocked. Corpus **#190 is audited and GREEN by Antigravity**; #191 is unblocked. Corpus **#200 is audited and GREEN by Claude Fable 5** (render-anchored full-value audit, 44/44 exact; closes Table A-2). Corpus **#210 is audited and GREEN by Grok** (full-coverage 111/111 exact vs p51; different-agent rule; `AUDITS.md`). Corpus **#220 is audited and GREEN by Antigravity**; #221+ is unblocked. Corpus **#230 is audited and GREEN by Antigravity**; #231+ is unblocked. Corpus **#240 is audited and GREEN by Antigravity**; #241+ is unblocked. Corpus **#250 is audited and GREEN by Antigravity**. Corpus **#260 audit is DUE** (transcriber Grok; June MTS EOP; placeholder in `AUDITS.md`); #261+ blocked.
Lesson for transcribers: cross-check row COUNTS against the print — a
missing standalone-class row is invisible to strict coverage. In the OMB
chapter, Senate + House (pp1–4) carry **zero** P&F schedules (pure
appropriations language, out of scope) and pp38–40 are General
Provisions (legal text, out of scope).

### Live dispatch — Census P60-282 remainder (QUEUE REFRESH 2026-07-18)

**Treasury MTS May 2026: SOURCE COMPLETE.** Tables 1-9 all transcribed
(Table 7 #138-145; Table 6 #146-160 as liabilities + assets-financing +
Schedules A-E). Unit-150 audit GREEN (Antigravity); unit-160 audit
GREEN after completeness repair (Grok; 175/175 present values exact, 2
missing standalone rows inserted). **Verification 2026-07-18 (Claude
Fable 5): full-corpus sweep re-run on a repaired venv — 160/160 GREEN,
pytest 10/10, audit trail #120-#160 rotation-clean.** Corpus **#170 is
audited and GREEN by Antigravity** (unblocking #171).

- **NEXT DISPATCH — Census P60-282 Table A-2 continuation (zero new
  vendoring, D2).** The 59-page vendored PDF is sha256-ledgered. Its
  appendix has **13 tables**, not the former ~11 estimate: A-1 (PDF
  p21), A-2 (pp22-35; footnotes p36), A-3 (p37), **A-4a (pp38-39),
  A-4b (pp40-41)**, A-5 (pp42-44), A-6 (pp45-46), A-7 (pp47-48),
  and B-1..B-5 (pp51-55). Exact map and split policy:
  `plans/census-p60-282-remainder.md`.

  **Legacy-id correction:** shipped unit #3 is named
  `census-p60/2023-income-a1`, but its embedded metadata and source
  page correctly identify **Table A-2, ALL RACES, 2023-2017**. Keep
  the historical id/file; do not duplicate those eight rows.

  **A-2 sizing and completion:** 459 source rows × 11 arithmetic-bearing
  fields = 5,049 source fields across 41 source-native cap-fit units. All 41
  units are now shipped (the legacy-named seed plus #161–200), encoding
  5,048 numeric cells; one historical household count prints `N` and is
  documented but omitted under the numeric-only schema. Each row carries household count
  (standalone), printed total 100, nine bracket percentages, one sum,
  and one percent-closure relation. Maximum 13 rows / 143 cells per
  unit; median/mean columns stay outside this deliberately scoped
  distribution block.

  **TABLE A-2 COMPLETE AND AUDITED:** #191–200 shipped with independent
  pypdf comparison (1,144/1,144 cells exact), strict reconcile, and the
  full corpus gate. The #200 different-agent audit is **GREEN** (Claude
  Fable 5, 2026-07-18, render-anchored full-value; `AUDITS.md`) —
  `plans/census-p60-282-remainder.md` is complete.

  **APPENDIX SUMMARY/DISTRIBUTION FAMILY (started 2026-07-18, Claude
  Fable 5):** #201–210 shipped — A-3 (2 units, quintile-share
  percent-closures), B-3 (2), B-4 (2), A-1 (3: 2022 / 2023 Number-column
  roll-ups + all-standalone percent-change block), and the B-1 2022
  block. Portrait pages have a NORMAL text layer (the reversed-token
  quirk is specific to the rotated A-2/A-4 landscape pages). Convention
  settled this batch: printed `*` significance markers are apparatus and
  are stripped; Number-column roll-ups carry exact observed deltas as
  tolerances with the footnote-2 rounded-components rationale; medians,
  MOEs, ratios, Gini, percentiles, percent-change, and overlapping race
  counts are standalone with whys.

  **BATCH #211–220 SHIPPED (Grok, 2026-07-19):** B-1/B-2/B-5 complete; A-7
  started. **#220 audit GREEN** (Antigravity).

  **BATCH #221–230 SHIPPED (Grok, 2026-07-19):** A-7 full-MOE era complete
  (#221–222, 51 rows total across five bands); Table A-6 complete (#223–230:
  people + full-time × {2022, 2023, pct-workers, pct-median}; Sex/age/education
  Number roll-ups; Z→0; female-to-male ratio on FT pct-median only). Full sweep
  230/230 GREEN; pytest 10/10.

  **BATCH #231–240 SHIPPED (Grok, 2026-07-19):** A-7 complete through 1960
  (#231–232, N-omission sparse cells); Table A-4a complete (#233–238, 59 rows);
  Table A-4b started (#239–240, means/shares/indices with percent-closures).
  Sweep 240/240 GREEN; pytest 10/10.

  **BATCH #241–250 SHIPPED (Grok, 2026-07-19):** Table A-4b complete (#241–244,
  59 rows); Table A-5 complete (#245–250, 59 year-rows transposed from landscape
  measure×year layout). Sweep 250/250 GREEN; pytest 10/10.

  **BATCH #251–260 SHIPPED (Grok, 2026-07-19):** Vendored Treasury MTS June 2026
  (`mts-202606.pdf`, content-gated 39pp) and shipped 10 starter units (Tables 1–3,
  9, major receipts, Legislative/Judicial/EOP Table 5). Sweep 260/260 GREEN.

  **AUDIT GATE:** unit **#260** (`treasury-mts/2026-06-outlays-eop`) requires a
  different-agent audit (placeholder in `AUDITS.md`; transcriber Grok).
  **#261+ is blocked until GREEN.** After GREEN: continue June Table 5 sections
  with May conventions, then Table 6–8 / means-of-financing.


- **D1/web vendoring options (browser-capable agents; content-gate per
  DESIGN §7 — magic-byte check, soft-404 caution):**
  1. **Treasury MTS June 2026** — fiscaldata static path (same pattern
     as `mts-202605.pdf`); a whole new month-family with every
     extraction convention already settled. Highest-leverage vendor.
  2. **A second 10-K** (e.g., Microsoft FY2025) via EDGAR
     FilingSummary.xml (SEC requires a contact UA) — balance sheet
     first per the Apple #2 seed pattern.

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

- 2026-07-19 · `treasury-mts/2026-06-outlays-eop` — #260 (Grok). Table 5 EOP; strict-default GREEN. **June MTS family started. Different-agent audit DUE; #261+ blocked.**
- 2026-07-19 · `treasury-mts/2026-06-outlays-legislative` — #259 (Grok). Table 5 Legislative Branch; strict-default GREEN.
- 2026-07-19 · `treasury-mts/2026-06-outlays-judicial` — #258 (Grok). Table 5 Judicial Branch; strict-default GREEN.
- 2026-07-19 · `treasury-mts/2026-06-receipts-major` — #257 (Grok). Major net receipts; strict-default GREEN.
- 2026-07-19 · `treasury-mts/2026-06-table9` — #256 (Grok). Table 9 source/function summary; strict-default GREEN.
- 2026-07-19 · `treasury-mts/2026-06-table3-outlays-remainder` — #255 (Grok). Table 3 remainder totals; strict-default GREEN.
- 2026-07-19 · `treasury-mts/2026-06-table3-outlays-departments` — #254 (Grok). Table 3 department lines (standalone); strict-default GREEN.
- 2026-07-19 · `treasury-mts/2026-06-table3-receipts` — #253 (Grok). Table 3 receipts block; strict-default GREEN.
- 2026-07-19 · `treasury-mts/2026-06-table2` — #252 (Grok). Table 2 financing summary; strict-default GREEN.
- 2026-07-19 · `treasury-mts/2026-06-table1` — #251 (Grok). Table 1 monthly through June; strict-default GREEN. **Vendored mts-202606.pdf.**
- 2026-07-19 · `census-p60/2023-income-a5-1975-1967` — #250 (Grok). 126c/9r; strict-default GREEN. **Table A-5 complete. Different-agent audit GREEN (Antigravity); #251+ unblocked.**
- 2026-07-19 · `census-p60/2023-income-a5-1985-1976` — #249 (Grok). 140c/10r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a5-1995-1986` — #248 (Grok). 140c/10r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a5-2005-1996` — #247 (Grok). 140c/10r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a5-2014-2006` — #246 (Grok). 140c/10r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a5-2023-2015` — #245 (Grok). 140c/10r; landscape-transposed. **Table A-5 started.**
- 2026-07-19 · `census-p60/2023-income-a4b-1975-1967` — #244 (Grok). 162c/9r; strict-default GREEN. **Table A-4b complete (59 rows).**
- 2026-07-19 · `census-p60/2023-income-a4b-1985-1976` — #243 (Grok). 180c/10r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a4b-1995-1986` — #242 (Grok). 180c/10r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a4b-2005-1996` — #241 (Grok). 180c/10r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a4b-2014-2006` — #240 (Grok). 180c/10r percent-closures; strict-default GREEN. **Different-agent audit GREEN (Antigravity); #241+ unblocked.**
- 2026-07-19 · `census-p60/2023-income-a4b-2023-2015` — #239 (Grok). 180c/10r; strict-default GREEN. **Table A-4b started.**
- 2026-07-19 · `census-p60/2023-income-a4a-1975-1967` — #238 (Grok). 117c/0r; strict-default GREEN. **Table A-4a complete (59 rows).**
- 2026-07-19 · `census-p60/2023-income-a4a-1985-1976` — #237 (Grok). 130c/0r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a4a-1995-1986` — #236 (Grok). 130c/0r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a4a-2005-1996` — #235 (Grok). 130c/0r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a4a-2014-2006` — #234 (Grok). 130c/0r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a4a-2023-2015` — #233 (Grok). 130c/0r; pypdf multiset exact. **Table A-4a started.**
- 2026-07-19 · `census-p60/2023-income-a7-1966-1960` — #232 (Grok). 35c/0r (N counts/MOEs omitted). **Table A-7 complete.**
- 2026-07-19 · `census-p60/2023-income-a7-1974-1967` — #231 (Grok). 74c/0r (N MOEs omitted); strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a6-ft-pct-median` — #230 (Grok). 42c/0r (incl. ratio row); strict-default GREEN. **Table A-6 complete. Different-agent audit GREEN (Antigravity); #231+ unblocked.**
- 2026-07-19 · `census-p60/2023-income-a6-ft-pct-workers` — #229 (Grok). 40c/0r; Z→0 on Total; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a6-ft-2023` — #228 (Grok). 60c/4r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a6-ft-2022` — #227 (Grok). 60c/4r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a6-people-pct-median` — #226 (Grok). 40c/0r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a6-people-pct-workers` — #225 (Grok). 40c/0r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a6-people-2023` — #224 (Grok). 60c/4r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-a6-people-2022` — #223 (Grok). 60c/4r; Sex/age/educ Number roll-ups; strict-default GREEN. **Table A-6 started.**
- 2026-07-19 · `census-p60/2023-income-a7-1984-1975` — #222 (Grok). 130c/0r; strict-default GREEN; pypdf ordered exact. **A-7 full-MOE era complete (51 rows).**
- 2026-07-19 · `census-p60/2023-income-a7-1995-1985` — #221 (Grok). 143c/0r; strict-default GREEN; pypdf ordered exact.
- 2026-07-19 · `census-p60/2023-income-a7-2005-1996` — #220 (Grok). 130c/0r/130 standalone; strict-default GREEN; pypdf ordered 130/130. **Different-agent audit GREEN (Antigravity); #221+ unblocked.**
- 2026-07-19 · `census-p60/2023-income-a7-2014-2006` — #219 (Grok). 130c/0r; dual 2013 redesigned/legacy; strict-default GREEN; pypdf ordered exact.
- 2026-07-19 · `census-p60/2023-income-a7-2023-2015` — #218 (Grok). 130c/0r; dual 2017 series; strict-default GREEN; pypdf ordered exact. **Table A-7 started.**
- 2026-07-19 · `census-p60/2023-income-b5-2014-2009` — #217 (Grok). 91c/0r; dual 2013; strict-default GREEN; pypdf multiset exact. **Table B-5 complete.**
- 2026-07-19 · `census-p60/2023-income-b5-2023-2015` — #216 (Grok). 130c/0r; strict-default GREEN; pypdf multiset exact.
- 2026-07-19 · `census-p60/2023-income-b2-percent-difference` — #215 (Grok). 74c/0r; strict-default GREEN. **Table B-2 complete.**
- 2026-07-19 · `census-p60/2023-income-b2-post-tax` — #214 (Grok). 111c/11r; matches B-1 2023 values; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-b2-money-income` — #213 (Grok). 111c/11r; strict-default GREEN.
- 2026-07-19 · `census-p60/2023-income-b1-percent-change` — #212 (Grok). 74c/0r; strict-default GREEN. **Table B-1 complete.**
- 2026-07-19 · `census-p60/2023-income-b1-2023` — #211 (Grok). 111c/11r; strict-default GREEN; pypdf 111/111 exact.
- 2026-07-18 · `census-p60/2023-income-b1-2022` — #210 (Claude Fable 5). 111c/11r/79 standalone; strict-default GREEN; independent pypdf source comparison 111/111 exact. **Every-10th audit GREEN** (Grok, 2026-07-19, full-coverage 111/111; `AUDITS.md`); #211+ unblocked.
- 2026-07-18 · `census-p60/2023-income-a1-percent-change` — #209 (Claude Fable 5). 74c/0r/74 standalone (derived ratios, outside relation vocabulary); strict-default GREEN; independent pypdf source comparison 74/74 exact. **Table A-1 complete.**
- 2026-07-18 · `census-p60/2023-income-a1-2023` — #208 (Claude Fable 5). 111c/11r/79 standalone; 2 roll-ups exact, 9 at source-authorized rounding tol; strict-default GREEN; independent pypdf source comparison 111/111 exact.
- 2026-07-18 · `census-p60/2023-income-a1-2022` — #207 (Claude Fable 5). 111c/11r/79 standalone; 1 roll-up exact, 10 at source-authorized rounding tol; strict-default GREEN; independent pypdf source comparison 111/111 exact.
- 2026-07-18 · `census-p60/2023-income-b4-equivalence-adjusted-income` — #206 (Claude Fable 5). 78c/2r/66 standalone; both closures exact; strict-default GREEN; independent pypdf source comparison 78/78 exact. **Table B-4 complete.**
- 2026-07-18 · `census-p60/2023-income-b4-income` — #205 (Claude Fable 5). 78c/2r/66 standalone; money closure exact, post-tax tol 0.1; strict-default GREEN; independent pypdf source comparison 78/78 exact.
- 2026-07-18 · `census-p60/2023-income-b3-equivalence-adjusted-post-tax` — #204 (Claude Fable 5). 78c/2r/66 standalone; both closures exact; strict-default GREEN; independent pypdf source comparison 78/78 exact. **Table B-3 complete.**
- 2026-07-18 · `census-p60/2023-income-b3-post-tax` — #203 (Claude Fable 5). 78c/2r/66 standalone; both closures at source-authorized tol 0.1; strict-default GREEN; independent pypdf source comparison 78/78 exact.
- 2026-07-18 · `census-p60/2023-income-a3-equivalence-adjusted` — #202 (Claude Fable 5). 78c/2r/66 standalone; both closures exact; strict-default GREEN; independent pypdf source comparison 78/78 exact. **Table A-3 complete.**
- 2026-07-18 · `census-p60/2023-income-a3-money-income` — #201 (Claude Fable 5). 78c/2r/66 standalone; 2022 closure at source-authorized tol 0.2, 2023 exact; strict-default GREEN; independent pypdf source comparison 78/78 exact. **First percent-closure-led family unit.**
- 2026-07-18 · `census-p60/2023-income-a2-hispanic-any-race-1975-1972` — #200 (Codex). 44c/8r/4 standalone; strict-default GREEN; independent pypdf source comparison 44/44 exact; HISPANIC (ANY RACE) and Table A-2 complete. **Every-10th audit GREEN** (Claude Fable 5, render-anchored 44/44; `AUDITS.md`); new-family work unblocked.
- 2026-07-18 · `census-p60/2023-income-a2-hispanic-any-race-1988-1976` — #199 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-hispanic-any-race-2001-1989` — #198 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-hispanic-any-race-2012-2002` — #197 (Codex). 121c/22r/11 standalone; strict-default GREEN; independent pypdf source comparison 121/121 exact.
- 2026-07-18 · `census-p60/2023-income-a2-hispanic-any-race-2023-2013` — #196 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-two-or-more-races-2012-2002` — #195 (Codex). 121c/22r/11 standalone; strict-default GREEN; independent pypdf source comparison 121/121 exact; group complete.
- 2026-07-18 · `census-p60/2023-income-a2-two-or-more-races-2023-2013` — #194 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-american-indian-alaska-native-historical-1988-1987` — #193 (Codex). 22c/4r/2 standalone; strict-default GREEN; independent pypdf source comparison 22/22 exact; historical group complete.
- 2026-07-18 · `census-p60/2023-income-a2-american-indian-alaska-native-historical-2001-1989` — #192 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-american-indian-alaska-native-alone-2012-2002` — #191 (Codex). 121c/22r/11 standalone; strict-default GREEN; independent pypdf source comparison 121/121 exact; modern group complete.
- 2026-07-18 · `census-p60/2023-income-a2-american-indian-alaska-native-alone-2023-2013` — #190 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact. **Different-agent audit GREEN (Antigravity); #191 unblocked.**
- 2026-07-18 · `census-p60/2023-income-a2-american-indian-alaska-native-alone-or-in-combination-2012-2002` — #189 (Codex). 121c/22r/11 standalone; strict-default GREEN; independent pypdf source comparison 121/121 exact; group complete.
- 2026-07-18 · `census-p60/2023-income-a2-american-indian-alaska-native-alone-or-in-combination-2023-2013` — #188 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-asian-pacific-islander-historical-1988-1987` — #187 (Codex). 21 numeric cells/4r/1 standalone; strict-default GREEN; independent pypdf comparison 21/21 numeric cells exact; printed 1987 count `N` documented and omitted; historical group complete.
- 2026-07-18 · `census-p60/2023-income-a2-asian-pacific-islander-historical-2001-1989` — #186 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-asian-alone-2012-2002` — #185 (Codex). 121c/22r/11 standalone; strict-default GREEN; independent pypdf source comparison 121/121 exact; modern ASIAN ALONE complete.
- 2026-07-18 · `census-p60/2023-income-a2-asian-alone-2023-2013` — #184 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-asian-alone-or-in-combination-2012-2002` — #183 (Codex). 121c/22r/11 standalone; strict-default GREEN; independent pypdf source comparison 121/121 exact; group complete.
- 2026-07-18 · `census-p60/2023-income-a2-asian-alone-or-in-combination-2023-2013` — #182 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-black-historical-1975-1967` — #181 (Codex). 99c/18r/9 standalone; strict-default GREEN; independent pypdf source comparison 99/99 exact; historical BLACK complete.
- 2026-07-18 · `census-p60/2023-income-a2-black-historical-1988-1976` — #180 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact. **Different-agent audit GREEN (Antigravity); #181 unblocked.**
- 2026-07-18 · `census-p60/2023-income-a2-black-historical-2001-1989` — #179 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-black-alone-2012-2002` — #178 (Codex). 121c/22r/11 standalone; strict-default GREEN; independent pypdf source comparison 121/121 exact; modern BLACK ALONE complete.
- 2026-07-18 · `census-p60/2023-income-a2-black-alone-2023-2013` — #177 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-black-alone-or-in-combination-2012-2002` — #176 (Codex). 121c/22r/11 standalone; strict-default GREEN; independent pypdf source comparison 121/121 exact; group complete.
- 2026-07-18 · `census-p60/2023-income-a2-black-alone-or-in-combination-2023-2013` — #175 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-white-not-hispanic-historical-1975-1972` — #174 (Codex). 44c/8r/4 standalone; strict-default GREEN; independent pypdf source comparison 44/44 exact; historical WHITE, NOT HISPANIC complete.
- 2026-07-18 · `census-p60/2023-income-a2-white-not-hispanic-historical-1988-1976` — #173 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-white-not-hispanic-historical-2001-1989` — #172 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-white-alone-not-hispanic-2012-2002` — #171 (Codex). 121c/22r/11 standalone; strict-default GREEN; independent pypdf source comparison 121/121 exact; modern WHITE ALONE, NOT HISPANIC complete.
- 2026-07-18 · `census-p60/2023-income-a2-white-alone-not-hispanic-2023-2013` — #170 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact. **Different-agent audit GREEN (Antigravity); #171 unblocked.**
- 2026-07-18 · `census-p60/2023-income-a2-white-historical-1975-1967` — #169 (Codex). 99c/18r/9 standalone; strict-default GREEN; independent pypdf source comparison 99/99 exact; historical WHITE complete.
- 2026-07-18 · `census-p60/2023-income-a2-white-historical-1988-1976` — #168 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-white-historical-2001-1989` — #167 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-white-alone-2012-2002` — #166 (Codex). 121c/22r/11 standalone; strict-default GREEN; independent pypdf source comparison 121/121 exact; WHITE ALONE complete.
- 2026-07-18 · `census-p60/2023-income-a2-white-alone-2023-2013` — #165 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-all-races-1978-1967` — #164 (Codex). 132c/24r/12 standalone; strict-default GREEN; independent pypdf source comparison 132/132 exact; ALL RACES complete.
- 2026-07-18 · `census-p60/2023-income-a2-all-races-1991-1979` — #163 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-all-races-2004-1992` — #162 (Codex). 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact.
- 2026-07-18 · `census-p60/2023-income-a2-all-races-2016-2005` — #161 (Codex). Table A-2 ALL RACES continuation; 143c/26r/13 standalone; strict-default GREEN; independent pypdf source comparison 143/143 exact; 2013 redesigned row closes at source-authorized tol 0.2.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-e-direct-part2` — #160 (Antigravity). Schedule E Direct Loans Part 2; post-audit 179c/23r (was 175c). **Every-10th audit GREEN after completeness repair** (Grok: 175/175 present values exact; inserted Transitional Housing −1 + AID International Debt Reduction −172/−172/−172; `AUDITS.md`).
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-e-direct-part1` — #159 (Antigravity). Schedule E Direct Loans Part 1; 136c/18r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-e-guaranteed` — #158 (Antigravity). Schedule E Guaranteed Loans; 181c/17r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-d-trust-funds` — #157 (Antigravity). Schedule D Trust Funds; 224c/30r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-d-federal-funds-labor-totals` — #156 (Antigravity). Schedule D Federal Funds Labor-Totals; 116c/18r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-d-federal-funds-agri-just` — #155 (Antigravity). Schedule D Federal Funds Agriculture-Justice; 48c/6r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-c-epa-ind` — #154 (Antigravity). Schedule C EPA-Independent; 73c/8r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-c-treas-vets` — #153 (Antigravity). Schedule C Treasury-Veterans; 35c/1r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-c-hhs-trans` — #152 (Antigravity). Schedule C HHS-Transportation; 68c/3r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-c-comm-energy` — #151 (Grok). Schedule C Commerce–Energy; 62c/5r.
- 2026-07-18 · `treasury-mts/2026-05-table6-schedule-c-agri` — #150 (Grok). Schedule C Agriculture; 93c/10r. **Every-10th audit GREEN** (Antigravity; `AUDITS.md`).
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
