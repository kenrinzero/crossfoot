# Crossfoot

An arithmetic-reconciled corpus of public statistical tables: each messy
PDF/HTML table is transcribed into a typed `.cells.json` whose own internal
arithmetic — row totals, subtotals, percent closures, balance identities —
must **reconcile exactly** under `reconcile.py`. The source's redundancy is
the proof: a transcription typo almost always breaks a cross-foot, so
correctness is derived, not trusted.

```jsonc
// a cell, and a relation the reconciler re-derives from leaf cells
{ "id": "r15c1", "row": 15, "col": 1, "value": "6274791", "role": "total" }
{ "type": "sum", "sources": ["r1c1", "...", "r14c1"], "target": "r15c1",
  "tol": "2", "why": "Table 8 prints: 'Details may not add to totals due to rounding.'" }
```

All arithmetic runs in exact `Decimal` — never floats. Values are decimal
strings exactly as printed. A tolerance is only legal when the source's own
rounding note is quoted in `why`; strict coverage (every total targeted,
every leaf feeding a relation) is the default gate.

## The corpus

**341 units, all GREEN** (2026-07-19):

| family | source | units |
|---|---|---|
| `treasury-mts` | Monthly Treasury Statement, May + June FY2026 (both months complete: Tables 1–9 incl. full Table 5 outlay detail and Table 6 Schedules A–E) | 165 |
| `census-p60` | Census P60-282 *Income in the United States: 2023* — the complete appendix (A-1…A-7, B-1…B-5) | 91 |
| `omb` | OMB FY2027 Budget Appendix, Legislative Branch chapter — complete (every account with a printed schedule) | 55 |
| `sec-10k` | Apple FY2023 + Microsoft FY2025 10-K statement sets (complete: balance sheet, income, comprehensive income, cash flows, equity, parentheticals) | 12 |
| `fec` | Official 2024 presidential general election results — complete | 11 |
| `bls-cpi` | CPI relative importance of components, Dec 2024 — complete | 7 |

Per-unit specs live in [BACKLOG.md](BACKLOG.md), the authoritative
manifest.

Every vendored source in `sources/` is sha256-ledgered with provenance in
[sources/SOURCES.md](sources/SOURCES.md) — US government material and SEC
public filings, transcribed verbatim, never edited.

## Process

The corpus is transcribed and audited by a rotating fleet of AI agents
(20+ different models to date) under a fixed discipline:

- one session = one unit = one new file, gated by `reconcile.py` GREEN
  with zero coverage warnings ([AGENTS.md](AGENTS.md) has the rules;
  [RUNBOOK-transcriber.md](RUNBOOK-transcriber.md) the session flow);
- every 10th unit gets a **different-agent spot-audit** against the
  source ([RUNBOOK-auditor.md](RUNBOOK-auditor.md)); the full audit
  trail, including the defects the cadence caught, is in
  [AUDITS.md](AUDITS.md);
- PDF units are render-anchored (a vision model must look at the page,
  not just the text layer); HTML units run text-only.

## Running it

```bash
uv venv && uv sync                                     # once
uv run python reconcile.py tables/<family>/<id>.cells.json
uv run pytest                                          # oracle self-tests
for f in tables/*/*.cells.json; do uv run python reconcile.py "$f"; done   # full sweep
```

## License

MIT for code and transcriptions (see [LICENSE](LICENSE)). `sources/`
contains vendored public documents (US government / SEC public filings)
with per-file provenance in `sources/SOURCES.md`.
