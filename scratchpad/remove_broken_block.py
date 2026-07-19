"""Remove the broken 10-unit duplicate runway block from NEXT.md.

The HEAD has a 9-unit runway block followed by a leftover 10-unit block
(same content but with msft-paren included). This script removes the
10-unit block.
"""
from __future__ import annotations

from pathlib import Path

REPO = Path("C:/Users/kenrin/Project/crossfoot")
NEXT = REPO / "NEXT.md"


def main() -> int:
    current = NEXT.read_text(encoding="utf-8")
    lines = current.splitlines(keepends=True)
    print(f"Current NEXT.md: {len(lines)} lines")

    # Find the broken block: starts at the first "  vision**" line
    # (the tail of "no vision**" from the prior line getting
    # concatenated) and ends at the line containing "  **#340**" plus
    # an em-dash.

    start_idx = None
    for i, line in enumerate(lines):
        if line.startswith("  vision**"):
            start_idx = i
            break
    if start_idx is None:
        print("ERROR: broken block start not found")
        return 1
    print(f"Broken block starts at line {start_idx + 1}")

    end_idx = None
    for i in range(start_idx, len(lines)):
        if "  **#340**" in lines[i]:
            end_idx = i
            break
    if end_idx is None:
        print("ERROR: broken block end not found")
        return 1
    print(f"Broken block ends at line {end_idx + 1}")

    # Delete from start_idx to end_idx+1 (inclusive of the end line)
    delete_until = end_idx + 1
    # Also remove the blank line after, if present
    if delete_until < len(lines) and lines[delete_until].strip() == "":
        delete_until += 1
        print(f"Also removing trailing blank line")

    print(f"\nDeleting lines {start_idx + 1}..{delete_until}")
    new_lines = lines[:start_idx] + lines[delete_until:]
    new_content = "".join(new_lines)
    NEXT.write_text(new_content, encoding="utf-8", newline="\n")
    print(f"Wrote {NEXT} ({len(new_content)} chars, {len(new_lines)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
