# Census P60-282 Remainder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct the Census appendix inventory, preserve the shipped legacy unit without duplicate work, and advance Table A-2 through source-native percent-distribution slices with an auditable route to corpus #170.

**Architecture:** Treat each Table A-2 unit as one demographic group and one contiguous source-year band. Each row carries the 11 already-settled cells (household count, printed 100 total, and nine income-bracket percentages), two relations (a `sum` targeting the printed 100 and a `percent-closure` over the nine brackets), and one standalone household-count cell. Keep every unit at 13 rows / 143 cells or fewer; exclude the median/mean columns because the shipped seed deliberately scoped the arithmetic-bearing distribution block only.

**Tech Stack:** Python 3.10+, JSON Schema 2020-12, `decimal.Decimal`, `reconcile.py`, `pytest`, PyMuPDF text extraction, pypdfium2 rendering.

## Global Constraints

- `DESIGN.md`, `schema/cells.schema.json`, and `reconcile.py` semantics remain frozen.
- Values are decimal strings; never use binary floats.
- Every A-2 slice is re-read from `sources/census/p60-282.pdf`; no values are copied from another corpus unit.
- Every A-2 slice must reconcile GREEN with zero warnings under strict coverage and meet its manifest relation floor.
- Render verification is mandatory even when the PDF text layer is used for extraction.
- Corpus #170 must be audited by an agent other than its transcriber before later units ship.
- The historical id `census-p60/2023-income-a1` remains unchanged; documentation must identify it as the legacy-named A-2 ALL RACES 2023-2017 slice.

---

## Source inventory

| table | PDF pages | source shape |
|---|---:|---|
| A-1 | 21 | Income summary measures, 2022 and 2023 |
| A-2 | 22-35; footnotes 36 | Income distribution by demographic group and year |
| A-3 | 37 | Money-income and equivalence-adjusted distribution measures |
| A-4a | 38-39 | Household income dispersion time series |
| A-4b | 40-41 | Household income dispersion time series, continued measures |
| A-5 | 42-44 | Equivalence-adjusted income dispersion time series |
| A-6 | 45-46 | Earnings summary measures |
| A-7 | 47-48 | Worker counts, median earnings, and earnings ratio time series |
| B-1 | 51 | Post-tax income summary measures |
| B-2 | 52 | Money-income versus post-tax summary measures |
| B-3 | 53 | Post-tax distribution measures |
| B-4 | 54 | Four-way income distribution comparison |
| B-5 | 55 | Post-tax income dispersion time series |

The source has 13 appendix tables, not the approximately 11 previously stated in `NEXT.md`; A-4a and A-4b were omitted from that queue summary.

## Table A-2 sizing

The arithmetic-bearing block has 459 source rows and 5,049 cells at 11 cells per row. Source-native group splits require 41 total units at the 13-row cap. The already-shipped legacy unit covers the first eight ALL RACES rows, leaving 40 new A-2 units.

| demographic group | years | rows | cells | cap-fit units |
|---|---:|---:|---:|---:|
| ALL RACES | 2023-1967 | 59 | 649 | 5 total; 1 shipped |
| WHITE ALONE | 2023-2002 | 24 | 264 | 2 |
| WHITE (historical definition) | 2001-1967 | 35 | 385 | 3 |
| WHITE ALONE, NOT HISPANIC | 2023-2002 | 24 | 264 | 2 |
| WHITE, NOT HISPANIC (historical definition) | 2001-1972 | 30 | 330 | 3 |
| BLACK ALONE OR IN COMBINATION | 2023-2002 | 24 | 264 | 2 |
| BLACK ALONE | 2023-2002 | 24 | 264 | 2 |
| BLACK (historical definition) | 2001-1967 | 35 | 385 | 3 |
| ASIAN ALONE OR IN COMBINATION | 2023-2002 | 24 | 264 | 2 |
| ASIAN ALONE | 2023-2002 | 24 | 264 | 2 |
| ASIAN AND PACIFIC ISLANDER (historical definition) | 2001-1987 | 15 | 165 | 2 |
| AMERICAN INDIAN AND ALASKA NATIVE ALONE OR IN COMBINATION | 2023-2002 | 24 | 264 | 2 |
| AMERICAN INDIAN AND ALASKA NATIVE ALONE | 2023-2002 | 24 | 264 | 2 |
| AMERICAN INDIAN AND ALASKA NATIVE (historical definition) | 2001-1987 | 15 | 165 | 2 |
| TWO OR MORE RACES | 2023-2002 | 24 | 264 | 2 |
| HISPANIC (ANY RACE) | 2023-1972 | 54 | 594 | 5 |

