# VendorBridge 🏗️
### Procurement & Vendor Management ERP

A full-stack ERP platform to digitize and streamline procurement operations — from vendor registration to invoice generation.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Database | MySQL + SQLAlchemy |
| Auth | JWT (python-jose + passlib) |
| Frontend | Plain HTML + CSS + JavaScript |
| PDF | ReportLab |
| Email | SMTP (Gmail) |

---

## 📁 Project Structure

```
vendorbridge/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── routers/
│   │   ├── vendors.py
│   │   ├── rfq.py
│   │   ├── quotations.py
│   │   ├── approvals.py
│   │   ├── purchase_orders.py
│   │   ├── invoices.py
│   │   └── logs.py
│   └── utils/
│       ├── pdf.py
│       └── email.py
└── frontend/
    ├── index.html
    ├── signup.html
    ├── dashboard.html
    ├── vendors.html
    ├── rfq.html
    ├── quotations.html
    ├── approvals.html
    ├── purchase_orders.html
    ├── invoices.html
    └── js/
        └── api.js
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- Git

### 1. Clone the repository
```bash
git clone https://github.com/AmeePatel46/VendorBridge_AI.git
cd VendorBridge_AI
```

### 2. Create virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
cd vendorbridge/backend
pip install fastapi uvicorn sqlalchemy pymysql "python-jose[cryptography]" "passlib[bcrypt]" python-multipart "pydantic[email]" reportlab python-dotenv bcrypt==4.0.1
```

### 4. Configure environment
Create a `.env` file inside `vendorbridge/backend/`:
```env
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/vendorbridge
SECRET_KEY=anyrandomstring123
MAIL_USERNAME=youremail@gmail.com
MAIL_PASSWORD=your_gmail_app_password
MAIL_FROM=youremail@gmail.com
MAIL_SERVER=smtp.gmail.com
```

### 5. Create MySQL database
```sql
CREATE DATABASE vendorbridge;
```

### 6. Run the backend
```bash
cd vendorbridge/backend
uvicorn main:app --reload --port 8000
```

### 7. Run the frontend
```bash
cd vendorbridge/frontend
python -m http.server 5500
```

---

## 🌐 Access

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5500/index.html |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Root | http://localhost:8000 |

---

## 👥 User Roles

| Role | Permissions |
|------|------------|
| **Admin** | Manage users, vendors, view analytics |
| **Procurement Officer** | Create RFQs, compare quotes, generate PO & invoices |
| **Manager** | Approve/reject procurement requests |
| **Vendor** | Submit quotations, track RFQ status |

---

## 📋 Modules

### 1. 🔐 Authentication
- Signup / Login
- JWT-based session handling
- Role-based access control

### 2. 🏢 Vendor Management
- Register vendors with GST details
- Track vendor status (active/inactive)
- Search and filter vendors

### 3. 📄 RFQ (Request for Quotation)
- Create RFQs with product details and deadlines
- Assign vendors to RFQs
- Track RFQ status

### 4. 💰 Quotation Management
- Vendors submit quotations with pricing and delivery timelines
- Side-by-side quotation comparison
- Lowest price highlighting 🏆

### 5. ✅ Approval Workflow
- Manager approves or rejects quotations
- Remarks and approval timeline tracking
- Status transitions

### 6. 📦 Purchase Orders
- Auto-generated PO numbers
- Tax calculations
- Status tracking

### 7. 🧾 Invoice Generation
- Auto-generated invoice numbers
- PDF download
- Email dispatch
- Status updates (generated → sent → paid)

---

## 🔄 Procurement Workflow

```
RFQ Created → Vendors Invited → Quotations Submitted
     → Comparison → Approval → Purchase Order → Invoice → Dispatch
```

---

## 📬 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/signup | Register user |
| POST | /auth/login | Login & get token |
| GET/POST | /vendors/ | List/Create vendors |
| GET/POST | /rfqs/ | List/Create RFQs |
| GET/POST | /quotations/ | List/Submit quotations |
| GET | /quotations/compare/{rfq_id} | Compare quotes |
| POST | /approvals/ | Approve/Reject |
| GET/POST | /purchase-orders/ | List/Create POs |
| GET/POST | /invoices/ | List/Generate invoices |
| GET | /invoices/{id}/pdf | Download PDF |
| POST | /invoices/{id}/send-email | Email invoice |
| GET | /logs/ | Activity logs |

---

## 🛠️ Built With

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for database management
- [PyMySQL](https://pymysql.readthedocs.io/) - MySQL connector
- [ReportLab](https://www.reportlab.com/) - PDF generation
- [python-jose](https://python-jose.readthedocs.io/) - JWT tokens

---
***Developer
Amee Patel
Dhrity Patel
Devanshi Raval
Hetvi Trivedi


---

*Built for VendorBridge Hackathon 2026* 🏆
