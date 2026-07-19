import pdfplumber
pdf = pdfplumber.open("sources/treasury-mts/mts-202606.pdf")
page = pdf.pages[35]
words = page.extract_words()
hdr = [w for w in words if w["top"] < 92]
for w in hdr:
    print(round(w["top"]), round(w["x0"]), w["text"])
