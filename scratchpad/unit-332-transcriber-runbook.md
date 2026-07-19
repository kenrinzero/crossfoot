# Unit #332 transcriber runbook — `sec-10k/msft-fy2025-balance-sheet-parenthetical`

This is the easiest unit in the sec-10k no-vision runway: 8 cells, 0
relations, 8 standalone waivers. No math, no PDF render check, no
vision. HTML source already vendored and sha256-ledgered. Goal: read
the source, transcribe 4 rows × 2 columns, write one JSON file, run
two gates, commit, push.

If anything below feels wrong, stop and ask Mavis (the orchestrator).
Don't try to "fix" things outside the unit's scope — there are guardrails
on purpose.

---

## What you are writing

ONE new file, and only this file:

```
tables/sec-10k/msft-fy2025-balance-sheet-parenthetical.cells.json
```

This file must NOT exist before you start — if it does, something is
wrong, ask Mavis. If you write it, reconcile.py and pytest must both
go green before you commit.

## The source (already vendored, read it but do NOT edit it)

```
sources/sec-10k/msft-fy2025-balance-sheet-parenthetical-R5.htm
```

The source is 4 data rows × 2 fiscal-year columns (Jun. 30 2025 /
Jun. 30 2024). The "Statement of Financial Position [Abstract]" header
row is a section header with no values — do not transcribe it as a row.

The 4 data rows, exactly as printed:

| # | row label (printed)                                          | col 1 (Jun. 30 2025) | col 2 (Jun. 30 2024) | unit           |
|---|--------------------------------------------------------------|----------------------|----------------------|----------------|
| 1 | Accounts receivable, allowance for doubtful accounts         | 944                  | 830                  | USD millions   |
| 2 | Property and equipment, accumulated depreciation             | 93,653               | 76,421               | USD millions   |
| 3 | Common stock, shares authorized                              | 24,000,000,000       | 24,000,000,000       | shares         |
| 4 | Common stock, outstanding                                    | 7,434,000,000        | 7,434,000,000        | shares         |

Notes:
- All four rows print as raw numbers in the source HTM (`<td class="nump">`). No parentheses, no negative values, no `(**)`, no currency symbol except a `$` prefix that's stripped.
- Rows 1–2 are USD millions; rows 3–4 are raw share counts (not thousands). The unit per cell lives in the cells[].`unit` field.
- Transcribe values as decimal STRINGS exactly as printed (strip thousands separators; keep sign). So r3c1 is `"24000000000"`, NOT `"24,000,000,000"` and NOT `"2.4e10"`.

## Hard "do not" list

If you touch any of these, you will break something:

- `reconcile.py` — frozen contract. Do not edit, do not "improve", do not add flags.
- `schema/cells.schema.json` — frozen.
- `sources/**` — vendored sources are immutable. Do not re-extract, do not curl EDGAR (you'll get 403'd — the SEC requires a contact-formatted User-Agent and the source is already vendored).
- `tables/sec-10k/**` — only write the ONE new file. Do not edit any existing `*.cells.json`.
- `BACKLOG.md`, `NEXT.md`, `AUDITS.md`, `CHANGELOG.md` — bookkeeping, Mavis does those after the unit ships. If you want to be helpful, do them and Mavis will verify; but the safe path is to ship the unit and stop.
- The project log / week log / brief / INDEX under `.atelier/` — Mavis does those, not the transcriber.
- The `scratchpad/` directory is full of other agents' working files. Do not clean it up. Do not commit any of it (everything there is either already committed or untracked WIP from past sessions).

If reconcile.py prints a RED, do not edit reconcile.py. The RED is
your transcription error — re-read the source, fix the cell, re-run.

## Tooling gotchas (these have bitten people before)

