from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import require_role
import models, schemas
import uuid

router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])

@router.post("/")
def create_po(po: schemas.POCreate, db: Session = Depends(get_db),
              user=Depends(require_role("procurement_officer", "admin"))):
    quotation = db.query(models.Quotation).filter(
        models.Quotation.id == po.quotation_id,
        models.Quotation.status == "approved"
    ).first()
    if not quotation:
        raise HTTPException(400, "Quotation not approved or not found")
    po_number = f"PO-{uuid.uuid4().hex[:8].upper()}"
    total = quotation.total_price * (1 + po.tax / 100)
    new_po = models.PurchaseOrder(
        po_number=po_number,
        quotation_id=po.quotation_id,
        total_amount=total,
        tax=po.tax
    )
    db.add(new_po)
    db.commit()
    db.refresh(new_po)
    return new_po

@router.get("/")
def list_pos(db: Session = Depends(get_db), user=Depends(require_role("admin", "procurement_officer", "manager"))):
    return db.query(models.PurchaseOrder).all()