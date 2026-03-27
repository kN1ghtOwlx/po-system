# PO Management System

A Purchase Order Management System built with FastAPI, PostgreSQL, and vanilla JavaScript.

---

## Tech Stack

- **Backend** — Python, FastAPI, SQLAlchemy
- **Database** — PostgreSQL
- **Frontend** — HTML5, Bootstrap 5, Vanilla JS
- **Auth** — JWT (python-jose)
- **AI** — Google Gemini API

---

## Project Structure
```
po-management/
├── backend/
│   ├── routers/
│   │   ├── vendors.py
│   │   ├── products.py
│   │   ├── orders.py
│   │   ├── auth.py
│   │   └── ai.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   └── requirements.txt
├── frontend/
│   ├── login.html
│   ├── index.html
│   └── create_po.html
├── .gitignore   
└── README.md
```

---

## Database Design

Four tables make up the core schema:

**vendors** — stores supplier information including name, contact, and a rating score between 1 and 5.

**products** — stores purchasable items with a unique SKU, unit price, and current stock level.

**purchase_orders** — the main document linking a vendor to an order. Holds a unique reference number, status, and the calculated total amount including tax.

**po_items** — junction table between purchase_orders and products. Stores the quantity and unit price for each product line in a given order. One PO can have many items; one product can appear in many POs.

### Relationships
```
vendors ──< purchase_orders ──< po_items >── products
```

- A vendor has many purchase orders
- A purchase order has many line items
- Each line item links to one product

---

## How to Run

### Prerequisites

- Python 3.11+
- PostgreSQL 15+

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd po-management
```

### 2. Set up the backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up the database
```bash
psql -U postgres
```
```sql
CREATE DATABASE po_management;
\q
```

### 4. Configure environment variables

Create a `.env` file inside the `backend/` folder:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/po_management
SECRET_KEY=mysecretkey123
ALGORITHM=HS256
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Seed the database
```bash
python seed.py
```

### 6. Start the backend
```bash
uvicorn main:app --reload
```

API runs at **http://localhost:8000**  
Interactive docs at **http://localhost:8000/docs**

### 7. Start the frontend

Open a new terminal:
```bash
cd frontend
python3 -m http.server 3000
```

Frontend runs at **http://localhost:3000/login.html**

---

## Default Login

| Username | Password |
|----------|----------|
| admin    | admin123 |

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /auth/login | Login and get JWT token | No |
| GET | /vendors/ | List all vendors | No |
| POST | /vendors/ | Create a vendor | No |
| GET | /products/ | List all products | No |
| POST | /products/ | Create a product | No |
| GET | /orders/ | List all purchase orders | No |
| POST | /orders/ | Create a purchase order | Yes |
| PATCH | /orders/{id}/status | Update order status | Yes |
| POST | /ai/describe | Generate AI product description | No |

---

## Business Logic

### Calculate Total

When a purchase order is created, the system automatically calculates the total:
```
subtotal = sum of (quantity × unit_price) for each line item
total    = subtotal × 1.05  (5% tax applied)
```

This runs server-side every time a new order is submitted, ensuring the total is always accurate regardless of what the frontend sends.

---

## AI Feature

Clicking the ✨ button next to any product on the Create PO page sends the product name to the Gemini API and returns a 2-sentence professional marketing description. The description appears below the product dropdown in real time.