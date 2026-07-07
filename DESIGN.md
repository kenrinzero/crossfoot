# Crossfoot — Design Contract (FROZEN)

> **Status: FROZEN at seed time (2026-07-07).** This document +
> `schema/cells.schema.json` + `reconcile.py`'s check semantics are the
> contract. New relation types, schema changes, and coverage-rule changes
> are explicitly-scoped harness units (T2) — never folded into a
> transcription unit.

Crossfoot turns messy public tables (PDF/HTML) into typed, self-verifying
cell files: each `<source>/<table-id>.cells.json` declares its cells AND
the table's own arithmetic (`relations`), and `reconcile.py` re-derives
every declared total from the leaves — the source's own redundancy is the
proof. A transcription typo almost always breaks a cross-foot.

## 1. Stack & layout

Python ≥ 3.10; runtime dep `jsonschema` only; pytest via uv (dev).

```
schema/cells.schema.json   the frozen cell/relation schema (2020-12)
reconcile.py               the oracle: schema check + relation math + coverage
sources/<family>/...       vendored source documents (verbatim; SOURCES.md ledger)
tables/<family>/<table-id>.cells.json   the corpus (one file per unit)
fixtures/                  harness self-test fixtures (not corpus data)
BACKLOG.md                 the unit manifest
```

## 2. The cell schema (settled)

- **Values are decimal STRINGS** (`"5800.25"`), never JSON floats;
  `reconcile.py` computes in `decimal.Decimal`. "To the penny" is only
  honest without binary floats (locked by a regression fixture).
- Every cell: `id` (`rXcY`), `row`, `col`, `value`, **`role`** ∈
  `leaf | total | standalone`. `standalone` (a number participating in no
  relation) requires a `why` — the anti-under-declaration hook is in the
  schema from day one. Optional `unit` per cell; table-level
  `unit_note`/`scale` for "in millions" style disclosures.
- **Row and column labels are REQUIRED** (v1 schema scope decision):
  cheap to transcribe, and they make the corpus usable. Footnote capture
  is deferred to the Tier-3 second pass.

## 3. Relations v1 (settled)

| type | check | default tol |
|---|---|---|
| `sum` | Σ sources == target | `"0"` (exact) |
| `percent-closure` | Σ sources == `total` (default `"100"`) | `"0.05"` |

Balance identities (assets = liabilities + equity) are `sum` relations.
A non-default `tol` REQUIRES a `why` (e.g. the source's own "may not sum
due to rounding" footnote, quoted). Weighted averages, multi-currency,
nested closure → Tier-4 harness units.

## 4. Coverage (settled design; enforcement staged)

Consistency ≠ completeness — a lazy transcription could under-declare
relations and pass. Two rules, both implemented in `reconcile.py` NOW:

1. every `role: total` cell must be the **target** of ≥ 1 relation;
2. every `role: leaf` cell must appear as a **source** in ≥ 1 relation.

At seed time violations are **warnings**; `--strict-coverage` makes them
errors. The Tier-1 unit flips strict to the default (with a fixture
proving an under-declared table fails). Schema-level `standalone`+`why` is
the pressure valve for genuinely relation-free numbers.

The manifest carries **`expected_relations_min`** (not an exact count —
settled deviation from the plan: exact equality is brittle because
legitimate alternative decompositions exist; a floor plus the coverage
rules gives the same anti-laziness teeth without false rejections).

## 5. Manifest steering policy (settled)

A source qualifies iff **no official machine-readable file of the same
table at the same shape exists**. API-reconstructable data is admissible
only when the published table adds structure the raw feed lacks (margins,
subtotals, presentation hierarchies). Blocklist (grow as found):
Retrosheet/Boxball, FRED series dumps, any agency CSV mirror of the same
table. Bias: 10-K/10-Q financials, Treasury/budget statements, census
report cross-tabs, election returns.

## 6. Spot-audit cadence (settled; Tier 3 formalizes)

Every 10th shipped unit gets a non-arithmetic audit — labels, units,
periods, 10 sampled cell values re-read against the source — by a
**different agent** than the transcriber, logged in `AUDITS.md`. This is
the mitigation for self-consistent errors (transposed non-relation cells,
wrong labels) that arithmetic cannot catch.

## 7. Pre-dispatch verification record (2026-07-07)

- **Sources vendored:** Apple FY2023 10-K consolidated balance sheet
  (EDGAR R5, located via FilingSummary.xml; SEC requires a contact UA);
  Treasury **Monthly Treasury Statement May 2026** (fiscaldata static
  path — the old `fiscal.treasury.gov/files/.../mtsMMYY.pdf` pattern now
  soft-404s to HTML, caught by magic-byte check); Census **P60-282**
  income report PDF. All US-government/public-filing material.
- **BLS is bot-gated** (Akamai 403 to both curl and Windows TLS): the
  plan's `bls-cpi` starter is QUEUED pending browser-assisted vendoring —
  replaced in the starter trio by the Treasury MTS receipts table (same
  "budget appendix" family the plan names). Seeding note: BLS vendoring
  needs Kenrin or a browser-capable session.
- Prior-art re-check waived per Kenrin's 2026-07-07 calibration
  (methodology/fun project).

## 8. Settled decisions (the plan's "Decisions Still Needed")

| Plan decision | Resolution |
|---|---|
| Coverage-enforcement design | § 4 — both rules; warnings now, strict at Tier 1; `standalone`+`why` valve |
| Per-relation tolerances | § 3 — sum exact, percent ±0.05; overrides need quoted `why` |
| Spot-audit cadence | § 6 — every 10th unit, different agent, AUDITS.md |
| Manifest steering policy | § 5 — same-shape rule + blocklist |
| Schema scope v1 | § 2 — labels required; footnotes deferred to Tier 3 |
| (deviation) expected relation count | § 4 — `expected_relations_min` floor instead of exact equality, rationale recorded |

## 9. What the seed shipped vs did not

Shipped: frozen schema, working `reconcile.py` (relations + coverage +
Decimal math), oracle-bites fixtures (green / typo-red / under-declared),
three vendored sources with provenance, the manifest with three starter
units. NOT shipped: any transcription unit (floor work), strict-coverage
default (Tier 1), non-arithmetic second pass (Tier 3).
