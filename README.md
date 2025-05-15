# 🛒 Inventory & Sales API

This project is a FastAPI-based backend for managing products, inventory, sales, and revenue reporting. It supports filtering, inventory tracking, and revenue comparison for e-commerce or retail systems.

---

## 🚀 Features

- Create and manage products
- Track product sales and inventory changes
- Generate revenue reports by day, week, month, or year
- Compare revenue across different time periods
- RESTful API with Pydantic validation
- SQLAlchemy ORM integration
- Alembic for database migrations

---


## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
    git clone https://github.com/harib475/ecom-analytics.git
    cd ecom-analytics
```

### 2. Create a Virtual Environment
```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
    pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the project root to configure your database and other settings. For example:
```bash
    DATABASE_URL=postgresql+asyncpg://user:password@hostname/databasename
```
### 5. Also need to update alembic.ini file line no 66
```bash
    sqlalchemy.url = postgresql+asyncpg://user:password@hostname/databasename
```

### 5. Run Migrations with Alembic
Initialize Alembic (only if not done)
```bash
    alembic init alembic
```

Create a New Migration
```bash
    alembic revision --autogenerate -m "Add commit message"
```

Apply Migrations
```bash
    alembic upgrade head
```


### Populate Initial Data (Optional)
Run the data population script to add sample products and sales:
```bash
    python scripts/populate_data.py
```

🚀 Running the Server
```bash
    uvicorn main:app --reload
```
Open the API docs in your browser:
http://127.0.0.1:8000/docs


📘 API Endpoints Overview
Products
GET /inventory/ — List products, optionally filter by low stock.

POST /products/ — Create a new product.

PUT /inventory/{product_id}/stock — Update product stock.

GET /inventory/{product_id}/changes — Inventory change history.

Sales
GET /sales/ — List sales with filters: start_date, end_date, product_id, category.

GET /sales/revenue/{period} — Revenue report by period (daily, weekly, monthly, annual).

GET /sales/compare/revenue — Compare revenue between two date ranges.

