# NEXT — rolling dispatch queue

The routing view: the next few sessions, in suggested order, with
difficulty and harness needs. `BACKLOG.md` stays the unit manifest
(specs, caps, minimums, per-unit shipped status); `DESIGN.md` the frozen
contract; `AUDITS.md` the audit records; the control-plane project log
(`.atelier/projects/coding/crossfoot/log.md`) holds the per-session
narrative. This file is only for deciding *who does what next* — keep it
lean: when a unit ships, drop it from the Queue and add a one-line entry
to *Shipped* (family/batch granularity; the detail already lives in
BACKLOG + the project log). Trimmed to this shape 2026-07-19; the full
per-unit history is in git and the archived project log.

**Rolling rules:** take the topmost session that fits your harness; when
shipped, remove its Queue block and prepend a one-liner to *Shipped*
(newest first). Append newly-visible sessions to the Queue.
Re-sequencing is allowed — note why.

**Difficulty labels — this repo says D, not T:** task difficulty is
written **D1/D2/D3** ≡ the CHARTER's fleet-wide T1/T2/T3 (Kenrin,
2026-07-13), because crossfoot's own "Tier N" names are project *stages*
(strict-coverage flip / footnote pass / new relation types). "Tier N"
in this repo always means a stage, never difficulty.

**Dispatched single-unit agents:** follow `RUNBOOK-transcriber.md` /
`RUNBOOK-auditor.md` — self-contained flows, no deep orientation needed.

**Harness notes for transcribers:**
- ⚠ **Recurring venv breaker:** if EVERY `uv run` fails with `failed to
  remove .venv/lib64: Access is denied (os error 5)`, a POSIX-side
  session has left a stray `lib64 -> lib` symlink in `.venv`. Fix:
  `rm .venv/lib64` — uv then rebuilds cleanly. A sweep run through a
  broken uv reports every unit RED — fix the venv BEFORE believing a
  red sweep.
- No poppler on either host; PDF units use `uv run --with pdfplumber`
  (text layer) + a pypdfium2 page render for visual verification. The
  MTS PDF text layer emits `(cid:NN)` tokens — decode `chr(NN+29)`.
  PDF units want a **vision-capable** agent (the render check is
  mandatory discipline); HTML units do not.
- The gate for every transcription: `uv run python reconcile.py <file>`
  GREEN with 0 warnings (strict coverage default), relations ≥ manifest
  minimum, `uv run pytest` green, one new file only.
