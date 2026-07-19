import pdfplumber, json
pdf = pdfplumber.open("sources/treasury-mts/mts-202606.pdf")
page = pdf.pages[35]  # PDF page 36
print("=== RAW TEXT PAGE 36 ===")
print(page.extract_text())
