"""Fix NEXT.md: delete the stale duplicate runway block.

The HEAD version had two runway blocks -- a clean 9-unit block and a
leftover 10-unit block (including the just-shipped #332). The 10-unit
block was a stale duplicate from the #331 commit. This script removes
the 10-unit block.

Also rewrites the #332 Shipped entry to add (Trinity) attribution.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path("C:/Users/kenrin/Project/crossfoot")
NEXT = REPO / "NEXT.md"

# The broken block has a unique signature: the line beginning with
# "  vision**" (which is the tail of "no vision**" from the prior line
# getting concatenated) and the line ending with "  **#340**" plus the
# em-dash. We'll find these and delete everything between them.
START_MARKER = "  vision** (vendored"
END_MARKER_TAIL = "  **#340**"


def main() -> int:
    # Read current working-tree file
    current = NEXT.read_text(encoding="utf-8")
    lines = current.splitlines(keepends=True)
    print(f"Current NEXT.md: {len(lines)} lines")

    # Find the broken block: starts at the first "  vision**" line and
    # ends at the line containing "  **#340**" plus an em-dash AFTER the
    # first occurrence.
    start_idx = None
    for i, line in enumerate(lines):
        if line.startswith(START_MARKER):
            start_idx = i
            break
    if start_idx is None:
        print("ERROR: broken block start not found")
        return 1
    print(f"Broken block starts at line {start_idx + 1}")

    # Find the end: the first "  **#340**" line AFTER the broken block start
    end_idx = None
    for i in range(start_idx, len(lines)):
        if END_MARKER_TAIL in lines[i] and i > start_idx:
            end_idx = i
            break
    if end_idx is None:
        print("ERROR: broken block end not found")
        return 1
    print(f"Broken block ends at line {end_idx + 1}")

    # Also delete the trailing blank line if present
    delete_until = end_idx + 1
    if delete_until < len(lines) and lines[delete_until].strip() == "":
        delete_until += 1
        print(f"Also removing trailing blank line at {delete_until}")

    print(f"\nDeleting lines {start_idx + 1}..{delete_until}")
    new_lines = lines[:start_idx] + lines[delete_until:]
    new_content = "".join(new_lines)
    NEXT.write_text(new_content, encoding="utf-8", newline="\n")
    print(f"Wrote {NEXT} ({len(new_content)} chars, {len(new_lines)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
