from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Auth
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "procurement_officer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

# Vendor
class VendorCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    category: str
    gst_number: str

class VendorOut(VendorCreate):
    id: int
    status: str
    class Config:
        from_attributes = True

# RFQ
class RFQCreate(BaseModel):
    title: str
    description: str
    quantity: int
    deadline: datetime
    vendor_ids: List[int]

class RFQOut(BaseModel):
    id: int
    title: str
    status: str
    deadline: datetime
    class Config:
        from_attributes = True

# Quotation
class QuotationCreate(BaseModel):
    rfq_id: int
    vendor_id: int
    unit_price: float
    total_price: float
    delivery_days: int
    notes: Optional[str] = ""

class QuotationOut(QuotationCreate):
    id: int
    status: str
    submitted_at: datetime
    class Config:
        from_attributes = True

# Approval
class ApprovalAction(BaseModel):
    quotation_id: int
    status: str   # "approved" or "rejected"
    remarks: Optional[str] = ""

# PO
class POCreate(BaseModel):
    quotation_id: int
    tax: float

# Invoice
class InvoiceCreate(BaseModel):
    po_id: int