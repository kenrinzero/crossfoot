"""Update INDEX.md row for crossfoot to 0.0.41 / 332 units."""
from __future__ import annotations

from pathlib import Path

REPO = Path("C:/Users/kenrin/Project/.atelier")
INDEX = REPO / "INDEX.md"

OLD_ROW = "| Crossfoot | maintained | 0.0.40 | [crossfoot](https://github.com/kenrinzero/crossfoot) (private; Windows working copy) | 2026-07-19 | [brief](projects/coding/crossfoot/brief.md) | 331 units GREEN; June MTS COMPLETE; sec-10k runway started (msft-fy2025-balance-sheet); #340 audit next |"
NEW_ROW = "| Crossfoot | maintained | 0.0.41 | [crossfoot](https://github.com/kenrinzero/crossfoot) (private; Windows working copy) | 2026-07-19 | [brief](projects/coding/crossfoot/brief.md) | 332 units GREEN; sec-10k runway 1/10 (msft-fy2025-balance-sheet + msft-fy2025-balance-sheet-parenthetical); #340 audit next |"


def main() -> int:
    # INDEX.md
    index_content = INDEX.read_text(encoding="utf-8")
    if OLD_ROW in index_content:
        index_content = index_content.replace(OLD_ROW, NEW_ROW, 1)
        INDEX.write_text(index_content, encoding="utf-8", newline="\n")
        print("Updated INDEX.md")
    else:
        print("WARNING: Crossfoot row not found in INDEX.md")

    # brief.md
    BRIEF = REPO / "projects" / "coding" / "crossfoot" / "brief.md"
    brief_content = BRIEF.read_text(encoding="utf-8")

    # Version: 0.0.40 -> 0.0.41, and update the description
    old_version_line = "- **Version:** 0.0.40 (331-unit corpus; June MTS SOURCE COMPLETE + audit-closed; sec-10k no-vision runway started)"
    new_version_line = "- **Version:** 0.0.41 (332-unit corpus; June MTS SOURCE COMPLETE + audit-closed; sec-10k no-vision runway 1/10 -- msft-fy2025-balance-sheet + msft-fy2025-balance-sheet-parenthetical)"
    if old_version_line in brief_content:
        brief_content = brief_content.replace(old_version_line, new_version_line, 1)
        print("Updated version line in brief.md")
    else:
        print(f"WARNING: version line not found in brief.md")

    # Current state: 331 -> 332, 9 more -> 8 more
    brief_content = brief_content.replace(
        "Corpus at 331 strict-GREEN units; main pushed at <pending>.",
        "Corpus at 332 strict-GREEN units; main pushed at <pending>.",
        1,
    )
    brief_content = brief_content.replace(
        "9 more dispatch-ready HTML units remaining in the runway (~450 cells, 7 D3 + 2 D2).",
        "8 more dispatch-ready HTML units remaining in the runway (~450 cells, 6 D3 + 2 D2).",
        1,
    )
    brief_content = brief_content.replace(
        "- [ ] Continue sec-10k no-vision runway per NEXT.md (9 units remaining, audit at #340)",
        "- [ ] Continue sec-10k no-vision runway per NEXT.md (8 units remaining, audit at #340)",
        1,
    )
    print("Updated brief.md counts (331->332, 9->8)")

    BRIEF.write_text(brief_content, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