---

### Task 1: Correct routing and preserve the legacy-id decision

**Files:**
- Create: `plans/census-p60-282-remainder.md`
- Modify: `NEXT.md`
- Modify: `BACKLOG.md`

**Interfaces:**
- Consumes: the frozen design contract and the shipped `census-p60/2023-income-a1` unit.
- Produces: an authoritative 13-table source map and exact A-2 split policy for all later transcription sessions.

- [x] **Step 1: Record the 13-table PDF map and 459-row A-2 sizing in this plan.**

- [x] **Step 2: Correct `BACKLOG.md` so the legacy unit is described as Table A-2, ALL RACES 2023-2017, without renaming its id or file.**

- [x] **Step 3: Replace the vague Census block in `NEXT.md` with the exact source inventory, the 40-unit A-2 remainder, and the #161-170 sequence below.**

- [x] **Step 4: Confirm the routing documents contain A-4a and A-4b and contain no claim that only approximately 11 appendix tables exist.**

Run:

```powershell
rg -n "13 appendix|A-4a|A-4b|40 new A-2|legacy" NEXT.md BACKLOG.md plans/census-p60-282-remainder.md
```

Expected: matches in all three routing artifacts, with the legacy id retained only as a historical identifier.

### Task 2: Ship corpus #161, ALL RACES 2016-2005

**Files:**
- Create: `tables/census-p60/2023-income-a2-all-races-2016-2005.cells.json`
- Modify: `BACKLOG.md`
- Modify: `NEXT.md`

**Interfaces:**
- Consumes: PDF page 22 and the A-2 column/relation convention frozen by the legacy unit.
- Produces: a 143-cell file with 13 rows, 26 relations, and 13 standalone household-count cells.

- [x] **Step 1: Render PDF page 22 upright and visually identify rows 2016 through 2005, including both printed 2013 series rows.**

Run:

```powershell
uv run --with pypdfium2 --with pillow python -c "import pypdfium2 as p; d=p.PdfDocument('sources/census/p60-282.pdf'); d[21].render(scale=2.5).to_pil().rotate(270, expand=True).save('tmp/pdfs/p60-282-p22-upright.png')"
```

Expected: an upright render headed `Table A-2` with 2016-2005 visible in the ALL RACES block.

- [x] **Step 2: Extract the 13 source rows with PyMuPDF and transcribe only household count, printed total, and the nine bracket percentages.**

Run:

```powershell
uv run --with pymupdf python -c "import fitz; t=fitz.open('sources/census/p60-282.pdf')[21].get_text(); print(t[t.index('2016.'):t.index('2004')])"
```

Expected: rows 2016, 2015, 2014, both 2013 series, 2012, 2011, 2010, 2009, 2008, 2007, 2006, and 2005 in print order.

- [x] **Step 3: Create the JSON with 13 `sum` relations targeting each printed 100 and 13 `percent-closure` relations over the nine bracket cells.**

- [x] **Step 4: Run the unit gate.**

Run:

```powershell
uv run python reconcile.py tables/census-p60/2023-income-a2-all-races-2016-2005.cells.json
```

Expected: `GREEN` with `0 warning(s)`.

- [x] **Step 5: Compare all 143 cells against a fresh page-22 extraction and the upright render, then update `BACKLOG.md` and `NEXT.md` as corpus #161.**

