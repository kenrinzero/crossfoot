# Plan — Treasury MTS May 2026, Table 5 (Outlays) sizing + extraction pattern

**D2 sizing session, 2026-07-14 (Claude Opus 4.8).** Source:
`sources/treasury-mts/mts-202605.pdf`, **Table 5. Outlays of the U.S.
Government, May 2026 and Other Periods** (pages 10–23). This doc sizes the
table, fixes the column model and conventions for the whole family, records
the full split scheme, and specs the **flagship** first unit. Coverage
decision (Kenrin, 2026-07-14): **flagship first, then reassess**; column
decision: **full 9 columns** (structural parity with the Table-4 receipts
units from the same statement).

## Scale finding (why this is not one unit)

Table 5 is an order of magnitude larger than Table 4 (receipts, ~250 cells /
4 units):

- **~4,247 numeric cells** across **662 rows** in **29 top-level sections**
  (28 departments/agencies + Undistributed Offsetting Receipts), pages 10–23.
- **9 columns**: 3 periods (This Month · Current FYTD · Prior FYTD) ×
  (Gross Outlays, Applicable Receipts, Net Outlays).
- At full-9 fidelity the whole table is **~35–45 transcription units** — a
  sustained program, hence phased. This session commits only to the flagship.

## Column model (all Table-5 units)

Columns c1–c9, fixed:

| c | period | measure |
|---|---|---|
| 1 | This Month | Gross Outlays |
| 2 | This Month | Applicable Receipts |
| 3 | This Month | Net Outlays |
| 4 | Current FYTD | Gross Outlays |
| 5 | Current FYTD | Applicable Receipts |
| 6 | Current FYTD | Net Outlays |
| 7 | Prior FYTD | Gross Outlays |
| 8 | Prior FYTD | Applicable Receipts |
| 9 | Prior FYTD | Net Outlays |

## Relation families (all Table-5 units)

1. **Per-line net identity** — where a line prints an Applicable Receipts
   value, `Net + Applicable = Gross` for that period, i.e. `sum([net, applicable]) → gross`.
   (Skip where Applicable is omitted; the line's Gross and Net are then equal
   and are each still covered by the column roll-ups below.)
2. **Per-column roll-up** — for each of the 9 columns, the section/bureau
   subtotal (`Total--X`) is the sum of that column's line values:
   `sum([line c_k …]) → Total_X c_k`.
3. **Department total** — where bureaus nest (e.g. Farm Service Agency inside
   Agriculture), the bureau `Total--` cells roll up into the department
   `Total--` per column.
4. **Grand total (capstone unit)** — `Total Outlays` per column = Σ department
   `Total--` nets/grosses/applicables; plus `Total On-Budget + Total Off-Budget
   = Total Outlays` per column (verified: 490,896 + 137,265 = 628,161 net TM).
   `Total Surplus/Deficit` is **out of scope** — it references Table 4 receipts.

## Conventions (settled here — first Table-5 unit sets them)

- **`(**)` (Treasury "$500,000 or less") is OMITTED**, like `......`. It is
  not a valid decimal string and is below the table's $1M rounding precision;
  its <0.5 contribution is absorbed by the relation tolerance. Document this in
  each unit's `unit_note`. A row whose only values are `(**)`/`......` is
  dropped entirely (e.g. Legislative "Offsetting Governmental Receipts").
- **`......` (No Transactions)** — omitted, never zero (existing convention).
- **Negatives** transcribed as printed with a leading `-` (Table 5 has many:
  Military Retirement Fund, Proprietary Receipts, Intrabudgetary, the whole
  Undistributed Offsetting Receipts section).
- **Tolerance** — Table-5 roll-ups sum many independently-rounded integers, so
  gaps of ±1 to ±3 are normal. Set `tol` to the **observed** gap and quote the
  MTS note: *"Note: Details may not add to totals due to rounding."* (printed
  on each Table-5 page). Never invent slack; if a total misses by more than
  rounding can explain and the page gives no reason, STOP and log it.
- **PDF discipline** — vision-capable agent required: render the page(s) with
  pypdfium2 and verify against the `(cid:NN)`→`chr(NN+29)`-decoded text layer
  (footnote markers can glue onto values, as in the receipts slices).

## Full split scheme (recorded for the deferred program)

One unit per section; the 16 over-cap sections sub-split by bureau at their own
transcription time. **Cap-fit as single units** (≈cells): Legislative (96),
State (95), Commerce (78), OPM (70), EPA (62), Other Defense Civil (58), NASA
(57), SBA (54), Corps of Engineers (53), EOP (46), Judicial (41), GSA (39), NSF
(33). **Over ≤120 cap → sub-split by bureau**: Social Security Admin (443),
Agriculture (284), Defense–Military (284), Undistributed Offsetting Receipts
(278), HHS (252), Treasury (251), HUD (229), Labor (182), Transportation (181),
Interior (177), Int'l Assistance (175), Education (173), VA (163), Energy (139),
Homeland Security (126), Justice (123). Plus one **capstone** grand-total unit
(Total Outlays + On/Off-Budget, re-anchoring the 28 section totals). Cell
counts are pre-`(**)`-omission estimates; expect a few % lower.

## FLAGSHIP unit (queued now) — `treasury-mts/2026-05-outlays-legislative`

**Legislative Branch**, page 10, self-contained. Exercises every part of the
pattern: applicable-receipts net identities, negatives, `(**)`/`......`
omission, and a single-level department roll-up.

- **Rows (13 data + 1 total; re-read values from the PDF, never copy):**
  Senate, House of Representatives, Joint Items, Capitol Police, Congressional
  Budget Office, Architect of the Capitol, Library of Congress, Government
  Publishing Office, Government Accountability Office, United States Tax Court,
  Other Legislative Branch Agencies, Proprietary Receipts from the Public,
  Intrabudgetary Transactions, **Total--Legislative Branch**. (Drop "Offsetting
  Governmental Receipts" — only `(**)`/`......`.)
- **Size:** ≈**96 cells** (after `(**)` omission), full 9 columns.
- **Relations:** 9 per-column roll-ups into Total--Legislative Branch + net
  identities on the lines that print Applicable Receipts (House, Architect,
  Library) → **≈18 relations**. Applicable-column roll-ups (c2/c5/c8) and the
  Current/Prior net columns foot exactly; the This-Month gross/net totals miss
  by ~2 and two FYTD grosses by ~1 → `tol` quoting the MTS rounding note.
- **Manifest params:** `min relations 14`, `size cap ≤120 (≈96 sized)`,
  `standalone waivers 0`, type `sum`, **difficulty D2** (first-of-family, PDF →
  vision agent).
- **Gate:** `uv run python reconcile.py <file>` exit 0, zero coverage
  warnings, ≥14 relations; `uv run pytest` 10/10. Corpus unit #14.

## After the flagship

Reassess with Kenrin: continue by cap-fit sections (cheap), commit to the full
~40-unit program, or stop at a marquee subset. The pattern + conventions above
carry to every subsequent Table-5 unit.
