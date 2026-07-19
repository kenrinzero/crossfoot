# Crossfoot

An arithmetic-reconciled corpus of public statistical tables: each messy
PDF/HTML table is transcribed into a typed `.cells.json` whose own internal
arithmetic — row totals, subtotals, percent closures, balance identities —
must **reconcile exactly** under `reconcile.py`. The source's redundancy is
the proof: a transcription typo almost always breaks a cross-foot, so
correctness is derived, not trusted.

## Status

Active corpus (2026-07-19): schema + oracle frozen and live (**10/10 tests**;
strict coverage is the default), **341 transcription units shipped**. Census
P60-282 appendix complete; **Treasury MTS June 2026 SOURCE COMPLETE** (Tables
1–9 + Table 5 detail + Table 6 A–E + Tables 7–8); **sec-10k no-vision runway
COMPLETE 11/11** (MSFT FY2025 + Apple FY2023 statement sets, #331–341).
Every-10th different-agent audit cadence **GREEN through #340** (post-audit
repair on #340 recorded in AUDITS.md); next fires at **#350**.


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
