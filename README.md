# E-commerce Admin API

This project implements a FastAPI-based backend API for an e-commerce admin dashboard. It includes:

- Product registration
- Inventory management
- Sales tracking and revenue analytics

## Setup

1. Create a MySQL database named `ecommerce_db`.
2. Update the `DATABASE_URL` in `app/database.py` with your MySQL credentials.
3. Run the app:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

4. Populate demo data:

```bash
python demo_data/populate_demo_data.py
```

## Endpoints

- `GET /sales/`: Get sales records
- `GET /inventory/`: Check current inventory
- `POST /products/`: Add a new product



<!-- alembic init alembic     -->

<!-- alembic revision --autogenerate -m "Initial migration" -->

<!-- alembic upgrade head   -->