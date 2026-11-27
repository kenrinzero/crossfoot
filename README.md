# Crossfoot

[![check](https://github.com/kenrinzero/crossfoot/actions/workflows/check.yml/badge.svg)](https://github.com/kenrinzero/crossfoot/actions/workflows/check.yml)

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

**610 units, all GREEN** (2026-11-27):

| family | source | units |
|---|---|---|
| `treasury-mts` | Monthly Treasury Statement, May through September FY2026 complete (Tables 1–9 incl. full Table 5 outlay detail and Table 6 Schedules A–E); September is the Final FY2026 statement. The October 2026 statement (FY2027, month 1) is in progress: 29 of its 80 units are shipped | 434 |
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

Figures are for the 610 units as of 2026-11-27. GREEN means a unit passes
`reconcile.py` with zero coverage warnings.

**By arithmetic: 48,333 of 59,424 cells (81.3%).** These are the `leaf`
and `total` cells. Each takes part in at least one of the 11,523 declared
relations (10,934 sums, 589 percent closures), and `reconcile.py`
re-derives every relation on every run.

**Not by arithmetic: 11,091 cells (18.7%).** These are `standalone`:
printed numbers that no declared relation touches, each with a stated
reason. For them GREEN says nothing about the value; a typo there passes
the reconciler.

| family | cells | standalone | share |
|---|---:|---:|---:|
| `census-p60` | 10,454 | 4,962 | 47.5% |
| `omb` | 3,984 | 1,393 | 35.0% |
| `sec-10k` | 596 | 71 | 11.9% |
| `treasury-mts` | 42,596 | 4,612 | 10.8% |
| `fec` | 1,136 | 43 | 3.8% |
| `bls-cpi` | 658 | 10 | 1.5% |

38 units (3,030 cells) declare no relation at all: 22 Census tables of
medians, inequality measures, ratios and percent changes; 7 small OMB
schedules; 7 Treasury units that list department or receipt lines without
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

**A check of every unit against its source (`tools/sourcecheck.py`).**
The tool reads the vendored PDF or HTML and compares it with each unit at
two levels.

- *Row level.* The values of a unit row must all be found on one printed
  line of the source: one line of the PDF text layer, or one HTML table
  row. This catches a wrong value, also in a `standalone` cell.
- *Column level.* Each cell must sit in the column the page prints it in,
  and where a unit has no cell the page must not print a number. This
  catches a value in the wrong column, a kind of error the row level
  cannot see. The printed columns are found from the positions of the
  numbers on the page; nothing is set up per table.

Whole-corpus run through unit #581 on 2026-11-27:

| family | rows | found on one printed line | every cell in its printed column |
|---|---:|---:|---|
| `treasury-mts` | 6,566 | 6,566 | 6,566 |
| `census-p60` | 1,291 | 1,291 | 1,291 |
| `omb` | 1,491 | 1,491 | 1,491 |
| `bls-cpi` | 329 | 329 | 329 |
| `sec-10k` | 245 | 245 | 245 |
| `fec` | 399 | 347 | 347 |

Three documented exceptions are checked in their own way, not skipped.
One Census cell holds `0` where the page prints `Z` (rounds to zero): the
tool looks for that `Z` on the row's line and in the cell's column. The 52
rows of the four FEC summary units gather the columns of five printed
blocks, so no single line carries them: every one of their values must be
printed somewhere in the document, and their columns are not compared.
And the FEC results print `Total Electoral Votes Needed to Win = 270` as
a sentence under the table: the tool checks that the figure is on that
line and in none of the table's columns.

The first whole-corpus run flagged two rows, neither with a wrong value:
that FEC figure, and a May Treasury total row that held three of the nine
numbers its line prints. The six missing cells were added the same day
and the figure was recorded as an exception, so the table shows the state
after that.

The check started on the same day as a one-off script. Its first run
found three wrong values, all in the June Treasury statement and two of
them in `standalone` cells. A column-by-column comparison of 17 Treasury
units then found one value in the wrong column. All four were corrected,
and the table shows the state after that. The script has since become the
tool in this repository, and it reports each of the four when they are
put back in a copy. As a broader test, one error at a time was planted in
a copy of every unit: a value moved to an empty column, two values
swapped, a cell dropped, a cell added, a digit changed. In the 405
Treasury units the tool reported all 1,897. Over the whole corpus it
reported 2,485 of 2,526; 40 of the 41 it missed are in the OMB tables,
whose rows of 1s and 2s can also be read off a neighbouring line.

The tool does not read labels, and it cannot see a printed row that is
missing from a unit. It is not one of the gates: it needs PDF libraries
the gates do not install and takes about a minute and a half, so an
auditor runs it ([RUNBOOK-auditor.md](RUNBOOK-auditor.md)). The method
and the first findings are in
[AUDIT-2026-11-27.md](AUDIT-2026-11-27.md), the whole-corpus record in
[AUDITS.md](AUDITS.md).

### Tolerances

7,266 of the 10,934 sums close exactly. The other 3,668 carry a nonzero
tolerance equal to the observed difference, each with a `why`. In all but six of
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
    lines sum to 3,034 and the page prints the total as 310. Table 6 on
    page 24 prints 3,248, which is 214 above the sum of the lines and
    2,938 above the printed total. The smaller gap is consistent with
    the differences between the two tables in neighboring months.

  Each of these six sums already sits at its tolerance. Even a one-unit
  change that widens the gap fails. A change that narrows the gap can
  pass. The source checks and audits establish the printed values.
- **4 relations in `bls-cpi/relative-importance-2024-education-other`**
  (tolerance 0.008 to 0.009 on three or four three-decimal components).
  Recorded as rounding, but rounding of the printed digits allows at most
  0.0025. Unresolved.

Percent closures allow ±0.05 by default; 299 of the 589 declare 0.1 or
0.2, each with a `why`.

### Known gaps

- **Column positions.** Compared for the whole corpus on 2026-11-27
  ([above](#what-covers-the-cells-arithmetic-cannot-see)), with nothing
  left open. A unit shipped later is covered once an auditor has run the
  tool on it.
- **Labels.** Row and column labels sometimes use the corpus's wording
  rather than the printed header. The Treasury Table 6 units label
  column 5 with the printed "Beginning of This Month" (checked against
  every page header on 2026-11-27), but the five Table 8 units still
  call the same printed heading "Close of Prior Month", and other
  column labels carry additions the page does not print (a qualifier
  in parentheses, or " — end"). Labels were never checked corpus-wide.
  Join months by position, not by label alone.
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
uv run --group sourcecheck python tools/sourcecheck.py --all   # units against their sources; not a gate
```

Every push to `main` and every pull request runs `pytest` and the full
sweep on GitHub ([.github/workflows/check.yml](.github/workflows/check.yml)).

## License

MIT for code and transcriptions (see [LICENSE](LICENSE)). `sources/`
contains vendored public documents (US government / SEC public filings)
with per-file provenance in `sources/SOURCES.md`.
