# Plan — `bls-cpi/relative-importance-2024-special-aggregates`

**Difficulty of the resulting transcription unit: D3** (local-only, HTML —
no vision needed). This document is the frozen relation topology; the
transcription session just types the values (re-read from the source rows
named below), encodes the relations, and drives `reconcile.py` to GREEN.

- **Source:** `sources/bls-cpi/relative-importance-2024.htm`, Table 1
  (2023 Weights), "Relative importance of components in the Consumer Price
  Indexes: U.S. city average, December 2024". Two columns: CPI-U (col 1),
  CPI-W (col 2).
- **Target file:** `tables/bls-cpi/relative-importance-2024-special-aggregates.cells.json`
- **Planned by:** Claude Opus 4.8, 2026-07-14 (D1 relation-plan session).

## The problem this plan solves

The special-aggregates block (source data-rows 295–322, **28 rows / 56
cells**) is not a hierarchy. It is a set of cross-cutting reclassifications
of the same 100.000 total: the Commodities/Services cut, the
Durables/Nondurables cut, and a web of "All items less X" / "Commodities
less X" / "Services less X" / "Nondurables less X" indexes.

The schema has only `sum` and `percent-closure` — **no subtraction**. So
every "less X" index is declared as the identity **`(index) + X = (whole)`**,
which requires the excluded component `X` to be present as a cell. Where `X`
is already in the block (e.g. Energy) no re-anchor is needed; where it is a
main-table component (Food, Shelter, …) it is **re-anchored**: re-read from
the source main table and added as a leaf (never copied from a sibling
unit — CHARTER/AGENTS rule).

## Decisions (the D1 output)

| Decision | Value |
|---|---|
| In-slice rows / cells | 28 rows / 56 cells (source 295–322) |
| Main-table re-anchors | **8** rows / 16 cells (see table) |
| **Total cells** | **72** |
| Size cap | ≤ 120 cells (consistent with sibling BLS units) |
| **Standalone waivers** | **8 cells** (4 rows × 2 cols): Transportation services, Other services, Domestically produced farm food, Utilities and public transportation |
| Relations declared (expected) | **36** (18 identities × 2 columns) |
| **`expected_relations_min` (floor)** | **30** |
| Non-default tolerances | 8 relations at `tol-0.001` (independent 3-d.p. rounding; quote the BLS cost-weights note) |

### The 8 re-anchors (re-read from the source main table)

| local row | source row | label | CPI-U | CPI-W | role | used by |
|---|---|---|---|---|---|---|
| r29 | 3   | Food | 13.691 | 15.166 | leaf | R3, R14 |
| r30 | 94  | Shelter | 35.483 | 33.186 | leaf | R4 |
| r31 | 201 | Medical care | 8.273 | 6.946 | leaf | R5 |
| r32 | 87  | Alcoholic beverages | 0.835 | 0.793 | leaf | R9, R17 |
| r33 | 147 | Apparel | 2.480 | 2.751 | **total** | R18 (target); R15, R16 (source) |
| r34 | 164 | Footwear | 0.578 | 0.700 | leaf | R18 |
| r35 | 207 | Medical care services | 6.747 | 5.628 | leaf | R11 |
| r36 | 108 | Energy services | 3.094 | 3.617 | leaf | R12, R13 |

## Row map (local index → source row → value → role)

Order: the 28 special-aggregate rows keep source order as local r1–r28;
the 8 re-anchors are appended as r29–r36 (table above).

| r | src | label | CPI-U | CPI-W | role |
|---|---|---|---|---|---|
| 1  | 295 | All items | 100.000 | 100.000 | total |
| 2  | 296 | Commodities | 36.201 | 40.085 | total |
| 3  | 297 | Commodities less food and beverages | 21.675 | 24.126 | leaf |
| 4  | 298 | Nondurables less food and beverages | 10.701 | 12.228 | total |
| 5  | 299 | Nondurables less food, beverages, and apparel | 8.221 | 9.477 | leaf |
| 6  | 300 | Durables | 10.974 | 11.898 | leaf |
| 7  | 301 | Services | 63.799 | 59.915 | total |
| 8  | 302 | Rent of shelter | 35.072 | 32.783 | leaf |
| 9  | 303 | Transportation services | 6.305 | 6.848 | **standalone** |
| 10 | 304 | Other services | 10.061 | 8.986 | **standalone** |
| 11 | 305 | All items less food | 86.309 | 84.834 | total |
| 12 | 306 | All items less shelter | 64.517 | 66.814 | leaf |
| 13 | 307 | All items less medical care | 91.727 | 93.054 | leaf |
| 14 | 308 | Commodities less food | 22.511 | 24.919 | total |
| 15 | 309 | Nondurables less food | 11.536 | 13.021 | total |
| 16 | 310 | Nondurables less food and apparel | 9.056 | 10.270 | leaf |
| 17 | 311 | Nondurables | 25.227 | 28.188 | total |
| 18 | 312 | Apparel less footwear | 1.903 | 2.051 | leaf |
| 19 | 313 | Services less rent of shelter | 28.726 | 27.131 | leaf |
| 20 | 314 | Services less medical care services | 57.052 | 54.287 | leaf |
| 21 | 315 | Energy | 6.216 | 7.786 | total |
| 22 | 316 | All items less energy | 93.784 | 92.214 | leaf |
| 23 | 317 | All items less food and energy | 80.094 | 77.048 | leaf |
| 24 | 318 | Commodities less food and energy commodities | 19.388 | 20.750 | leaf |
| 25 | 319 | Energy commodities | 3.122 | 4.169 | leaf |
| 26 | 320 | Services less energy services | 60.705 | 56.298 | leaf |
| 27 | 321 | Domestically produced farm food | 6.795 | 7.632 | **standalone** |
| 28 | 322 | Utilities and public transportation | 7.744 | 8.434 | **standalone** |

