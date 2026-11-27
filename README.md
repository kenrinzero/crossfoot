# Crossfoot

An arithmetic-reconciled corpus of public statistical tables: each messy
PDF/HTML table is transcribed into a typed `.cells.json` that declares the
table's own internal arithmetic — row totals, subtotals, percent closures,
balance identities — and `reconcile.py` re-derives every declared relation
from the transcribed cells. The source's redundancy is the proof: a typo in
a cell that feeds a printed total almost always breaks a cross-foot, so for
those cells correctness is derived, not trusted.

The arithmetic reaches four cells in five. The rest are printed numbers
that nothing in their table adds up to (medians, margins of error, ratios,
comparison columns); they are checked against the source by audit instead.
[What is verified, and how](#what-is-verified-and-how) gives the split in
numbers and the known gaps.

```jsonc
// a cell, and a relation the reconciler re-derives from leaf cells
{ "id": "r15c1", "row": 15, "col": 1, "value": "6274791", "role": "total" }
{ "type": "sum", "sources": ["r1c1", "...", "r14c1"], "target": "r15c1",
  "tol": "2", "why": "Table 8 prints: 'Details may not add to totals due to rounding.'" }
```

All arithmetic runs in exact `Decimal` — never floats. Values are decimal
strings exactly as printed. A sum must close exactly unless its relation
carries a tolerance, and a tolerance needs a `why`: by rule the source's
own rounding note, quoted (the few other cases are listed
[below](#what-is-verified-and-how)). Strict coverage (every `total`
targeted, every `leaf` feeding a relation) is the default gate; a cell that
takes part in no arithmetic is marked `standalone` and must say why.

## The corpus

**581 units, all GREEN** (2026-11-27):

| family | source | units |
|---|---|---|
| `treasury-mts` | Monthly Treasury Statement, May through September FY2026 complete (Tables 1–9 incl. full Table 5 outlay detail and Table 6 Schedules A–E); September is the Final FY2026 statement | 405 |
| `census-p60` | Census P60-282 *Income in the United States: 2023* — the complete appendix (A-1…A-7, B-1…B-5) | 91 |
| `omb` | OMB FY2027 Budget Appendix, Legislative Branch chapter — complete (every account with a printed schedule) | 55 |
| `sec-10k` | Apple FY2023 + Microsoft FY2025 10-K statement sets (complete: balance sheet, income, comprehensive income, cash flows, equity, parentheticals) | 12 |
| `fec` | Official 2024 presidential general election results — complete | 11 |
| `bls-cpi` | CPI relative importance of components, Dec 2024 — complete | 7 |

Per-unit specs live in [BACKLOG.md](BACKLOG.md), the authoritative
manifest.

The corpus is **US sources only** (US government publications and SEC
public filings). Non-US families are out of scope.

Every vendored source in `sources/` is sha256-ledgered with provenance in
[sources/SOURCES.md](sources/SOURCES.md) — transcribed verbatim, never
edited.

## What is verified, and how

Figures are for the 581 units as of 2026-11-27. GREEN means a unit passes
`reconcile.py` with zero coverage warnings.

**By arithmetic: 46,039 of 56,823 cells (81.0%).** These are the `leaf`
and `total` cells. Each takes part in at least one of the 11,049 declared
relations (10,460 sums, 589 percent closures), and `reconcile.py`
re-derives every relation on every run.

**Not by arithmetic: 10,784 cells (19.0%).** These are `standalone`:
printed numbers that no declared relation touches, each with a stated
reason. For them GREEN says nothing about the value; a typo there passes
the reconciler.

| family | cells | standalone | share |
|---|---:|---:|---:|
| `census-p60` | 10,454 | 4,962 | 47.5% |
| `omb` | 3,984 | 1,393 | 35.0% |
| `sec-10k` | 596 | 71 | 11.9% |
| `treasury-mts` | 39,995 | 4,305 | 10.8% |
| `fec` | 1,136 | 43 | 3.8% |
| `bls-cpi` | 658 | 10 | 1.5% |

37 units (2,918 cells) declare no relation at all: 22 Census tables of
medians, inequality measures, ratios and percent changes; 7 small OMB
schedules; 6 Treasury units that list department or receipt lines without
a total inside the unit; and 2 SEC parenthetical statements. For those
units GREEN means only that the file is well-formed and labelled.

### What covers the cells arithmetic cannot see

**Different-agent audits against the source.** Every tenth unit is audited
by an agent that did not transcribe it
([RUNBOOK-auditor.md](RUNBOOK-auditor.md)). Up to unit #341 the audit
covered the tenth unit of each batch — a sample of its cells, often the
whole unit. From #342 on (the July, August and September Treasury
statements) each audit compares every printed position of its whole
batch, not a sample. The trail, including the defects the audits caught
and the ones they missed, is in [AUDITS.md](AUDITS.md).

**A row-level check of the whole corpus (2026-11-27).** For every row of
every unit, the row's values were looked up on one printed line of the
source: one line of the PDF text layer, or one HTML table row.

| family | rows | found on one printed line | not matched |
|---|---:|---:|---|
| `treasury-mts` | 6,566 | 6,566 | — |
| `census-p60` | 1,291 | 1,290 | 1: a printed `Z` transcribed as `0`, a documented convention |
| `omb` | 1,491 | 1,491 | — |
| `bls-cpi` | 329 | 329 | — |
| `sec-10k` | 245 | 245 | — |
| `fec` | 399 | 347 | 52 summary rows that combine several printed blocks by design; every one of their values is printed in the document |

The first run found three wrong values, all in the June Treasury statement
and two of them in `standalone` cells. They were corrected the same day;
the table shows the state after the correction, and it counts one Treasury
row that was added later that day and checked against its printed line.
The check compares values, not their order within a row or the label the
row sits under, and it cannot see a printed number that is missing from a
unit. It was a one-off: the script is not part of this repository or its
gates. Method and findings are in
[AUDIT-2026-11-27.md](AUDIT-2026-11-27.md). A later comparison of 17
Treasury units column by column found one value in the wrong column, a
kind of error the row-level check cannot see. It was moved to the column
the page prints it in ([AUDITS.md](AUDITS.md), *Directed follow-up*). The
rest of the corpus has not had a column-by-column comparison outside the
audits.

### Tolerances

7,007 of the 10,460 sums close exactly. The other 3,453 carry a tolerance
equal to the observed difference, each with a `why`. In all but six of
them the `why` is the source's own rounding note. 74 are larger than one
unit of the last printed digit per source, so they are not ordinary
rounding of the printed digits:

- **64 Census relations** (tolerance 5 to 70). The source prints these
  household and worker counts rounded to four significant digits, so sums
  of them drift by tens. The `why` cites the Census footnote on rounded
  components.
- **6 relations in `treasury-mts/2026-06-table6-schedule-e-guaranteed`**,
  recorded as source discrepancies, not as rounding. The June statement
  prints three figures on page 32 that do not agree with its own lines,
  and the corpus keeps the printed figures:
  - **four at tolerance 90.** Two closing balances (Business Loan Fund and
    the Net Activity total) each differ by 90 from both of their
    roll-forwards. The July statement opens both lines at the computed
    values.
  - **one at tolerance 182.** The column total over those closing
    balances inherits both gaps (182 = 90 + 90 + 2 of rounding).
  - **one at tolerance 2,724.** The prior-year column: its 24 printed
    lines sum to 3,034 and the page prints the total as 310. The
    statement's own Table 6 on page 24 agrees with the lines.

  A sum that carries such a tolerance cannot catch an error smaller than
  the tolerance. The cells under these six relations rest on the source
  check and the audits, not on arithmetic.
- **4 relations in `bls-cpi/relative-importance-2024-education-other`**
  (tolerance 0.008 to 0.009 on three or four three-decimal components).
  Recorded as rounding, but rounding of the printed digits allows at most
  0.0025. Unresolved.

Percent closures allow ±0.05 by default; 299 of the 589 declare 0.1 or
0.2, each with a `why`.

### Known gaps

- **Column positions.** One value was found in the wrong column on
  2026-11-27 and moved. Only 17 Treasury units have been compared with
  the page column by column outside the audits, so others may exist in
  units audited by sample (up to #341).
- **Labels.** Row and column labels sometimes use the corpus's wording
  rather than the printed header: the printed "Beginning of This Month"
  appears as "Close of Prior Month" in some units. Unit notes say so, but
  labels were never checked corpus-wide. Join months by position, not by
  label alone.
- **Source errors stay in.** Cells hold what the source prints, including
  the three June figures listed under [Tolerances](#tolerances).

## Process

The corpus is transcribed and audited by a rotating fleet of AI agents —
37 model identities to date, credited in
[CONTRIBUTORS.md](CONTRIBUTORS.md) — under a fixed discipline:

- one session = one unit = one new file, gated by `reconcile.py` GREEN
  with zero coverage warnings ([AGENTS.md](AGENTS.md) has the rules;
  [RUNBOOK-transcriber.md](RUNBOOK-transcriber.md) the session flow);
- every 10th unit triggers a **different-agent audit** against the
  source, as described [above](#what-covers-the-cells-arithmetic-cannot-see);
- PDF units are render-anchored (a vision model must look at the page,
  not just the text layer); HTML units run text-only.

Older audit records cite files under `scratchpad/` (page renders, text
dumps, one-off scripts). That folder is local working space and is not
part of the repository; the copies that were tracked before 2026-11-27
remain in the git history.

## Running it

```bash
uv venv && uv sync                                     # once
uv run python reconcile.py tables/<family>/<id>.cells.json
uv run pytest                                          # oracle self-tests
uv run python reconcile.py --all                       # full sweep (empty selection is red; any unit failure is red)
```

## License

MIT for code and transcriptions (see [LICENSE](LICENSE)). `sources/`
contains vendored public documents (US government / SEC public filings)
with per-file provenance in `sources/SOURCES.md`.