- **Use the Write tool, not `Edit` and not `Add-Content` (PowerShell).** The Write tool writes the file byte-exact. `Add-Content` mangles Unicode and joins lines onto the previous one. `Edit` is for targeted replacements; using it to build a new file from scratch is fragile.
- **The Read tool can silently truncate long files.** If the read output feels suspiciously short, verify the actual line count via PowerShell `Get-Content <file> | Measure-Object -Line` before relying on it. The source HTM is short (~120 lines), so this shouldn't bite you here, but worth knowing.
- **Do not pass nontrivial Python via `python.exe -c "..."` on the command line.** PowerShell's parser eats some backslashes before they reach Python. If you need a Python helper script for any reason, write it to a `.py` file with the Write tool and run it via `python.exe <file>.py`. For this unit, you don't need any Python helper — the gates are direct commands.
- **The venv is Windows-side at `.venv\Scripts\python.exe`.** Use the full path; do not assume `python` or `uv` is on PATH.

## Step-by-step

### 1. Read the source

```
sources/sec-10k/msft-fy2025-balance-sheet-parenthetical-R5.htm
```

Confirm the 4 data rows match the table above. If the source has
changed, stop and ask Mavis — the source is supposed to be vendored
and frozen.

### 2. Write the cells.json

Use the Write tool. The exact structure (paste this template, then fill
in the values):

```json
{
  "table_id": "sec-10k/msft-fy2025-balance-sheet-parenthetical",
  "source": {
    "path": "sources/sec-10k/msft-fy2025-balance-sheet-parenthetical-R5.htm",
    "table": "BALANCE SHEETS (Parenthetical)",
    "title": "Microsoft Corporation balance sheets (parenthetical)",
    "period": "June 30, 2025 and June 30, 2024"
  },
  "unit_note": "USD millions for allowance and accumulated depreciation; raw share counts (not thousands) for the two share-count rows. Parenthesized accounting values are transcribed as negatives; thousands separators and currency symbols are stripped.",
  "columns": [
    { "index": 1, "label": "Jun. 30, 2025" },
    { "index": 2, "label": "Jun. 30, 2024" }
  ],
  "rows": [
    { "index": 1, "label": "Accounts receivable, allowance for doubtful accounts" },
    { "index": 2, "label": "Property and equipment, accumulated depreciation" },
    { "index": 3, "label": "Common stock, shares authorized" },
    { "index": 4, "label": "Common stock, outstanding" }
  ],
  "cells": [
    { "id": "r1c1", "row": 1, "col": 1, "value": "944", "role": "standalone", "unit": "USD millions", "why": "Single-source parenthetical disclosure from the balance sheet (R5); not part of any arithmetic relation." },
    { "id": "r1c2", "row": 1, "col": 2, "value": "830", "role": "standalone", "unit": "USD millions", "why": "Single-source parenthetical disclosure from the balance sheet (R5); not part of any arithmetic relation." },
    { "id": "r2c1", "row": 2, "col": 1, "value": "93653", "role": "standalone", "unit": "USD millions", "why": "Single-source parenthetical disclosure from the balance sheet (R5); not part of any arithmetic relation." },
    { "id": "r2c2", "row": 2, "col": 2, "value": "76421", "role": "standalone", "unit": "USD millions", "why": "Single-source parenthetical disclosure from the balance sheet (R5); not part of any arithmetic relation." },
    { "id": "r3c1", "row": 3, "col": 1, "value": "24000000000", "role": "standalone", "unit": "shares", "why": "Single-source share-count disclosure from the balance sheet (R5); not part of any arithmetic relation." },
    { "id": "r3c2", "row": 3, "col": 2, "value": "24000000000", "role": "standalone", "unit": "shares", "why": "Single-source share-count disclosure from the balance sheet (R5); not part of any arithmetic relation." },
    { "id": "r4c1", "row": 4, "col": 1, "value": "7434000000", "role": "standalone", "unit": "shares", "why": "Single-source share-count disclosure from the balance sheet (R5); not part of any arithmetic relation." },
    { "id": "r4c2", "row": 4, "col": 2, "value": "7434000000", "role": "standalone", "unit": "shares", "why": "Single-source share-count disclosure from the balance sheet (R5); not part of any arithmetic relation." }
  ],
  "relations": []
}
```