## Relations (18 identities → 36 relation objects, one per column)

`tol` column: `.` = exact (default `"0"`), `0.001` = the single-digit
rounding gap. Every `tol-0.001` relation carries the standard BLS
`why`: *"BLS cost-weights page (sources/bls-cpi/relative-importance-cost-weights.htm)
states 'just as with the officially published relative importance, due to
rounding error these weights do not perfectly sum up to the total.'
Components independently rounded to 3 d.p."*

| id | identity | sources → target | tol U | tol W | mand? |
|---|---|---|---|---|---|
| R1  | All items = Commodities + Services | r2,r7 → r1 | . | . | opt |
| R2  | All items = Energy + All items less energy | r21,r22 → r1 | . | . | **mand** |
| R3  | All items = All items less food + Food | r11,r29 → r1 | . | . | opt |
| R4  | All items = All items less shelter + Shelter | r12,r30 → r1 | . | . | **mand** |
| R5  | All items = All items less medical care + Medical care | r13,r31 → r1 | . | . | **mand** |
| R6  | All items less food = All items less food and energy + Energy | r23,r21 → r11 | 0.001 | . | **mand** |
| R7  | Commodities = Durables + Nondurables | r6,r17 → r2 | . | 0.001 | **mand** |
| R8  | Commodities less food = Commodities less food and energy commodities + Energy commodities | r24,r25 → r14 | 0.001 | . | **mand** |
| R9  | Commodities less food = Commodities less food and beverages + Alcoholic beverages | r3,r32 → r14 | 0.001 | . | **mand** |
| R10 | Services = Rent of shelter + Services less rent of shelter | r8,r19 → r7 | 0.001 | 0.001 | **mand** |
| R11 | Services = Services less medical care services + Medical care services | r20,r35 → r7 | . | . | **mand** |
| R12 | Services = Services less energy services + Energy services | r26,r36 → r7 | . | . | **mand** |
| R13 | Energy = Energy commodities + Energy services | r25,r36 → r21 | . | . | opt |
| R14 | Nondurables = Nondurables less food + Food | r15,r29 → r17 | . | 0.001 | opt |
| R15 | Nondurables less food = Nondurables less food and apparel + Apparel | r16,r33 → r15 | . | . | **mand** |
| R16 | Nondurables less food and beverages = Nondurables less food, beverages, and apparel + Apparel | r5,r33 → r4 | . | . | **mand** |
| R17 | Nondurables less food = Nondurables less food and beverages + Alcoholic beverages | r4,r32 → r15 | . | . | opt |
| R18 | Apparel = Apparel less footwear + Footwear | r18,r34 → r33 | 0.001 | . | **mand** |

**Mandatory identities** (sole cover for ≥1 cell): 13 → 26 relation
objects. **Optional** (genuine exact cross-validating identities that
strengthen the proof): R1, R3, R13, R14, R17 → 10 objects. Declaring all
18 gives 36; the `expected_relations_min` floor of **30** forces the 26
mandatory plus at least 4 of the optional.

### Note to carry on R8 / R9 (definitional)

The commodity "less food(/and beverages)" aggregates subtract the **full
published Food (13.691/15.166) and Alcoholic beverages (0.835/0.793)
figures** — not just their commodity portions. Verified by footing in both
columns (e.g. CPI-U: 36.201 − 13.691 − 0.835 = 21.675 = Commodities less
food and beverages; 36.201 − 13.691 = 22.510 ≈ 22.511 Commodities less
food, tol-0.001). Put this in the relation `note` so the D3 transcriber
does not "fix" the apparent cross-classification.

## Standalone `why` strings (4 rows / 8 cells)

- **r9 Transportation services** — cross-cutting service aggregate; its
  complement within Services (private motor-vehicle services + public
  transportation, spread across 4+ main-table rows) is not in this block
  and would require importing unrelated rows with no clean footing.
- **r10 Other services** — diffuse residual service grouping (recreation,
  education & communication, personal-care, and misc services); no in-slice
  or single-component complement.
- **r27 Domestically produced farm food** — a sub-selection of Food
  (excludes imported/processed); no complementary cell exists in the table.
- **r28 Utilities and public transportation** — cross-cut bundle
  (household energy + water/sewer/trash + telephone + public transportation)
  that does not foot against any small in-slice or re-anchor set
  (Fuels and utilities 4.312 + Public transportation 1.468 = 5.780 ≠ 7.744).

## Transcription checklist (the D3 gate)

1. One new file: `tables/bls-cpi/relative-importance-2024-special-aggregates.cells.json`.
2. 72 cells (28 aggregates + 8 re-anchors, ×2 cols), values exactly as
   printed; re-anchors re-read from the named source rows, not copied.
3. 36 relations per the table; 8 at `tol-0.001` with the quoted `why`;
   R8/R9 carry the definitional `note`.
4. 8 standalone cells with the `why` strings above.
5. `uv run python reconcile.py <file>` exits 0, **zero coverage warnings**,
   ≥ 30 relations. `uv run pytest` still 10/10.
6. This is corpus unit #13 — the next spot-audit is due at unit 20.
