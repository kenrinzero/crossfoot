import pypdfium2 as pdfium
pdf = pdfium.PdfDocument("sources/treasury-mts/mts-202606.pdf")
page = pdf[35]
img = page.render(scale=3).to_pil()
img.crop((0, 0, img.width, 500)).save("scratchpad/p36-header-3x.png")
img.save("scratchpad/p36-full-3x.png")
print("saved", img.size)