Things to NOT change in the template:
- `cells[].id` must be `r{row}c{col}` and match `row` / `col` exactly (schema enforces this).
- `cells[].role` must be `"standalone"` for every cell (this unit has no relations).
- `cells[].why` must be a string of at least 8 characters (schema enforces this).
- `cells[].value` must be a decimal string (no `,`, no `$`, no scientific notation).
- `relations` must be the empty array `[]` — no relations, all standalone.

If the Write tool fails with a JSON parse error, the most common cause
is a trailing comma or a missing quote. Re-check.

### 3. Run the gate

From `C:\Users\kenrin\Project\crossfoot`:

```
.venv\Scripts\python.exe reconcile.py tables\sec-10k\msft-fy2025-balance-sheet-parenthetical.cells.json
```

Expected output:

```
GREEN: tables\sec-10k\msft-fy2025-balance-sheet-parenthetical.cells.json reconciles (0 warning(s))
```

If you see `WARN` lines, that's a real issue — read them and fix the
offending cell. If you see `RED`, your transcription is wrong
somewhere. Common causes:
- Trailing comma in the JSON (Write tool rarely does this, but it can happen).
- Mismatched `id` vs `row`/`col` (e.g. `"id": "r1c2"` with `"row": 1, "col": 1`).
- A `value` containing a comma or currency symbol (should be plain digits).
- A `why` shorter than 8 characters.

### 4. Run the test suite

```
.venv\Scripts\python.exe -m pytest -q
```

Expected: `10 passed`. If anything fails, you may have changed
something outside the unit (reconcile.py, schema/, an existing
table) — revert and start over.

### 5. Commit

```
git add tables\sec-10k\msft-fy2025-balance-sheet-parenthetical.cells.json
git commit -m "ship corpus #332: sec-10k/msft-fy2025-balance-sheet-parenthetical (8c/0r, strict-default GREEN; all standalone)"
```

Do not commit anything else. If `git status` shows other modified
files, that's a sign you touched something out of scope — revert them
before committing.

### 6. Push

```
git push origin main
```

PowerShell will print `To https://github.com/kenrinzero/crossfoot.git`
followed by the commit range. The "Command exited with code 1" line is
PowerShell's stderr/stdout interleaving quirk; if the commit range
line printed, the push succeeded.

## After the unit ships

Stop. Tell Mavis (or Kenrin). Mavis will do the bookkeeping:
BACKLOG row QUEUED → SHIPPED, NEXT.md queue trim, project log entry,
week-log one-liner, brief + INDEX update, .atelier commit + push.

If you want to do the bookkeeping yourself, Mavis will verify —
that's fine. But the unit is shipped first, bookkeeping second.

## Common failure modes and what they mean

| Symptom | Likely cause | Fix |
|---|---|---|
| `reconcile.py` exits 0 but pytest fails | You changed reconcile.py or schema/ | Revert; the gates are supposed to be untouched. |
| `reconcile.py` prints `WARN` | Coverage issue — a total cell with no target, or a leaf not feeding any relation | This unit has no totals and no relations, so this should be impossible. If it happens, re-read the JSON — likely a typo in `role`. |
| `reconcile.py` prints `RED` on a sum | N/A for this unit (no relations) | If somehow you added a relation, the math is wrong. |
| `reconcile.py` prints `schema:` error | JSON is malformed (extra comma, missing quote, wrong bracket) | Lint the JSON carefully. |
| `pytest` prints anything other than `10 passed` | You touched a frozen file | Revert your non-unit changes, re-run. |
| `git push` says "rejected" | Someone else pushed to main while you were working | `git pull --rebase origin main`, then push again. If conflicts, stop and ask Mavis. |

## When in doubt

Stop and ask. The unit is small, the cost of an extra 5 minutes is
nothing, the cost of a corrupted schema is a full repo audit. Mavis
will help.
