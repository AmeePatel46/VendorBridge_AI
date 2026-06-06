from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import require_role
import models

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/")
def get_logs(db: Session = Depends(get_db), user=Depends(require_role("admin", "manager"))):
    return db.query(models.ActivityLog).order_by(models.ActivityLog.timestamp.desc()).limit(100).all()