- Cross-check row COUNTS against the print — a missing standalone-class
  row is invisible to strict coverage (bit us at #129 and #160).

---

## Queue

- **UNBLOCKED (2026-08-17):** the #360 every-10th audit closed **GREEN**
  (Claude Opus 5; whole-batch positional check of #351–#360, 1,485 cell
  positions vs an independent parse, plus a Table 3 cross-table tie on all
  four departmental capstones — AUDITS.md). #361 may ship. **Next
  every-10th audit fires at #370.**

- **Treasury MTS July 2026 — 61 of 80 units remain, D-tiered.** The D1 vendoring is DONE
  (2026-08-17): published 2026-08-12, vendored, gated, ledgered. **#342–#360 shipped**:
  table1, table2, table3 ×3, table9, receipts-major, outlays-legislative,
  outlays-judicial, outlays-eop, agriculture ×3, commerce, defense ×3,
  education ×2 — every one matching its June twin's row/cell/relation
  counts exactly, table1 and the two capstones with printed-month deltas
  aside (noted per unit in BACKLOG). **`BACKLOG.md`
  § *Treasury MTS July 2026* carries the full unit table with a D level
  and a `needs` tag per unit** — take the topmost row that fits your
  harness.
  - **All 80 are PDF units → vision-capable agent required**, no
    exceptions; the render check is the discipline, and the text layer
    emits `(cid:NN)` (decode `chr(NN+29)`). `uv run --with pdfplumber`.
  - **D2 ×64 / D3 ×16.** D3 = flat blocks (≤60 cells, ≤15 relations, no
    capstone/split structure) or all-standalone; D2 = the rest. Full
    derivation rule in the BACKLOG section so it can be re-checked.
  - **Order within the family:** ship a department's `-bureaus` /
    programme units BEFORE its `-departmental` capstone — capstones are
    tagged `ties-siblings` and re-anchor sibling totals.
  - **Floors are provisional** (inherited from the June twins). A floor
    you cannot reach honestly is a finding — stop and log; never pad,
    and never invent a row to match June (#340 defect class).
  - **Audit:** #350 closed **GREEN** 2026-08-17 (Qoder; whole-family check)
    and #360 closed **GREEN** the same day (Claude Opus 5; whole-batch
    positional check of #351–#360 + Table 3 cross-table ties). Both in
    AUDITS.md. Corpus unblocked; next every-10th fires at **#370**.

- **Treasury MTS August 2026** — probed 2026-08-17: not yet published
  (503 + HTML body). Expected ~mid-September; re-probe then.

- **FEC footnote pages pp7–9** stay a Tier-3 stage concern (DESIGN §8)
  — not yet in scope.

**Audit cadence:** every-10th different-agent spot-audits GREEN through
**#360** (records + batch-numbering tie-break rule in `AUDITS.md`;
real catches so far: #129 missing memo row, #160 two missing standalone
rows, #250 systematic A-5 year-shift). #331, #332, #333 shipped without audits;
#340 audited GREEN (ZCode; post-audit repair recorded in AUDITS.md); #341 shipped
without audit per cadence; **#342–#350 audited GREEN together 2026-08-17 (Qoder,
whole-family positional check)**; **#351–#360 audited GREEN together 2026-08-17
(Claude Opus 5, 1,485 positions + cross-table ties)**. Next fires at **#370**.

**Standing note for the next auditor:** the last two every-10th audits both
widened scope from the 10th unit to the whole ten-unit batch, because both
batches came from a single agent. That is now the family's working practice —
one unit audited alone is thin cover when ten consecutive units share a
transcriber (the #340 precedent). Whole-batch positional checking is cheap here:
Table 5's text layer parses into `(label, 9 values)` records, so the auditor can
compare presence *and* absence for every cell rather than sample.

---

## Shipped

Family/batch granularity, newest first. Per-unit specs and shipped
status live in `BACKLOG.md`; session narrative in the project log
(pre-2026-07-19 detail in its `log-archive/`).

- 2026-08-17 · **treasury-mts July 2026 batch #356–#360 (5 units)** — defense-programs (88c/18r), defense-rdte (84c/12r, 24 FH standalones), defense-departmental capstone (155c/12r, +4 printed cells over June, ties-siblings byte-match machine-checked), education-bureaus (92c/22r), education-departmental capstone (93c/13r, ties-siblings byte-match). All strict-default GREEN 0 warnings; sweep 360/360. Max tol 2 (24-component capstone grand roll-ups). **#360 fires the every-10th audit — corpus blocked, see AUDITS.md.**
- 2026-08-17 · **treasury-mts July 2026 batch #352–#355 (4 units)** — agriculture-programs (126c/22r), agriculture-fns (80c/14r), agriculture-departmental capstone (208c/37r, ties-siblings byte-match machine-checked), commerce (75c/20r). All strict-default GREEN 0 warnings; sweep 355/355. Notable: the capstone's Prior-FYTD Outlays grand roll-up carries an adjudicated tol=3 (25 components, 196,013 vs printed 196,010, page-23 note quoted).
- 2026-08-17 · **treasury-mts/2026-07-outlays-eop** — #351 (D3/PDF/vision; 43c/9r, strict-default GREEN 0 warnings; 6 tol-1 computed against the p23 footnote, two net identities + col-3 roll-up exact; +2 printed cells over the June twin on Unanticipated Needs)
- 2026-08-17 · **treasury-mts July 2026 batch #343–#350 (8 units)** — table2, table3-receipts, table3-outlays-departments, table3-outlays-remainder, table9, receipts-major, outlays-legislative, outlays-judicial. All strict-default GREEN 0 warnings; sweep 350/350. Every unit matches its June twin's row/cell/relation counts *and* role distribution. Notables: `receipts-major` re-cited to page 9 (Table 4) where its lines are printed rather than derived — the June twin's page-8 citation looks wrong; `outlays-legislative` carries the family's only tol=2 (13-component roll-up, Table 5's footnote is on p23 not p10). **#350 opens the every-10th audit — corpus blocked, see AUDITS.md.**
- 2026-08-17 · **treasury-mts/2026-07-table1** — #342, family opener (D2/PDF/vision; 72c/30r, strict-default GREEN 0 warnings; 24 rows, one month more than the June twin; 8 tol-1 relations computed per-relation, the six FY2025 ones landing on exactly June's). Three checks beyond reconcile: 39 FY2025 values byte-identical to the June unit, June YTD + July month = July YTD exact in all 3 columns, Table 1 ties Table 2 on all 6 same-page figures. Sweep 342/342 GREEN.
- 2026-07-19 · **sec-10k no-vision runway COMPLETE (11/11, #331–341)** — trial-fleet run: #331 balance sheet (Mavis), #332–333 parentheticals (Trinity/Nanobot, Step), #334–335 comprehensive income (Ring), #336–337 income/operations (Hunyuan), #338 aapl cash flows (Qwen), #339 msft cash flows (Zed/Nemotron), #340 msft stockholders' equity (Copilot CLI; **every-10th audit GREEN by ZCode**, post-audit review repair: 2 unprinted duplicate begin-balance rows removed, see AUDITS.md), #341 aapl shareholders' equity (Mistral Vibe). Review pass (Claude Fable 5): all 11 units machine-verified EXACT multiset vs source, NI/cash cross-unit ties hold, sweep 341/341 GREEN.
- 2026-07-19 · **aapl-fy2023-cash-flows** — #338 (D3/HTML/no-vision; 90c/15r + 6 standalone supplemental, strict-default GREEN; ops/investing/financing subtotals + net change + roll-forward all exact; NI byte-matches operations unit #337)
- 2026-07-19 · **aapl-fy2023-operations** — #337 (D3/HTML/no-vision; 57c/21r + 12 standalone EPS/shares, strict-default GREEN; GM→TotalOpEx→OpInc→IBT→NI chain + products/services splits exact all cols; NI byte-matches comprehensive-income unit #335)
- 2026-07-19 · **msft-fy2025-income** — #336 (D3/HTML/no-vision; 57c/18r + 12 standalone EPS/shares, strict-default GREEN; GM→OpInc→IBT→NI chain + product/service splits exact all cols; NI byte-matches comprehensive-income unit #334)
- 2026-07-19 · **aapl-fy2023-comprehensive-income** — #335 (10 rows × 3 cols; 30c/12r, strict-default GREEN; NI must byte-match operations unit)
- 2026-07-19 · **msft-fy2025-comprehensive-income** — #334 (6 rows × 3 cols; 18c/6r, strict-default GREEN; OCI = 3 components, CI = NI + OCI, both exact all cols; NI byte-matches income unit)
- 2026-07-19 · **aapl-fy2023-balance-sheet-parenthetical** — #333 (Step; 8c/0r, all standalone; par value 0.00001 decimal; share counts in whole shares; strict-default GREEN)
- 2026-07-19 · **msft-fy2025-balance-sheet-parenthetical** — #332 (Trinity, Nanobot harness; Mavis extra audit per Kenrin's request, AUDITS.md) — 8c/0r, all standalone, every value single-source; share counts in whole shares; strict-default GREEN
- 2026-07-19 · **sec-10k no-vision runway STARTED** — #331
  (`msft-fy2025-balance-sheet`, Mavis; 68c/14r, strict-default GREEN,
  A=L+E foot exact both columns; printed-0 short-term debt col1
  transcribed; AOCI leaf negative; label-embedded parentheticals
  dropped per project log — R5 unit's scope). 5 more units queued
  in NEXT.md; next every-10th audit at #340.
- 2026-07-19 · **Treasury MTS June 2026 SOURCE COMPLETE** — #251–330
  (Grok, 8×10-unit batches; vendored `mts-202606.pdf` same day):
  Tables 1–3, 9, full Table 5 detail incl. grand-total capstone, Table
  6 + Schedules A–E, Tables 7–8. Audits #260–#330 all GREEN. **#330
  audit GREEN (Claude Fable 5) closed the source; #331+ unblocked.**
- 2026-07-19 · **Census P60-282 appendix COMPLETE** — #201–250 (Claude
  Fable 5 seeded conventions #201–210; Grok #211–250): A-1, A-3,
  A-4a/b, A-5, A-6, A-7, B-1..B-5. The #250 audit caught + fixed a
  systematic A-5 year-shift (all 6 files re-extracted).
- 2026-07-18 · **Census P60-282 Table A-2 COMPLETE** — #161–200
  (Codex): all race/ethnicity groups, 41 source-native units with the
  legacy-named seed #3; independent pypdf comparisons exact throughout.
- 2026-07-18 · **Treasury MTS May 2026 SOURCE COMPLETE** — #130–160
  (Antigravity sized 21 cap-fit units; Grok + Antigravity shipped):
  Tables 1–3, 9, 7, 8 + Table 6 family with Schedules A–E.
- 2026-07-18 · **OMB FY2027 Legislative Branch chapter COMPLETE** —
  #75–129 (55 units; Antigravity, Claude Sonnet 5, Claude Opus
  4.6/4.7/4.8, Codex, Claude Fable 5): CBO, LoC 10/10, US Tax Court
  3/3, Capitol Police 4/4, OCWR, GAO 2/2 (by-schedule over-cap split
  precedent), GPO 4/4, Boards and Commissions 15 units, AoC 13
  accounts. Family wrinkle catalogue preserved in the 2026-07-19 log
  archive summary. Senate/House pp1–4 carry no P&F schedules (out of
  scope); pp38–40 are General Provisions (out of scope).
- 2026-07-17 · **FEC 2024 presidential general COMPLETE** — #64–74
  (Kimi): electoral votes, popular-vote blocks pp2–6, cross-page
  per-state TOTAL VOTES re-anchor capstone (national 155,238,302).
- 2026-07-13…16 · **Corpus #1–63** — Treasury MTS May Table 4 + Table
  5 (incl. grand-sum capstone #63), seed units (Apple FY2023 balance
  sheet, Census brackets), BLS 2024 CPI relative importance; plus the
  strict-coverage-default harness flip.
