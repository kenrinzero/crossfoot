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
  mandatory discipline, not decoration). The HTML unit (Apple) does not.
- The gate for every transcription: `uv run python reconcile.py <file>
  --strict-coverage` GREEN with 0 warnings, relations ≥ manifest minimum,
  `uv run pytest` still green, one new file only.

---

## Queue

### 1. sec-10k/aapl-fy2023-balance-sheet — **D2** · local-only · no vision needed
The flagship: per-column roll-ups + the assets = liabilities + equity
identity, two fiscal-year columns. Min 12 relations, ≤140 cells.
**Why D2 not D3:** the R5 HTML is machine-readable but visually nested
(indent hierarchy, parenthesized negatives → `-`, section subtotals) —
mapping the roll-up tree takes care, not just reading cells.

### 2. census-p60/2023-income-a1 — **D2** · local-only · vision needed (PDF)
Income brackets sum to total; percent distribution closes to 100 — the
corpus's first `percent-closure` relations (default tol ±0.05 needs no
`why`; only non-default tols do). Min 8 relations, ≤150 cells.
**Why D2:** PDF extraction + first use of the second relation type; the
arithmetic itself is simple.

### 3. tier1/strict-coverage-default — **D2 (harness)** · local-only · after 1–2 are green
Crossfoot's "Tier 1" stage: make `--strict-coverage` the default in
`reconcile.py`, add the manifest column for granted `standalone` waivers,
keep all shipped tables + fixtures behaving (mini-uncovered must still
red). **Why D2:** small, fully pre-specified in BACKLOG/DESIGN § 4; it
just edits the oracle, so it must NOT be folded into any transcription
session. Note: the shipped Treasury unit already passes strict — the flip
should be a no-op for the corpus so far.

### 4. bls-cpi/relative-importance-2024 vendoring — **D1 (web)** · needs browser
Save `https://www.bls.gov/cpi/tables/relative-importance/2024.htm` into
`sources/bls-cpi/` + SOURCES.md ledger row (sha256, retrieval date, URL)
+ content sanity check + a sized manifest row. Akamai 403s curl and
Windows TLS — needs a browser-capable session (Windows side has them) or
Kenrin. **Why D1:** provenance judgment + bot-gate navigation + sizing
the future unit; the transcription that follows is a separate D2/D3.

### 5. treasury-mts/2026-05-receipts-detail — **D2** · local-only · vision needed (PDF)
Slice the remainder of Table 4 (~160 cells) into ≤120-cell units and ship
the first. Suggested cut (verify before trusting): the Employment &
General Retirement subtree is ~105 cells and self-contained (OASI/DI/HI
pyramids — dense sum structure). Add the slice rows to BACKLOG first.
**Why D2:** the slicing decision + footnote-marker hazards (BACKLOG)
demand judgment; pure transcription of a decided slice would be D3.

## Not yet sequenced

- treasury-mts/2026-05-outlays — Table 5 size/split decision, then units.
- fec/2024-presidential-general, omb/budget-appendix-slice — D1 (web)
  vendoring first.
- Spot-audit at unit 10 — **D3**, MUST be a different agent than the
  transcribers (DESIGN § 6), non-arithmetic checks → AUDITS.md.

---

## Shipped

- 2026-07-13 · treasury-mts/2026-05-receipts (D2, went to Claude Fable 5) —
  Table 4 major-classification slice; 87 cells, 42 relations, 11 tol-1
  with quoted rounding note; strict-coverage GREEN. Commit `069e687`.
  In hindsight D2 was right: the cid-font decode + slice decision needed
  judgment; future *decided* slices of the same PDF are D3-adjacent.
