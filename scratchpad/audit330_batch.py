import pdfplumber, json
u = json.load(open("tables/treasury-mts/2026-06-table7-receipts-totals.cells.json"))
pdf = pdfplumber.open("sources/treasury-mts/mts-202606.pdf")
page = pdf.pages[u["source"]["page"] - 1]
text = page.extract_text()
for line in text.split("\n"):
    if "Total" in line and ("Receipts" in line or "receipts" in line):
        print(line)
