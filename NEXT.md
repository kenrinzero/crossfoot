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

- **NEXT DISPATCH — `sec-10k/msft-fy2025-balance-sheet` (#331; D3,
  HTML, no vision).** Vendored + sized 2026-07-19:
  `sources/sec-10k/msft-fy2025-balance-sheet-R4.htm` (sha256 ledgered,
  content-gated; NOTE R4 in this filing, not R5 as in Apple's). 34 rows
  × 2 fiscal-year columns (Jun. 30 2025 / 2024) = 68 values; 7 sum
  relations per column (cash+STI, Total current assets, Total assets,
  Total current liabilities, Total liabilities, Total stockholders'
  equity incl. negative AOCI leaf, Total L+E = A) — all pre-verified
  EXACT both columns, no tolerances. Wrinkles: Short-term debt prints a
  real `0` in col 1 (transcribe it — printed zero, not blank); AOCI is
  negative; label-embedded parenthetical numbers (allowance,
  accumulated depreciation, share counts) belong to the R5
  parenthetical statement, NOT this unit. Follow the Apple #2 seed
  conventions (BACKLOG rows for both).

- **D1/web vendoring (later):**
  - Treasury MTS **July 2026** — probed 2026-07-19: not yet published
    (503 + HTML body, caught by the magic-byte check). Expected
    ~mid-August at the fiscaldata static path; re-probe then.
  - Further MSFT FY2025 statements (income R2, cash flows R6, same
    accession dir) — available as follow-ons; need vendoring + sizing.

- **FEC footnote pages pp7–9** stay a Tier-3 stage concern (DESIGN §8)
  — not yet in scope.

**Audit cadence:** every-10th different-agent spot-audits GREEN through
**#330** (records + batch-numbering tie-break rule in `AUDITS.md`;
real catches so far: #129 missing memo row, #160 two missing standalone
rows, #250 systematic A-5 year-shift). Next fires at **#340**.

---

## Shipped

Family/batch granularity, newest first. Per-unit specs and shipped
status live in `BACKLOG.md`; session narrative in the project log
(pre-2026-07-19 detail in its `log-archive/`).

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
