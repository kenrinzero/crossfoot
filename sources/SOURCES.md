# sources/ — provenance ledger

Vendored verbatim 2026-07-07 so transcription units run with local files
only. US-government material is public domain; SEC filings are public
records. Never edit vendored files; discrepancies are findings.

| file | bytes | origin | sha256 |
|---|---|---|---|
| `sources/sec-10k/aapl-fy2023-balance-sheet-R5.htm` | 119221 | EDGAR: sec.gov/Archives/edgar/data/320193/000032019323000106/R5.htm (Apple FY2023 10-K, Consolidated Balance Sheets; located via FilingSummary.xml; SEC requires a contact User-Agent) | `a4365d58313587a6f994c152dd3c2c8ee57cec854fc7c5ffc6cce52ebdef15d5` |
| `sources/treasury-mts/mts-202605.pdf` | 1989172 | fiscaldata.treasury.gov/static-data/published-reports/mts/MonthlyTreasuryStatement_202605.pdf (May FY2026 MTS; the old fiscal.treasury.gov path now soft-404s to HTML — verify %PDF magic when re-vendoring) | `8ffa9e6f8d1ab0fc53efb484e43254190fcb91fee65c94982d7f484cfd2c4450` |
| `sources/census/p60-282.pdf` | 1890167 | www2.census.gov/library/publications/2024/demo/p60-282.pdf (Income in the United States: 2023, P60-282) | `e6cf145cb10b5d037f5e77fa199d2e558bfe24f76273f385e9767c2eabba1cbf` |

**bls-cpi/** is empty: bls.gov is bot-gated (Akamai; 403 to curl AND
Windows TLS, verified 2026-07-07) — vendoring queued for a
browser-capable session or Kenrin (BACKLOG.md).
