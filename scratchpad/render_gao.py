import pdfplumber, pypdfium2 as pdfium
PDF = "sources/omb/budget-2027-app-2-3-legislative.pdf"
with pdfplumber.open(PDF) as pdf:
    for p0 in (26, 27, 28, 29):  # PDF pages 27,28,29,30
        txt = pdf.pages[p0].extract_text() or ""
        open(f"scratchpad/gao-p{p0+1}-text.txt","w",encoding="utf-8").write(txt)
doc = pdfium.PdfDocument(PDF)
for p0 in (27, 28):  # render pages 28, 29 (where GAO id 005-0107 lives)
    doc[p0].render(scale=3.0).to_pil().save(f"scratchpad/gao-p{p0+1}-render.png")
print("OK")
