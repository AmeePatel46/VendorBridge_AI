from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import require_role
import models, schemas

router = APIRouter(prefix="/quotations", tags=["Quotations"])

@router.post("/")
def submit_quotation(q: schemas.QuotationCreate, db: Session = Depends(get_db),
                     user=Depends(require_role("vendor", "procurement_officer"))):
    quotation = models.Quotation(**q.dict())
    db.add(quotation)
    db.commit()
    db.refresh(quotation)
    return quotation

@router.get("/compare/{rfq_id}")
def compare_quotations(rfq_id: int, db: Session = Depends(get_db),
                       user=Depends(require_role("procurement_officer", "manager", "admin"))):
    quotes = db.query(models.Quotation).filter(models.Quotation.rfq_id == rfq_id).all()
    result = []
    for q in quotes:
        vendor = db.query(models.Vendor).filter(models.Vendor.id == q.vendor_id).first()
        result.append({
            "quotation_id": q.id,
            "vendor": vendor.name,
            "unit_price": q.unit_price,
            "total_price": q.total_price,
            "delivery_days": q.delivery_days,
            "notes": q.notes
        })
    result.sort(key=lambda x: x["total_price"])
    return result