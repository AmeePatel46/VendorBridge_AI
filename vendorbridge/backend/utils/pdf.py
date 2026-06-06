from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def generate_invoice_pdf(invoice) -> str:
    os.makedirs("generated_pdfs", exist_ok=True)
    path = f"generated_pdfs/{invoice.invoice_number}.pdf"
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 60, "VendorBridge")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Invoice Number: {invoice.invoice_number}")
    c.drawString(50, height - 110, f"PO ID: {invoice.po_id}")
    c.drawString(50, height - 130, f"Amount: ₹{invoice.amount:.2f}")
    c.drawString(50, height - 150, f"Tax: ₹{invoice.tax:.2f}")
    c.drawString(50, height - 170, f"Total: ₹{invoice.total:.2f}")
    c.drawString(50, height - 190, f"Status: {invoice.status}")
    c.drawString(50, height - 220, "Thank you for your business.")
    c.save()
    return path