### Task 3: Verify and commit the first checkpoint

**Files:**
- Modify: `plans/census-p60-282-remainder.md` checkbox state

**Interfaces:**
- Consumes: Tasks 1-2 outputs.
- Produces: one reviewable commit with authoritative routing plus one source-verified corpus unit.

- [x] **Step 1: Run the harness tests.**

Run:

```powershell
uv run pytest -q
```

Expected: `10 passed`.

- [x] **Step 2: Run the full strict corpus sweep.**

Run:

```powershell
uv run python -c "from pathlib import Path; from reconcile import check; fs=sorted(Path('tables').rglob('*.cells.json')); bad=[(str(f), *check(f)) for f in fs if check(f)[0] or check(f)[1]]; print(f'corpus={len(fs)} non_green={len(bad)}'); print(bad)"
```

Expected: `corpus=161 non_green=0` and `[]`.

- [x] **Step 3: Inspect the complete diff for unintended changes and commit the checkpoint.**

Run:

```powershell
git diff --check
git status --short
git diff --stat
git diff
git add plans/census-p60-282-remainder.md NEXT.md BACKLOG.md tables/census-p60/2023-income-a2-all-races-2016-2005.cells.json
git commit -m "transcribe Census A-2 ALL RACES 2016-2005"
```

Expected: one commit containing only the plan, routing changes, and corpus #161.

### Task 4: Repair public-facing documentation drift

**Files:**
- Modify: `README.md`
- Inspect: `pyproject.toml`

**Interfaces:**
- Consumes: verified corpus #161 state.
- Produces: a current repository status section without changing package metadata unless history proves the package version tracks corpus milestones.

- [x] **Step 1: Replace the stale 25-unit/Table-5 status in `README.md` with the verified 161-unit state and current Census dispatch.**

- [x] **Step 2: Inspect `git log -p -- pyproject.toml`; retain `version = "0.0.1"` because repository history shows it has represented package metadata independently of the Atelier milestone version since the seed.**

- [x] **Step 3: Re-run `uv run pytest -q`, `git diff --check`, and commit the documentation-only change separately.**

Run:

```powershell
uv run pytest -q
git diff --check
git add README.md plans/census-p60-282-remainder.md
git commit -m "docs: refresh Crossfoot corpus status"
```

Expected: tests pass and package metadata remains unchanged unless repository history demonstrates a shared version policy.

### Task 5: Continue A-2 to the #170 audit gate

**Files:**
- Create: nine additional `tables/census-p60/*.cells.json` units
- Modify after each unit: `BACKLOG.md`, `NEXT.md`, and this plan's checkbox state

**Interfaces:**
- Consumes: the verified #161 unit and A-2 split policy.
- Produces: corpus #162-170, stopping before any #171 work until a different-agent audit of #170 is GREEN.

- [ ] **#162:** ALL RACES 2004-1992, 13 rows / 143 cells.
- [ ] **#163:** ALL RACES 1991-1979, 13 rows / 143 cells.
- [ ] **#164:** ALL RACES 1978-1967, 12 rows / 132 cells; ALL RACES complete.
- [ ] **#165:** WHITE ALONE 2023 through the second printed 2013 series row, 13 rows / 143 cells.
- [ ] **#166:** WHITE ALONE 2012-2002, 11 rows / 121 cells; WHITE ALONE complete.
- [ ] **#167:** WHITE historical 2001-1989, 13 rows / 143 cells.
- [ ] **#168:** WHITE historical 1988-1976, 13 rows / 143 cells.
- [ ] **#169:** WHITE historical 1975-1967, 9 rows / 99 cells; historical WHITE complete.
- [ ] **#170:** WHITE ALONE, NOT HISPANIC 2023 through the second printed 2013 series row, 13 rows / 143 cells.
- [ ] **Audit gate:** a different agent performs a render-anchored full-value or stratified non-arithmetic audit of #170 and records it in `AUDITS.md` before #171 ships.
