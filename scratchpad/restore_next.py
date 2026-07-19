"""Surgical edits to NEXT.md, preserving em-dashes via chr(0x2014)."""
from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path("C:/Users/kenrin/Project/crossfoot")
NEXT = REPO / "NEXT.md"

# Use chr(0x2014) for em-dash to avoid encoding issues in the .py file
EM = chr(0x2014)  # em-dash


def main() -> int:
    # Restore from HEAD
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
    current = result.stdout
    print(f"Restored from HEAD: {len(current)} chars, {current.count(chr(10))} lines")

    # 1. Remove the NEXT DISPATCH block for #332
    q_start = current.find("## Queue")
    if q_start == -1:
        print("ERROR: ## Queue not found")
        return 1
    runway_start = current.find("- **sec-10k statement-set runway", q_start)
    if runway_start == -1:
        print("ERROR: runway block start not found")
        return 1
    dispatch_start = current.find("- **NEXT DISPATCH", q_start)
    if dispatch_start != -1:
        blank_before_runway = current.rfind("\n\n", dispatch_start, runway_start)
        if blank_before_runway != -1:
            current = current[:dispatch_start] + current[blank_before_runway + 2:]
            print("Removed NEXT DISPATCH block")
        # Recompute runway_start
        runway_start = current.find("- **sec-10k statement-set runway")
    else:
        print("WARNING: NEXT DISPATCH block already removed")

    # 2. Update runway header: "9 more units after #332" -> "8 more units"
    old_header = f"sec-10k statement-set runway {EM} 9 more units after #332, ALL HTML"
    new_header = f"sec-10k statement-set runway {EM} 8 more units, ALL HTML"
    if old_header in current:
        current = current.replace(old_header, new_header, 1)
        print("Updated runway header")
    else:
        print(f"WARNING: runway header not found")

    # 3. Update runway count: "in all 9" -> "in all 8"
    current = current.replace(
        "Every headline identity in all 9 was pre-verified EXACT at vendoring",
        "Every headline identity in all 8 was pre-verified EXACT at vendoring",
        1,
    )
    print("Updated runway count text")

    # 4. Add #332 Shipped entry above #331
    shipped_marker = "- 2026-07-19 · **sec-10k no-vision runway STARTED**"
    shipped_idx = current.find(shipped_marker)
    if shipped_idx == -1:
        print("ERROR: shipped #331 marker not found")
        return 1
    trinity_entry = (
        f"- 2026-07-19 · **msft-fy2025-balance-sheet-parenthetical** {EM} #332 "
        f"(Trinity, Nanobot harness; Mavis extra audit per Kenrin's request, "
        f"AUDITS.md) {EM} 8c/0r, all standalone, every value single-source; "
        f"share counts in whole shares; strict-default GREEN\n"
    )
    current = current[:shipped_idx] + trinity_entry + current[shipped_idx:]
    print("Inserted #332 Shipped entry")

    # 5. Update #331 entry's text: "10 more units queued" -> "9 more units queued"
    current = current.replace(
        "10 more units queued\n  in NEXT.md; next every-10th audit at #340.",
        "9 more units queued\n  in NEXT.md; next every-10th audit at #340.",
        1,
    )
    print("Updated #331 entry count")

    NEXT.write_text(current, encoding="utf-8", newline="\n")
    print(f"\nWrote {NEXT} ({len(current)} chars, {current.count(chr(10))} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
