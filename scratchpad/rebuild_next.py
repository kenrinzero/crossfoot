"""Rebuild NEXT.md from HEAD with two fixes:
1. Remove the duplicate 10-unit runway block (a leftover from the #331
   commit that didn't get cleaned up).
2. Add (Trinity) attribution to the #332 Shipped entry.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path("C:/Users/kenrin/Project/crossfoot")
NEXT = REPO / "NEXT.md"

# The broken section to remove (it was a stale duplicate of the runway
# list that should have been deleted when #331 shipped). Starts with the
# line that has the corrupted leftover header "vision** (vendored..." and
# ends with the end of the runway block (right before "- **D1/web...").
BROKEN_START = "  vision** (vendored + sized 2026-07-19; sha256s in SOURCES.md, specs"
BROKEN_END_LINE = "  re-read, never copied. The every-10th audit fires mid-runway at\n  **#340** -- plan transcriber rotation accordingly."

# Replacement for the Shipped entry (with Trinity attribution and
# audit-cadence note).
OLD_SHIPPED = "- 2026-07-19 · **msft-fy2025-balance-sheet-parenthetical** -- #332\n  (8c/0r, all standalone, every value single-source; share counts in whole shares; strict-default GREEN)"
NEW_SHIPPED = "- 2026-07-19 · **msft-fy2025-balance-sheet-parenthetical** -- #332 (Trinity, Nanobot harness; Mavis extra audit per Kenrin's request, AUDITS.md)\n  (8c/0r, all standalone, every value single-source; share counts in whole shares; strict-default GREEN)"


def main() -> int:
    result = subprocess.run(
        ["git", "show", "HEAD:NEXT.md"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        print(f"git show failed: {result.stderr}")
        return 1
    head = result.stdout

    # Find and remove the broken duplicate block
    bstart = head.find(BROKEN_START)
    if bstart == -1:
        print(f"WARNING: broken duplicate block not found (marker: {BROKEN_START!r})")
    else:
        # Find the end of the runway block: the second "**#340**" line that
        # follows the broken block's start.
        # The broken block ends with the same trailing line as the good one.
        bend_marker = "  re-read, never copied. The every-10th audit fires mid-runway at\n  **#340** -- plan transcriber rotation accordingly."
        # Find the SECOND occurrence of this marker (the first is the good block)
        first = head.find(bend_marker, bstart)
        if first == -1:
            print(f"WARNING: bend marker not found after broken start")
        else:
            # The second occurrence is the end of the broken block
            second = head.find(bend_marker, first + len(bend_marker))
            if second == -1:
                print(f"WARNING: second bend marker not found")
            else:
                # Delete from bstart through the end of the second marker line
                bend = second + len(bend_marker)
                # Trim the trailing newline so we don't have extra blank lines
                while bend < len(head) and head[bend] in "\n":
                    bend += 1
                head = head[:bstart] + head[bend:]
                print(f"Removed broken duplicate block: {bstart}..{bend}")

    # Replace the #332 Shipped entry to add Trinity attribution
    if OLD_SHIPPED in head:
        head = head.replace(OLD_SHIPPED, NEW_SHIPPED, 1)
        print("Added Trinity attribution to #332 Shipped entry")
    else:
        print(f"WARNING: old #332 Shipped not found (looking for: {OLD_SHIPPED[:60]!r}...)")

    NEXT.write_text(head, encoding="utf-8", newline="\n")
    print(f"Wrote {NEXT} ({len(head)} chars, {head.count(chr(10))} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
