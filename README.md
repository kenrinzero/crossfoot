# Crossfoot

An arithmetic-reconciled corpus of public statistical tables: each messy
PDF/HTML table is transcribed into a typed `.cells.json` whose own internal
arithmetic — row totals, subtotals, percent closures, balance identities —
must **reconcile exactly** under `reconcile.py`. The source's redundancy is
the proof: a transcription typo almost always breaks a cross-foot, so
correctness is derived, not trusted.

## Status

Active corpus (2026-07-18): schema + oracle frozen and live (**10/10 tests**;
strict coverage is the default), six public-source families vendored, and
**170 transcription units shipped**. Treasury MTS May 2026 (Tables 1-9), the
OMB FY2027 Legislative Branch chapter, BLS 2024 relative importance, and FEC
2024 presidential results are numerically complete. Census P60-282 Table A-2
is the live dispatch family; #161–170 are source-compared and strict-GREEN,
and #170 now awaits its required different-agent audit before #171 can ship.

## How a unit works

```bash
uv venv && uv sync              # once
# read BACKLOG.md -> open sources/<family>/<file> -> write
#   tables/<family>/<table-id>.cells.json  (cells + relations)
uv run python reconcile.py tables/<family>/<table-id>.cells.json
uv run pytest                   # harness self-tests stay green
```

Green + zero coverage warnings + ≥ the manifest's minimum relations = done.
Values are decimal strings (Decimal math — never floats); every total must
be targeted by a relation and every leaf must feed one.

## License

MIT for code and transcriptions. `sources/` contains vendored public
documents (US government / SEC public filings) with per-file provenance in
`sources/SOURCES.md`.
