import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.models import Product, Sale, InventoryLog
from app.database import engine, SessionLocal
import datetime, random

def populate():
    session = SessionLocal()

    # Clear existing data (ensure dependent records are deleted first)
    session.query(Sale).delete()  # Delete sales first
    session.query(InventoryLog).delete()  # Delete inventory logs
    session.query(Product).delete()  # Then delete products

    # Create some products
    products = [
        Product(name="iPhone 14", category="Electronics", price=999.99, stock=50),
        Product(name="Samsung TV", category="Electronics", price=499.99, stock=20),
        Product(name="Blender", category="Home Appliances", price=59.99, stock=100)
    ]

    session.add_all(products)
    session.commit()

    # Add sales and inventory logs for each product
    for prod in products:
        for _ in range(5):
            # Add Sale records
            sale = Sale(
                product_id=prod.id, 
                quantity=random.randint(1, 5),
                total_price=prod.price * random.randint(1, 5),
                sale_date=datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))
            )
            session.add(sale)

            # Add Inventory Log (Stock change)
            # Example: A random number of units sold or restocked
            inventory_change = random.randint(-5, 10)  # Random stock change
            reason = "Restocked" if inventory_change > 0 else "Sold"
            inventory_log = InventoryLog(
                product_id=prod.id, 
                change=inventory_change,
                reason=reason,
                timestamp=sale.sale_date  # Match the inventory change with sale date
            )
            session.add(inventory_log)

        # Update product stock after sales
        total_sold = sum([sale.quantity for sale in session.query(Sale).filter(Sale.product_id == prod.id).all()])
        prod.stock -= total_sold  # Adjust stock after sales

    # Commit all data at once
    session.commit()
    session.close()

if __name__ == "__main__":
    populate()
