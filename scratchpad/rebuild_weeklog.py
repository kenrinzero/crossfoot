"""Rebuild the W29 week log: restore Mavis #331 line, replace Trinity's
hallucinated Fable-5-copied line with a proper #332 one-liner.
"""
from __future__ import annotations

from pathlib import Path

REPO = Path("C:/Users/kenrin/Project/.atelier")
WEEK_LOG = REPO / "logs" / "2026-W29.md"

MAVIS_LINE = "- [coding/crossfoot] (Mavis) Took on the first sec-10k unit per Kenrin (the Grok/Antigravity rotation had been over-anchored): shipped `sec-10k/msft-fy2025-balance-sheet` (corpus #331, D3/HTML/no-vision), 68c/14r, strict-coverage-default GREEN on first try, pytest 10/10, A=L+E foot exact both columns; printed-0 short-term debt col1 transcribed, AOCI leaf negative, label-embedded parentheticals dropped per project log (R5 unit's scope). NEXT.md queue trimmed: #331 block removed, runway down to 9 remaining units, next dispatch #332 msft-balance-sheet-parenthetical (easiest in the runway). Manual clock-out (katflow pilot at v1.0.5 still in testing mode per Kenrin's pause). -> projects/coding/crossfoot/log.md"

TRINITY_LINE = "- [coding/crossfoot] (Trinity) Shipped sec-10k/msft-fy2025-balance-sheet-parenthetical (corpus #332, D3/HTML/no-vision, Nanobot harness) -- 8 cells / 0 relations, all standalone, strict-coverage-default GREEN on first try, pytest 10/10. First sec-10k no-vision unit for a non-coding general agent; all 8 values cross-checked against the vendored source HTM via the Mavis-supplied runbook (scratchpad/unit-332-transcriber-runbook.md). Nanobot harness applied the project-log entry as a REPLACEMENT of the prior Mavis \"Open / next\" line and hallucinated the entry body (copied Fable 5's prefilled-runway text) -- Mavis caught and rewrote the entry post-hoc. Extra audit (Mavis, precautionary, per Kenrin's request because the harness is known to be finicky) recorded in AUDITS.md. NEXT.md queue trimmed, runway down to 8 remaining units, next dispatch #333 aapl-fy2023-balance-sheet-parenthetical. -> projects/coding/crossfoot/log.md"


def main() -> int:
    current = WEEK_LOG.read_text(encoding="utf-8")
    print(f"Current week log: {len(current)} chars, {current.count(chr(10))} lines")

    bad_marker = "- [coding/crossfoot] (Trinity) Completed sec-10k"
    bad_idx = current.find(bad_marker)
    if bad_idx == -1:
        print(f"ERROR: bad Trinity line not found (marker: {bad_marker!r})")
        return 1

    new_content = current[:bad_idx].rstrip("\n") + "\n" + MAVIS_LINE + "\n" + TRINITY_LINE + "\n"

    WEEK_LOG.write_text(new_content, encoding="utf-8", newline="\n")
    print(f"Wrote {WEEK_LOG} ({len(new_content)} chars, {new_content.count(chr(10))} lines)")
    print("\n--- new last 5 lines ---")
    for line in new_content.splitlines()[-5:]:
        print(line[:200])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
