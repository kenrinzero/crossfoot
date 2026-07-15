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

**Decision (Kenrin, 2026-07-14): proceed by cap-fit sections.** The 12 remaining
single-unit sections are queued in `NEXT.md` (Judicial p10; Commerce p11; State
p16; Corps of Engineers p18; Other Defense Civil / EPA / EOP / GSA all p19; NASA
/ NSF / OPM / SBA all p20). The 16 over-cap sections + capstone stay deferred.

## Pattern addendum (learned from the flagship, 2026-07-14)

The Legislative flagship shipped at **96 cells / 20 relations** (9 per-column
roll-ups + 11 per-line net identities; 6 rounding tolerances — This-Month
gross/net roll-ups by 2, the Current-FYTD gross and Prior-FYTD net roll-ups by 1,
and two net identities — Senate Current-FYTD, Architect Prior-FYTD — by 1). Two
refinements the flagship surfaced, for every subsequent unit:

1. **Single-source columns can't roll up.** A `sum` relation needs ≥ 2 sources
   (schema). In small sections the Applicable Receipts column often has only one
   line carrying a value (e.g. Judicial: only *Proprietary Receipts* prints an
   applicable), so that column's `Total--` cell has no 2-source roll-up. Cover it
   instead with the **total-row net identity** (next point); do **not** invent a
   second source or leave the total cell uncovered. The flagship dodged this —
   every Legislative column had ≥ 4 line sources — so it is first exercised
   downstream.
2. **The total row obeys the net identity too.** `Total Outlays(net) + Total
   Applicable Receipts = Total Gross Outlays` holds per period (Legislative TM:
   556 + 16 = 572; FYTD 4644 + 38 = 4682; Prior 4755 + 59 = 4814 — all exact).
   Declaring it is optional when the three total cells are already covered by
   their column roll-ups (as in the flagship, which omits it), but it is the
   clean cover for a single-source Applicable total, and a cheap extra check
   otherwise. Where the roll-ups carry rounding tol, the total-row identity is
   usually exact (applicable columns foot exactly), so prefer it as the anchor.

## Over-cap tier sizing — CORRECTED measurement (2026-07-15, Claude Opus 4.8)

The earlier `## Full split scheme` counts (pre-`(**)`-omission estimates) had
two consequential errors, both from a single measurement-script bug that
**merged Social Security Administration + Independent Agencies** into one row:

- **SSA is 81 cells, not 443** — a clean **cap-fit single unit**, not the
  biggest over-cap section. (Hand-verified: 12 value-rows × 6 + 1 total-row × 9
  = 81. Its only structure is two Off-Budget trust-fund sub-totals.)
- **Independent Agencies (page 21) is a real ~305-cell section that the split
  scheme omitted entirely** — it was absorbed into the inflated "SSA 443". It is
  the **actual largest** Table-5 section.

Re-measured every section by bounding on the exact top-level section name and
counting **post-omission real numeric cells** (`......`/`(**)` excluded — the
number that actually gets transcribed). Method: `scratchpad/measure2.py`
(explicit 30-section boundary list; robust against the nested-`:` sub-header
trap that broke the first pass). Total across Table 5 pages 10–22: **3,974 real
cells** (not ~4,247). The corpus's 13 shipped cap-fit units already cover 740 of
these.

### The 30 top-level sections (measured, post-omission)

