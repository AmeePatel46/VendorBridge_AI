from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import require_role
import models, schemas
from datetime import datetime

router = APIRouter(prefix="/approvals", tags=["Approvals"])

@router.post("/")
def process_approval(action: schemas.ApprovalAction, db: Session = Depends(get_db),
                     user=Depends(require_role("manager", "admin"))):
    quotation = db.query(models.Quotation).filter(models.Quotation.id == action.quotation_id).first()
    if not quotation:
        raise HTTPException(404, "Quotation not found")
    approval = models.Approval(
        quotation_id=action.quotation_id,
        reviewed_by=user.id,
        status=action.status,
        remarks=action.remarks,
        reviewed_at=datetime.utcnow()
    )
    quotation.status = action.status
    db.add(approval)
    db.commit()
    return {"message": f"Quotation {action.status}"}

@router.get("/")
def list_approvals(db: Session = Depends(get_db), user=Depends(require_role("manager", "admin"))):
    return db.query(models.Approval).all()