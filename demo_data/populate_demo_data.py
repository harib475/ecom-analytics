import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.models import Product, Sale
from app.database import engine, SessionLocal
import datetime, random

def populate():
    session = SessionLocal()
    session.query(Product).delete()
    session.query(Sale).delete()

    products = [
        Product(name="iPhone 14", category="Electronics", price=999.99, stock=50),
        Product(name="Samsung TV", category="Electronics", price=499.99, stock=20),
        Product(name="Blender", category="Home Appliances", price=59.99, stock=100)
    ]

    session.add_all(products)
    session.commit()

    for prod in products:
        for _ in range(5):
            sale = Sale(product_id=prod.id, quantity=random.randint(1, 5),
                        total_price=prod.price * random.randint(1, 5),
                        sale_date=datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30)))
            session.add(sale)

    session.commit()
    session.close()

if __name__ == "__main__":
    populate()
