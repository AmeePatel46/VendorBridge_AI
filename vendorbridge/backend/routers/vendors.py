from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import require_role
import models, schemas

router = APIRouter(prefix="/vendors", tags=["Vendors"])

@router.post("/", response_model=schemas.VendorOut)
def create_vendor(vendor: schemas.VendorCreate, db: Session = Depends(get_db),
                  user=Depends(require_role("admin", "procurement_officer"))):
    db_vendor = models.Vendor(**vendor.dict())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

@router.get("/", response_model=list[schemas.VendorOut])
def list_vendors(db: Session = Depends(get_db), user=Depends(require_role("admin", "procurement_officer", "manager"))):
    return db.query(models.Vendor).all()

@router.put("/{vendor_id}/status")
def toggle_status(vendor_id: int, status: str, db: Session = Depends(get_db),
                  user=Depends(require_role("admin"))):
    vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(404, "Vendor not found")
    vendor.status = status
    db.commit()
    return {"message": "Status updated"}