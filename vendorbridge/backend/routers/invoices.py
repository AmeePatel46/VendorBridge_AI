from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from auth import require_role
from utils.pdf import generate_invoice_pdf
from utils.email import send_invoice_email
import models, schemas
import uuid

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("/")
def create_invoice(inv: schemas.InvoiceCreate, db: Session = Depends(get_db),
                   user=Depends(require_role("procurement_officer", "admin"))):
    po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == inv.po_id).first()
    if not po:
        raise HTTPException(404, "PO not found")
    invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
    tax_amount = po.total_amount * (po.tax / 100)
    invoice = models.Invoice(
        invoice_number=invoice_number,
        po_id=inv.po_id,
        amount=po.total_amount,
        tax=tax_amount,
        total=po.total_amount + tax_amount
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

@router.get("/{invoice_id}/pdf")
def download_invoice(invoice_id: int, db: Session = Depends(get_db),
                     user=Depends(require_role("procurement_officer", "admin"))):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(404, "Invoice not found")
    pdf_path = generate_invoice_pdf(invoice)
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{invoice.invoice_number}.pdf")

@router.post("/{invoice_id}/send-email")
async def email_invoice(invoice_id: int, recipient_email: str, db: Session = Depends(get_db),
                        user=Depends(require_role("procurement_officer", "admin"))):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(404, "Invoice not found")
    pdf_path = generate_invoice_pdf(invoice)
    await send_invoice_email(recipient_email, invoice.invoice_number, pdf_path)
    invoice.status = "sent"
    db.commit()
    return {"message": "Invoice sent"}

@router.get("/")
def list_invoices(db: Session = Depends(get_db), user=Depends(require_role("admin", "procurement_officer", "manager"))):
    return db.query(models.Invoice).all()