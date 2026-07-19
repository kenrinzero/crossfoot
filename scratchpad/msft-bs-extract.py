"""Independent source cross-check for MSFT FY2025 balance sheet (R4).

Reads sources/sec-10k/msft-fy2025-balance-sheet-R4.htm and prints the
(row-label, col1, col2) tuples in source order, so the transcriber can
verify each value against the cells.json being built. Skips header/section
rows (no value) and the "Commitments and contingencies" row (also no
value). Numbers are emitted as the printed string for direct comparison
(strips the dollar sign, thousands commas, and surrounding whitespace,
preserves the ASCII hyphen-minus for negative values, since the source
uses parentheses — those need to be unwrapped to '-').

This is a one-shot scratch script for unit #331. Lives in scratchpad/;
not part of the corpus.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "sources" / "sec-10k" / "msft-fy2025-balance-sheet-R4.htm"

# regex: a "row data" tr has a nump/num cell per column
TR_RE = re.compile(r'<tr[^>]*>\s*<td class="pl"[^>]*>(.*?)</td>\s*<td class="(?:nump|num)">(.*?)</td>\s*<td class="(?:nump|num)">(.*?)</td>\s*</tr>', re.S)
LABEL_RE = re.compile(r'<a[^>]*>(.*?)</a>', re.S)
NUM_CLEAN_RE = re.compile(r'[^\d\.\-]')


def clean(s: str) -> str:
    """Strip $ and , and whitespace; unwrap parenthesized negatives to '-'."""
    s = s.strip()
    if s.startswith('(') and s.endswith(')'):
        inner = NUM_CLEAN_RE.sub('', s[1:-1])
        return f'-{inner}'
    return NUM_CLEAN_RE.sub('', s)


def main() -> int:
    text = SOURCE.read_text(encoding='utf-8')
    rows = TR_RE.findall(text)
    out: list[tuple[str, str, str]] = []
    for raw_label, raw_c1, raw_c2 in rows:
        m = LABEL_RE.search(raw_label)
        label = m.group(1) if m else raw_label
        label = re.sub(r'\s+', ' ', label).strip()
        c1 = clean(raw_c1)
        c2 = clean(raw_c2)
        out.append((label, c1, c2))

    for i, (label, c1, c2) in enumerate(out, start=1):
        print(f'r{i:>2}  c1={c1:>12}  c2={c2:>12}  | {label}')

    print(f'\n{len(out)} value rows (excludes the 4 header/divider rows + Commitments & contingencies)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
