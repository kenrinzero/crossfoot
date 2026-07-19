import pdfplumber, pypdfium2 as pdfium

PDF = "sources/omb/budget-2027-app-2-3-legislative.pdf"
PAGE0 = 29  # 0-based -> PDF page 30

with pdfplumber.open(PDF) as pdf:
    pg = pdf.pages[PAGE0]
    txt = pg.extract_text() or ""
    open("scratchpad/omb-p30-text.txt","w",encoding="utf-8").write(txt)
    # also dump words with x positions for column disambiguation
    words = pg.extract_words(use_text_flow=False, keep_blank_chars=False)
    with open("scratchpad/omb-p30-words.txt","w",encoding="utf-8") as f:
        for w in words:
            f.write(f"{w['x0']:7.1f} {w['x1']:7.1f} {w['top']:7.1f}  {w['text']}\n")

pdf = pdfium.PdfDocument(PDF)
page = pdf[PAGE0]
bmp = page.render(scale=4.0)
pil = bmp.to_pil()
W, H = pil.size
pil.crop((0, int(0.55*H), int(0.52*W), H)).save("scratchpad/omb-p30-sa-left.png")
pil.crop((int(0.5*W), 0, W, int(0.64*H))).save("scratchpad/omb-p30-sa-right.png")
print("OK", W, H)
