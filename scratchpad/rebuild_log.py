"""Rebuild the crossfoot project log from the HEAD version + a correct
Trinity entry appended. Avoids the em-dash encoding trap the Edit tool
hit earlier this session.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path("C:/Users/kenrin/Project/.atelier")
LOG = REPO / "projects" / "coding" / "crossfoot" / "log.md"

TRINITY_ENTRY = """

---

## 2026-07-19 — Trinity (Nanobot harness, audited by Mavis)
**Did:** Shipped `sec-10k/msft-fy2025-balance-sheet-parenthetical` (corpus #332, D3/HTML/no-vision) — 8 cells, 0 relations, all standalone with `why`; strict-coverage-default GREEN on first try, pytest 10/10. Cross-checked all 8 values against the source HTM `sources/sec-10k/msft-fy2025-balance-sheet-parenthetical-R5.htm`: r1c1=944, r1c2=830, r2c1=93653, r2c2=76421, r3c1=24000000000, r3c2=24000000000, r4c1=7434000000, r4c2=7434000000 — all match the source. Used the Mavis-supplied runbook at `scratchpad/unit-332-transcriber-runbook.md` as the structural template.
**Decided:** (a) Two small metadata deviations from the runbook, both within spec: row 4 label expanded from "Common stock, outstanding" to "Common stock, shares outstanding" (slightly more readable, source is informal either way); per-cell `unit` field omitted (the runbook included "USD millions"/"shares" per cell, but the schema makes it optional and the table-level `unit_note` carries the distinction). Both fine per the AGENTS.md "labels are required; footnotes deferred" rule. (b) **Harness collapse flagged for future Nanobot sessions:** the Nanobot edit tool applied the new entry as a REPLACEMENT of the prior Mavis "Open / next" line instead of an APPEND, AND the body of the new entry was hallucinated — it copied Fable 5's prefilled-runway text verbatim instead of describing what #332 actually did. The cells.json itself was correct (the actual file edit DID write the right content); only the project-log narrative edit collapsed. Mavis caught this on a post-hoc audit and rewrote this entry from scratch. Worth flagging so the next Nanobot dispatch either gets a smaller, more surgical prompt or skips the project-log entry entirely.
**Open / next:** NEXT.md queue trimmed (the #332 dispatch block removed; runway shrunk to 8 remaining units — next dispatch is `aapl-fy2023-balance-sheet-parenthetical` #333, the Apple twin of this unit, also 8c/0r all standalone); BACKLOG row flipped QUEUED → SHIPPED; brief.md + INDEX.md updated by Mavis; extra audit added to AUDITS.md per Kenrin's request (not a 10th unit — the audit was precautionary because the harness is known to be finicky). Re-probe MTS July 2026 ~mid-August. Audit cadence: GREEN through #330, #331 + #332 shipped without audits, next fires at #340.
*(Manual audit pass by Mavis post-hoc; Nanobot session itself did not log a stopwatch timing.)*
"""


def main() -> int:
    # Read HEAD version via git show
    result = subprocess.run(
        ["git", "show", "HEAD:projects/coding/crossfoot/log.md"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        print(f"git show failed: {result.stderr}", file=sys.stderr)
        return 1
    head_content = result.stdout

    # The HEAD file already ends with the Mavis "Open / next" line, then a
    # trailing newline. Append the Trinity entry directly.
    new_content = head_content.rstrip("\n") + "\n" + TRINITY_ENTRY.lstrip("\n") + "\n"

    # Sanity: print the last 100 chars to confirm the structure
    print("--- new content last 100 chars ---")
    print(new_content[-100:])

    LOG.write_text(new_content, encoding="utf-8", newline="\n")
    print(f"\nWrote {LOG} ({len(new_content)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
