from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(Enum("admin", "procurement_officer", "manager", "vendor"), default="procurement_officer")
    created_at = Column(DateTime, default=datetime.utcnow)

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    category = Column(String(100))
    gst_number = Column(String(50))
    status = Column(Enum("active", "inactive"), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    quotations = relationship("Quotation", back_populates="vendor")

class RFQ(Base):
    __tablename__ = "rfqs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    quantity = Column(Integer)
    deadline = Column(DateTime)
    status = Column(Enum("open", "closed", "awarded"), default="open")
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    quotations = relationship("Quotation", back_populates="rfq")

class RFQVendor(Base):
    __tablename__ = "rfq_vendors"
    id = Column(Integer, primary_key=True)
    rfq_id = Column(Integer, ForeignKey("rfqs.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))

class Quotation(Base):
    __tablename__ = "quotations"
    id = Column(Integer, primary_key=True, index=True)
    rfq_id = Column(Integer, ForeignKey("rfqs.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    unit_price = Column(Float)
    total_price = Column(Float)
    delivery_days = Column(Integer)
    notes = Column(Text)
    status = Column(Enum("submitted", "accepted", "rejected"), default="submitted")
    submitted_at = Column(DateTime, default=datetime.utcnow)
    rfq = relationship("RFQ", back_populates="quotations")
    vendor = relationship("Vendor", back_populates="quotations")

class Approval(Base):
    __tablename__ = "approvals"
    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"))
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum("pending", "approved", "rejected"), default="pending")
    remarks = Column(Text)
    reviewed_at = Column(DateTime, nullable=True)

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String(50), unique=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"))
    total_amount = Column(Float)
    tax = Column(Float)
    status = Column(Enum("issued", "delivered", "cancelled"), default="issued")
    created_at = Column(DateTime, default=datetime.utcnow)

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"))
    amount = Column(Float)
    tax = Column(Float)
    total = Column(Float)
    status = Column(Enum("generated", "sent", "paid"), default="generated")
    created_at = Column(DateTime, default=datetime.utcnow)

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(255))
    module = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)