"""Unit-110 audit render: independent re-render of PDF page 36 + positioned text dump.

Auditor: Kimi. Does NOT overwrite the transcriber's staged files.
"""
import pypdfium2 as pdfium
import pdfplumber
from pathlib import Path

SRC = Path("sources/omb/budget-2027-app-2-3-legislative.pdf")
OUT = Path("scratchpad/audit-110-p36-render.png")
TXT = Path("scratchpad/audit-110-p36-words.txt")
PAGE_INDEX = 35  # PDF page 36 (0-based)

pdf = pdfium.PdfDocument(str(SRC))
page = pdf[PAGE_INDEX]
bitmap = page.render(scale=3.0)
pil = bitmap.to_pil()
pil.save(str(OUT))
print(f"render saved: {OUT} size={pil.size}")

with pdfplumber.open(str(SRC)) as pl:
    p = pl.pages[PAGE_INDEX]
    print(f"page size: {p.width} x {p.height}")
    words = p.extract_words(use_text_flow=False, keep_blank_chars=False)
    with TXT.open("w", encoding="utf-8") as f:
        for w in words:
            f.write(f"{w['top']:7.1f} {w['x0']:7.1f} {w['x1']:7.1f}  {w['text']}\n")
    print(f"words saved: {TXT} ({len(words)} words)")
