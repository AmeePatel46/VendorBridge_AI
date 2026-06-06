from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import require_role
import models, schemas
from datetime import datetime

router = APIRouter(prefix="/rfqs", tags=["RFQ"])

@router.post("/")
def create_rfq(rfq: schemas.RFQCreate, db: Session = Depends(get_db),
               user=Depends(require_role("procurement_officer", "admin"))):
    new_rfq = models.RFQ(
        title=rfq.title, description=rfq.description,
        quantity=rfq.quantity, deadline=rfq.deadline,
        created_by=user.id
    )
    db.add(new_rfq)
    db.commit()
    db.refresh(new_rfq)
    for vendor_id in rfq.vendor_ids:
        db.add(models.RFQVendor(rfq_id=new_rfq.id, vendor_id=vendor_id))
    db.commit()
    return {"id": new_rfq.id, "message": "RFQ created"}

@router.get("/")
def list_rfqs(db: Session = Depends(get_db), user=Depends(require_role("admin", "procurement_officer", "manager"))):
    return db.query(models.RFQ).all()

@router.get("/{rfq_id}/quotations")
def get_rfq_quotations(rfq_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin", "procurement_officer", "manager"))):
    return db.query(models.Quotation).filter(models.Quotation.rfq_id == rfq_id).all()