import sys, json
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4  
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def to_point(millimeters): # takes mm input and computes reportlab position
    return millimeters * 2.83465

def create_pdf(args):
    # init
    c = Canvas('myfile.pdf', pagesize=A4)
    width, height = A4  #keep for later
    with open(args, "r") as f:
        data = json.load(f)
    
    # logo
    image_path = "Superduper.png"
    image = ImageReader(image_path)
    image_width, image_height = image.getSize()
    x = to_point(17)
    y = height - to_point(23)
    c.drawImage(image, x, y, width=to_point(62)-x, height=image_height/2)

    # billing address 
    c.setFont("Helvetica-Bold", 8)
    c.drawString(to_point(20), height-to_point(35), "Rechnungsadresse")

    c.setFont("Helvetica", 8)
    billing_address = data["billing_address"]
    address = [billing_address['name'], billing_address['addr1'], billing_address['addr2'], billing_address['country']]
    leading = 10
    for n,i in enumerate(address):
        c.drawString(to_point(20), height-to_point(39) - n*leading, i)

    # shipping address

    c.setFont("Helvetica-Bold", 8)
    c.drawString(to_point(20), height-to_point(62), "Lieferadresse")

    c.setFont("Helvetica", 8)
    billing_address = data["billing_address"]
    address = [billing_address['name'], billing_address['addr1'], billing_address['addr2'], billing_address['country']]
    leading = 10
    for n,i in enumerate(address):
        c.drawString(to_point(20), height-to_point(66) - n*leading, i)

    ### LEFT SIDE
    # invoice number
    right_aligned_style = ParagraphStyle("right_aligned_style", alignment=2)
    text_parts = f"<font face='Helvetica-Bold' size=8>Rechnungsnummer</font><font face='Helvetica' size=8> {data['no_invoice']}</font>"
    paragraph = Paragraph(text_parts, right_aligned_style)
    paragraph.wrapOn(c, width, height)
    paragraph.drawOn(c, -to_point(10), height-to_point(35))
    # date of the invoice
    text_parts = f"<font face='Helvetica-Bold' size=8>Rechnungsdatum</font><font face='Helvetica' size=8> {data['date_invoice']}</font>"
    paragraph = Paragraph(text_parts, right_aligned_style)
    paragraph.wrapOn(c, width, height)
    paragraph.drawOn(c, -to_point(10), height-to_point(35)-10)
    # number of order
    text_parts = f"<font face='Helvetica-Bold' size=8>Bestellnummer</font><font face='Helvetica' size=8> {data['no_order']}</font>"
    paragraph = Paragraph(text_parts, right_aligned_style)
    paragraph.wrapOn(c, width, height)
    paragraph.drawOn(c, -to_point(10), height-to_point(35)-20)
    # date of order
    text_parts = f"<font face='Helvetica-Bold' size=8>Bestelldatum</font><font face='Helvetica' size=8> {data['date_order']}</font>"
    paragraph = Paragraph(text_parts, right_aligned_style)
    paragraph.wrapOn(c, width, height)
    paragraph.drawOn(c, -to_point(10), height-to_point(35)-30)
    # date of order
    text_parts = f"<font face='Helvetica-Bold' size=8>Lieferdatum</font><font face='Helvetica' size=8> {data['date_delivery']}</font>"
    paragraph = Paragraph(text_parts, right_aligned_style)
    paragraph.wrapOn(c, width, height)
    paragraph.drawOn(c, -to_point(10), height-to_point(35)-40) 
    # delivery type
    text_parts = f"<font face='Helvetica-Bold' size=8>Lieferart</font><font face='Helvetica' size=8> {data['delivery_type']}</font>"
    paragraph = Paragraph(text_parts, right_aligned_style)
    paragraph.wrapOn(c, width, height)
    paragraph.drawOn(c, -to_point(10), height-to_point(35)-50)
    # type payment
    text_parts = f"<font face='Helvetica-Bold' size=8>Zahlungsart</font><font face='Helvetica' size=8> {data['type_payment']}</font>"
    paragraph = Paragraph(text_parts, right_aligned_style)
    paragraph.wrapOn(c, width, height)
    paragraph.drawOn(c, -to_point(10), height-to_point(35)-60)


    # MAIN
    c.setFont("Helvetica-Bold", 13)
    c.drawString(to_point(20), height-to_point(100), f"Rechnung Nr. {data['no_invoice']}")
    c.setFont("Helvetica", 8)
    c.drawString(to_point(20), height-to_point(108.5), "Vielen Dank für Ihren Einkauf bei Super Duper!")

    c.setFont("Helvetica-Bold", 9)
    c.drawString(to_point(21.5), height-to_point(120), "Pos.")
    c.drawString(to_point(32), height-to_point(120), "Art.-Nr.")
    c.drawString(to_point(49), height-to_point(120), "Artikel")
    c.drawString(to_point(123), height-to_point(120), "Anzahl")
    c.drawString(to_point(139), height-to_point(120), "MwSt.")
    c.drawString(to_point(155), height-to_point(120), "Einzelpreis")
    c.drawString(to_point(179.5), height-to_point(120), "Gesamtpreis")

    c.setLineWidth(1)
    c.line(to_point(20), height-to_point(122), to_point(200), height-to_point(122))

    # PRODUCTS
    try:
        # first compute the name. 
        # rest is aligned with respect to the name
        for n, product in enumerate(data['products']):
            if n<9:
                pos = "0" + str(n+1)
            else: 
                pos = str(n+1)
            text_parts = f"<font face='Helvetica' size=9>{product['name']}</font><font face='Helvetica' size=7>\n{product['name_details']}</font>"
            paragraph = Paragraph(text_parts)
            paragraph.wrapOn(c, to_point(102-48.5), height)
            paragraph.drawOn(c, to_point(49), height-to_point(133))
            raise RuntimeError
    except RuntimeError:
        pass




    c.showPage()
    c.save()

if __name__ == "__main__":
    args = sys.argv
    args = args[1:]
    args = "test.json"
    create_pdf(args)
