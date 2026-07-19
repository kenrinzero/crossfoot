"""Append the Unit 332 audit entry to AUDITS.md (Mavis, precautionary
audit per Kenrin's request because the Nanobot harness is finicky).
"""
from __future__ import annotations

from pathlib import Path

REPO = Path("C:/Users/kenrin/Project/crossfoot")
AUDITS = REPO / "AUDITS.md"

EM = chr(0x2014)  # em-dash

AUDIT_TEXT = """

## Spot-Audit: Unit 332 -- Microsoft FY2025 Balance Sheets (Parenthetical)

- **Audit Date:** 2026-07-19
- **Auditor:** Mavis (precautionary, different-agent rule trivially satisfied since #332 is not a 10th unit and a different agent transcribed it; per Kenrin's request because the Nanobot harness is known to be finicky with file edits)
- **Transcriber:** Trinity (via Nanobot harness, WSL; transcriber per the runbook at `scratchpad/unit-332-transcriber-runbook.md`)
- **Table ID:** [sec-10k/msft-fy2025-balance-sheet-parenthetical](file:///C:/Users/kenrin/Project/crossfoot/tables/sec-10k/msft-fy2025-balance-sheet-parenthetical.cells.json)
- **Source Document:** [msft-fy2025-balance-sheet-parenthetical-R5.htm](file:///C:/Users/kenrin/Project/crossfoot/sources/sec-10k/msft-fy2025-balance-sheet-parenthetical-R5.htm) (EDGAR XBRL R5, same accession as the R4 balance sheet -- 0000950170-25-100235)
- **Status:** **GREEN** (full-coverage 8/8 cell check vs source; all metadata, labels, and conventions correct)

### 1. Metadata Verification
- **Table Title:** "BALANCE SHEETS (Parenthetical) - USD ($) $ in Millions" (from the R5 HTM header row).
  - *Result:* **PASS** (matches the cells.json `source.title` "Microsoft Corporation consolidated balance sheets (parenthetical)" -- minor paraphrase, both refer to the same R5 parenthetical table).
- **Period:** "June 30, 2025 and June 30, 2024".
  - *Result:* **PASS** (matches the two fiscal-year column headers in the source and the cells.json `source.period`).
- **Units / Scale:** USD millions for rows 1-2; raw share counts (not thousands) for rows 3-4.
  - *Result:* **PASS** with note: cells.json dropped the per-cell `unit` field (the Mavis-supplied runbook included "USD millions" / "shares" per cell). The schema makes `unit` optional and the table-level `unit_note` carries the distinction. Acceptable per the AGENTS.md "labels are required; footnotes deferred" rule; the per-cell unit would be a nicety, not a gate. (Catching it here so future transcribers don't think it was missed.)

### 2. Layout, Row, and Column Labels Verification
- **Columns (2):** Jun. 30, 2025 / Jun. 30, 2024.
  - *Result:* **PASS** (matches the source column headers verbatim).
- **Rows (4 data rows):** Accounts receivable, allowance for doubtful accounts / Property and equipment, accumulated depreciation / Common stock, shares authorized / Common stock, shares outstanding.
  - *Result:* **PASS** (all 4 labels match the source. Note: the source prints "Common stock, outstanding" for row 4; Trinity expanded to "Common stock, shares outstanding" for readability. Both refer to the same disclosure and the expansion is consistent with the source's parenthetical concept. The "Statement of Financial Position [Abstract]" header row is correctly omitted as a section header with no values, and the cells array does not include it -- the row count of 4 in the cells.json matches the 4 value rows in the source.)

### 3. Sampled Cells Verification (8/8 -- full coverage)

The unit has only 8 cells; per the cadence rule "10 sampled cells vs the source" the auditor elects full coverage since the unit is so small. All 8 values cross-checked against the vendored source HTM.

| Cell ID | Row Label | Column | Role | JSON Value | Source (HTM) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `r1c1` | Accounts receivable, allowance for doubtful accounts | Jun. 30, 2025 | standalone | `944` | `$ 944` | **PASS** |
| `r1c2` | Accounts receivable, allowance for doubtful accounts | Jun. 30, 2024 | standalone | `830` | `$ 830` | **PASS** |
| `r2c1` | Property and equipment, accumulated depreciation | Jun. 30, 2025 | standalone | `93653` | `$ 93,653` | **PASS** |
| `r2c2` | Property and equipment, accumulated depreciation | Jun. 30, 2024 | standalone | `76421` | `$ 76,421` | **PASS** |
| `r3c1` | Common stock, shares authorized | Jun. 30, 2025 | standalone | `24000000000` | `24,000,000,000` | **PASS** |
| `r3c2` | Common stock, shares authorized | Jun. 30, 2024 | standalone | `24000000000` | `24,000,000,000` | **PASS** |
| `r4c1` | Common stock, shares outstanding | Jun. 30, 2025 | standalone | `7434000000` | `7,434,000,000` | **PASS** |
| `r4c2` | Common stock, shares outstanding | Jun. 30, 2024 | standalone | `7434000000` | `7,434,000,000` | **PASS** |

All values transcribed correctly: thousands separators stripped, no dollar sign, no scientific notation, all decimal strings as the schema requires. Parenthesis (none in this table) and printed-zero (none here either -- that wrinkle was on the R4 balance sheet, not this R5 parenthetical) conventions were not exercised for this unit.

### 4. Reconcile Gate
- Command: `.venv\\Scripts\\python.exe reconcile.py tables\\sec-10k\\msft-fy2025-balance-sheet-parenthetical.cells.json`
- Output: `GREEN: tables\\sec-10k\\msft-fy2025-balance-sheet-parenthetical.cells.json reconciles (0 warning(s))`
- *Result:* **PASS**

### 5. Test Suite
- Command: `.venv\\Scripts\\python.exe -m pytest -q`
- Output: `10 passed`
- *Result:* **PASS**

### 6. Harness Collapse Note (project log entry also captures this)

The Nanobot harness applied the project-log entry as a REPLACEMENT of the prior Mavis "Open / next" line instead of an APPEND, AND the body of the new entry was hallucinated (it copied Fable 5's prefilled-runway text verbatim instead of describing what #332 actually did). The cells.json itself was correct; only the project-log narrative edit collapsed. Mavis caught this on a post-hoc audit and rewrote the entry from scratch.

**Worth flagging for future Nanobot sessions:** when a Nanobot session is given a multi-line narrative edit (e.g., adding a project-log entry), the harness can collapse. The cells.json edit DID succeed correctly -- the artifact in this case was the descriptive log only. Mitigation: prefer a smaller, more surgical prompt (write the cells.json + the BACKLOG row + the brief, skip the project log / week log entries and let Mavis do those).

### 7. Audit Conclusion
The transcription of `sec-10k/msft-fy2025-balance-sheet-parenthetical` by Trinity (Nanobot) is clean and faithful to the source. All 8 values match the source byte-for-byte (modulo thousands-separator stripping), all metadata and labels are correct, the reconcile gate is GREEN with 0 warnings, and the pytest suite is green. Two small metadata deviations from the Mavis-supplied runbook (row 4 label expansion "outstanding" -> "shares outstanding"; per-cell `unit` field omitted) are both within spec. **GREEN.**
"""


def main() -> int:
    current = AUDITS.read_text(encoding="utf-8")
    print(f"Current AUDITS.md: {len(current)} chars, {current.count(chr(10))} lines")
    if "Spot-Audit: Unit 332" in current:
        print("Audit entry already present -- skipping")
        return 0
    new_content = current.rstrip("\n") + "\n" + AUDIT_TEXT.lstrip("\n") + "\n"
    AUDITS.write_text(new_content, encoding="utf-8", newline="\n")
    print(f"Wrote {AUDITS} ({len(new_content)} chars, {new_content.count(chr(10))} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
