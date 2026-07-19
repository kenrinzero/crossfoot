"""Surgical edits to NEXT.md, preserving all em-dashes:
1. Remove the NEXT DISPATCH block for #332 (since it shipped)
2. Add the #332 Shipped entry ABOVE the #331 entry
3. Update the #331 entry's text (10 more -> 9 more, since #332 shipped)
"""
from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path("C:/Users/kenrin/Project/crossfoot")
NEXT = REPO / "NEXT.md"


def main() -> int:
    current = NEXT.read_text(encoding="utf-8")
    print(f"Current NEXT.md: {len(current)} chars, {current.count(chr(10))} lines")

    # 1. Remove the NEXT DISPATCH block for #332
    # Find: "## Queue\n\n- **NEXT DISPATCH -- ...balance-sheet-parenthetical"
    # End: right before "- **sec-10k statement-set runway"
    # The block is a multi-line bullet point.

    q_start = current.find("## Queue")
    if q_start == -1:
        print("ERROR: ## Queue not found")
        return 1
    runway_start = current.find("- **sec-10k statement-set runway", q_start)
    if runway_start == -1:
        print("ERROR: runway block start not found")
        return 1
    # The NEXT DISPATCH block runs from after "## Queue\n\n" (or blank line) to
    # just before "- **sec-10k statement-set runway". Let's find the bullet
    # point that starts with "- **NEXT DISPATCH".
    dispatch_start = current.find("- **NEXT DISPATCH", q_start)
    if dispatch_start == -1:
        print("WARNING: NEXT DISPATCH block not found (already removed?)")
    else:
        # Find the end: the blank line before the runway block, or the
        # runway block's bullet start.
        # The NEXT DISPATCH block is a single bullet, so it ends with "\n\n"
        # followed by the next bullet. We'll delete from dispatch_start
        # through the blank line just before the runway.
        # Find the "\n\n" before the runway
        blank_before_runway = current.rfind("\n\n", dispatch_start, runway_start)
        if blank_before_runway == -1:
            print("ERROR: blank line before runway not found")
            return 1
        current = current[:dispatch_start] + current[blank_before_runway + 2:]
        print("Removed NEXT DISPATCH block")

    # Recompute runway_start after the deletion
    runway_start = current.find("- **sec-10k statement-set runway")
    if runway_start == -1:
        print("ERROR: runway block start not found after removal")
        return 1

    # 2. Update the runway header "9 more units after #332" to "8 more units"
    current = current.replace(
        "sec-10k statement-set runway -- 9 more units after #332, ALL HTML",
        "sec-10k statement-set runway -- 8 more units, ALL HTML",
        1,
    )
    print("Updated runway header: 9 -> 8 units")

    # 3. Update the runway count text "Every headline identity in all 9" to "all 8"
    current = current.replace(
        "Every headline identity in all 9 was pre-verified EXACT at vendoring",
        "Every headline identity in all 8 was pre-verified EXACT at vendoring",
        1,
    )
    print("Updated runway count text: 9 -> 8")

    # 4. Add the #332 Shipped entry ABOVE the #331 entry
    # Find: "- 2026-07-19 · **sec-10k no-vision runway STARTED** -- #331"
    shipped_marker = "- 2026-07-19 · **sec-10k no-vision runway STARTED**"
    shipped_idx = current.find(shipped_marker)
    if shipped_idx == -1:
        print("ERROR: shipped #331 marker not found")
        return 1

    trinity_entry = (
        "- 2026-07-19 · **msft-fy2025-balance-sheet-parenthetical** -- #332 "
        "(Trinity, Nanobot harness; Mavis extra audit per Kenrin's request, "
        "AUDITS.md) -- 8c/0r, all standalone, every value single-source; "
        "share counts in whole shares; strict-default GREEN\n"
    )
    current = current[:shipped_idx] + trinity_entry + current[shipped_idx:]
    print("Inserted #332 Shipped entry above #331")

    # 5. Update #331 entry's text: "10 more units queued" -> "9 more units queued"
    current = current.replace(
        "10 more units queued\n  in NEXT.md; next every-10th audit at #340.",
        "9 more units queued\n  in NEXT.md; next every-10th audit at #340.",
        1,
    )
    print("Updated #331 entry: 10 more -> 9 more")

    NEXT.write_text(current, encoding="utf-8", newline="\n")
    print(f"\nWrote {NEXT} ({len(current)} chars, {current.count(chr(10))} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