**Already shipped (13 cap-fit, corpus #14–26):** Legislative 96, Judicial 39,
Commerce 73, State 89, Corps 51, Other Defense Civil 51, EPA 62, EOP 40, GSA 39,
NASA 54, NSF 33, OPM 67, SBA 46.

**Single-unit ceiling raised to ≤ 140 cells** (manifest already has 140/150
caps; splitting a ~130-cell cohesive section into halves is worse than one unit).
Under that rule, **five sections reclassify from over-cap to cap-fit single
units** — ship as-is, no bureau split:

| new unit (proposed) | cells | structure / note |
|---|---:|---|
| `-social-security` | 81 | 2 Off-Budget trust-fund sub-totals (family 3); the only Off-Budget rows in the table besides Postal Service. Prop. Receipts split On-/Off-Budget. |
| `-justice` | 120 | **flat** (no printed bureau subtotals; "Legal Activities"/"Office of Justice Programs" are visual groupings only). At cap. |
| `-homeland-security` | 126 | nested FEMA (`Total--Federal Emergency Management Agency`). cap ≤130. |
| `-energy` | 132 | nested `Total--Energy Programs`; spans p12–13. cap ≤135. |
| `-veterans-affairs` | 139 | nested Benefits Programs (Public Enterprise Funds, Insurance Funds). cap ≤140. |

**Genuinely over-cap (> 140) — sub-split by bureau at printed-subtotal
boundaries.** Each sub-unit is self-contained (its bureau roll-ups foot
internally); a final sub-unit re-anchors the bureau `Total--` rows + the direct
department lines + Proprietary/Intrabudgetary/Offsetting → `Total--Department`
(family 3 + total-row net identity). Re-anchored rows are **re-read from source,
never copied** (the SI-remainder discipline). Exact bureau membership is fixed at
transcription time; target unit counts:

| section | cells | units | natural split boundaries |
|---|---:|---:|---|
| Education | 161 | 2 | Office of Elem/Secondary + Special Ed + Postsecondary  ‖  Federal Student Aid (77) + direct + capstone |
| International Assistance | 165 | 2 | Int'l Security Assistance + Multilateral + AID  ‖  Military Sales + OPIC + Peace Corps + Millennium + IMF + capstone |
| Interior | 171 | 2 | Land&Minerals + Water&Science + Fish&Wildlife  ‖  Indian Affairs + Departmental Offices (65) + direct + capstone |
| Transportation | 176 | 2 | FAA (Airport&Airway TF nested) + Office of Secretary  ‖  FHWA + FMCSA + NHTSA + FRA + FTA + Maritime + capstone |
| Labor | 180 | 2 | Employment&Training (Unemployment TF nested, 95)  ‖  PBGC + Workers' Comp (85) + the small bureaus + capstone |
| HUD | 204 | 2 | Public&Indian Housing + Community Planning  ‖  Housing Programs (Credit Accounts 71) + GNMA + Mgmt + Prop + capstone |
| UOR (Undistributed Offsetting Receipts) | 209 | 2 | Employer Share, Employee Retirement (Total—) ‖ Interest Received by Trust Funds (Total—) + Rents/Royalties + Sale of Assets + section total. All negatives; deep agency nesting. |
| Treasury | 235 | 3 | Departmental Offices + Fiscal Service + ATTTB + BEP + Mint  ‖  IRS (79, nested)  ‖  Interest on Public Debt + Comptroller + FFB + direct + capstone |
| HHS | 252 | 3 | CMS (96, deeply nested: Hospital & Supplementary Medical Insurance TF totals)  ‖  Admin for Children & Families (96) + smaller agencies  ‖  direct + Prop (17,024!) + Intrabudgetary + capstone |
| Agriculture | 271 | 3 | Food & Nutrition Service + Forest Service (both `Total--`)  ‖  Farm Service Agency (`Total--`) + NRCS + Rural Dev/Housing/Utilities + Foreign Ag  ‖  Research + NIFA + APHIS + Food Safety + Ag Marketing + Risk Mgmt + "Other"(6245) + Prop + Intra + capstone |
| Defense–Military | 271 | 3 | splits cleanly by appropriation category, each with a printed `Total--`: Military Personnel + O&M + Procurement  ‖  RDT&E + Military Construction + Family Housing + Revolving  ‖  Trust Funds + Proprietary(by service) + Intrabudgetary(by service) + Offsetting + capstone |
| Independent Agencies | 305 | 3 | Railroad Retirement Board (heavily nested, `Total--RRB`) + FDIC + FCC + Postal Service(off-budget) + District of Columbia  ‖  TVA + NCUA + SEC + the mid agencies  ‖  the ~15 flat small agencies + "Other" + `Total--Independent Agencies` (capstone). Header row "Independent Agencies" is all `......` (dropped). |

That is **12 over-cap sections → ~28 sub-units** + **5 reclassified cap-fit
single units** + **1 grand capstone** = **~34 remaining units** (the earlier
"~35–45" over-estimate reflected the SSA inflation).

### Grand capstone decision

`Total Outlays` / `Total On-Budget` / `Total Off-Budget` (page 22) = **3 rows ×
9 cols = 27 cells** (`Total Surplus (+)/Deficit (-)` stays **out of scope** — it
references Table 4 receipts). Two self-contained identity families, **no
re-anchoring**:
- **On-/Off-Budget split:** `On-Budget + Off-Budget = Total Outlays` for each of
  9 columns → 9 relations (verified net TM: 490,896 + 137,265 = 628,161).
- **Total-row net identity:** `net + applicable = gross` for each of the 3 total
  rows × 3 periods → 9 relations.

→ **27 cells, 18 relations, self-verifying, cap-fit.** Ship as
`-grand-total-capstone`.

The *full* grand-sum (`Total Outlays = Σ all 30 section `Total--` rows` per
column) would re-anchor 30 total rows = 270 cells → a 3-part re-anchor unit, for
marginal added assurance since every section already self-verifies. **Deferred as
an optional later tier** (`-grand-sum-*`), not blocking. Flag for Kenrin: worth
it only if the table-wide cross-foot is wanted as a capstone showcase.

### Sequencing (this tier)

1. **Reclassified cap-fit single units first** (cheapest, highest value — they
   convert a sizing error into shipped corpus): `-social-security` (81),
   `-justice` (120), `-homeland-security` (126), `-energy` (132),
   `-veterans-affairs` (139). Corpus #27–31.
2. **Grand capstone** `-grand-total-capstone` (27 cells) — small, and it locks
   the On/Off-Budget structure early.
3. **Over-cap sub-units**, ascending section size: Education, Int'l Assistance,
   Interior, Transportation, Labor, HUD, UOR, Treasury, HHS, Agriculture,
   Defense–Military, Independent Agencies.

Spot-audit falls due at **unit 30** (`-homeland-security` under this sequence) —
different agent, per DESIGN §6.
