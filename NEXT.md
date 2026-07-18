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

**Completed so far — corpus #1–90, all reconcile GREEN under strict
coverage** (per-unit specs in `BACKLOG.md`, session detail in the
control-plane project log):

- **Treasury MTS Table 4 + Table 5, seed units (Apple, Census), BLS 2024
  CPI relative importance** — #1–63, complete (incl. the optional
  Table-5 grand-sum capstone #63).
- **FEC 2024 presidential general** — #64–74, complete (11 units).
- **OMB FY2027 Legislative Branch** — *in progress*: CBO #75; Library of
  Congress family 10/10 (#76–85); US Tax Court family 3/3 (#86–88);
  Capitol Police 2/4 (Salaries #89, General Expenses #90).

Every-10th different-agent spot-audits GREEN through #90. Unit #90
(Capitol Police General Expenses) was independently audited GREEN by Codex
in `AUDITS.md`. Next audit lands at #100. In the OMB chapter,
Senate + House (pp1–4) carry **zero** P&F schedules (pure appropriations
language, out of scope); the chapter has ≈40–45 real accounts.

### Live dispatch — OMB FY2027 Legislative Branch (PDF → vision, render-anchored)

- **GAO Salaries and Expenses (page 28-29, id `005-0107-0-1-801`) —
  LARGE, likely needs a split, do NOT attempt as one cap-fit unit
  without re-assessing:** single account but ~53 P&F rows alone (five
  program-activity goals 0001-0005 with their own
  0799/0801/0803/0805/0809/0899/0900 subtotal structure, plus the usual
  budgetary-resources/change-in-obligated-balance/budget-authority-net
  sections, all with offsetting-collections complexity similar to
  FEDLINK) + ~19 Object Classification rows + 2 Employment rows. Rough
  estimate **200+ cells** — well past the ~140-180 ceiling every other
  single-account unit in this corpus has stayed under. Whoever picks
  this up should re-measure properly first (like the Treasury MTS Table 5
  over-cap tier) and decide: split by the five GOAL program activities
  (mirrors the Treasury `-bureaus`/`-departmental` pattern), or take it
  as one unit if a higher ceiling is acceptable. **D1/D2 sizing pass
  needed before this is D2 execution.**

- **Capitol Police (pp5-6) — 2 of 4 accounts SHIPPED 2026-07-18
  (Salaries #89, General Expenses #90); pp5-6 now fully read.** Two
  small accounts remain, both D2 cap-fit:
  1. `omb/budget-appendix-fy2027-leg-capitol-police-security-enhancements`
     (id `002-0461-0-1-801`, page 6) — near-degenerate P&F: only
     1000/1930/1941 populated (all = 1), 4180/4190 blank. Est. ~6-9
     cells; likely **0 relations** (1930 = 1000 single-source, no
     appropriation printed), all standalone. Trivial closeout unit.
  2. `omb/budget-appendix-fy2027-leg-capitol-police-mutual-aid`
     (id `002-0478-0-1-801`, page 6) — U.S. Capitol Police Mutual Aid
     Reimbursements. Medium discretionary account (0001/0900,
     1000/1100/1930, 3000/3010/3020/3050, 4000/4010/4011/4020/4180/4190;
     several cols blank in 2027 est.). Est. ~40-50 cells. Clean (no
     offsetting collections). Render + values already captured in
     `scratchpad/cap-p6-*`.

- **Office of Congressional Workplace Rights — Salaries and Expenses
  (id `009-1600-0-1-801`, page 6, right column, immediately after
  Capitol Police):** small clean discretionary account (0001/1100/1930,
  3010/3020, 4000/4010/4180/4190; ~8/8/9 grid). Est. ~20-25 cells, D2
  cap-fit — spotted while reading Capitol Police page 6, dispatch-ready.

- **OMB chapter still fully unsized beyond the above:** Architect of
  the Capitol (~14-15 accounts, pp8-16, the largest remaining
  department), GPO (3, pp25-28), Legislative Branch Boards and
  Commissions (~8-10 tiny commissions, pp31-37). Each needs a
  survey/sizing pass before it is dispatch-ready.

- **FEC footnote pages pp7-9** stay a Tier-3 stage concern (DESIGN §8) —
  not yet in scope.

---

## Shipped

One line per shipped unit/batch, newest first. Full specs in
`BACKLOG.md`; session narrative in the control-plane project log.

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
