import pdfplumber, json, re
from decimal import Decimal

unit = json.load(open("tables/treasury-mts/2026-06-table8-investments.cells.json"))
pdf = pdfplumber.open("sources/treasury-mts/mts-202606.pdf")
page = pdf.pages[35]
text = page.extract_text()

# Expected: last 3 numeric tokens of each trust line = investment columns
expected_rows = {
 "Airport and Airway": 1, "Federal Disability Insurance": 2,
 "Federal Employees Life and Health": 3, "Federal Employees Retirement": 4,
 "Federal Hospital Insurance": 5, "Federal Old-Age and Survivors Insurance": 6,
 "Federal Supplementary Medical Insurance": 7, "Hazardous Substance Superfund": 8,
 "Highways": 9, "Military Retirement": 10, "Railroad Retirement": 11,
 "Unemployment": 12, "Veterans Life Insurance": 13, "All Other Trust": 14,
}
cells = {(c["row"], c["col"]): c["value"] for c in unit["cells"]}
mismatch = 0
checked = 0
for line in text.split("\n"):
    for label, ridx in expected_rows.items():
        if line.startswith(label + " "):
            nums = re.findall(r"-?[\d,]+", line[len(label):])
            inv = [n.replace(",", "") for n in nums[-3:]]
            for ci, v in enumerate(inv, 1):
                got = cells[(ridx, ci)]
                ok = got == v
                checked += 1
                if not ok:
                    mismatch += 1
                    print(f"MISMATCH r{ridx}c{ci}: unit={got} pdf={v}")
# Total row wraps to next line ("Held from Table 6-D ...")
for line in text.split("\n"):
    if line.startswith("Held from Table 6-D"):
        nums = [n.replace(",", "") for n in re.findall(r"-?[\d,]+", line)]
        # skip the '6' and '-D' fragments: filter len>=3 from tail
        inv = nums[-3:]
        for ci, v in enumerate(inv, 1):
            got = cells[(15, ci)]
            checked += 1
            if got != v:
                mismatch += 1
                print(f"MISMATCH r15c{ci}: unit={got} pdf={v}")
print(f"value check: {checked} checked, {mismatch} mismatches")
assert checked == 45, checked

# Relations recompute
for r in unit["relations"]:
    s = sum(Decimal(cells[[c for c in unit['cells'] if c['id']==sid][0]['row'], [c for c in unit['cells'] if c['id']==sid][0]['col']]) for sid in r["sources"])
    tgt_cell = [c for c in unit["cells"] if c["id"] == r["target"]][0]
    tgt = Decimal(tgt_cell["value"])
    delta = abs(s - tgt)
    tol = Decimal(r.get("tol", "0"))
    print(f"{r['note']}: sum={s} target={tgt} delta={delta} tol={tol} -> {'PASS (tol==delta)' if delta==tol else 'CHECK'}")

# Black Lung + Military Advances must be all ...... in investment columns (already visible in text)
for lbl in ["Black Lung Disability", "Military Advances"]:
    for line in text.split("\n"):
        if line.startswith(lbl):
            tail = line[len(lbl):].strip().split()
            print(f"{lbl} tail-3: {tail[-3:]}")

# Header words positioned, y-band of the header region
words = page.extract_words()
hdr = [w for w in words if 90 < w["top"] < 135]
print("header words:", [(w["text"], round(w["x0"])) for w in hdr])
