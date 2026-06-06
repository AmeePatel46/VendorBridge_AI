from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas, auth
from routers import vendors, rfq, quotations, approvals, purchase_orders, invoices, logs

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="VendorBridge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vendors.router)
app.include_router(rfq.router)
app.include_router(quotations.router)
app.include_router(approvals.router)
app.include_router(purchase_orders.router)
app.include_router(invoices.router)
app.include_router(logs.router)

@app.post("/auth/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=auth.hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@app.post("/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer", "role": user.role}

@app.get("/")
def root():
    return {"message": "VendorBridge API running"}