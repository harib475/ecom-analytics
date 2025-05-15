import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.models import Product, Sale, InventoryLog, InventoryChange
from app.database import engine, SessionLocal
import datetime, random

def populate():
    session = SessionLocal()

    # Clear existing data in the correct order (dependents first)
    session.query(Sale).delete()
    session.query(InventoryLog).delete()
    session.query(InventoryChange).delete()
    session.query(Product).delete()

    # Commit deletes before adding new data
    session.commit()

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
        total_sold = 0

        for _ in range(5):
            quantity_sold = random.randint(1, 5)
            total_price = prod.price * quantity_sold
            sale_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))

            # Add Sale record
            sale = Sale(
                product_id=prod.id,
                quantity=quantity_sold,
                total_price=total_price,
                sale_date=sale_date
            )
            session.add(sale)

            # Add Inventory Log (stock change)
            inventory_change = -quantity_sold  # sales reduce stock
            inventory_log = InventoryLog(
                product_id=prod.id,
                change=inventory_change,
                reason="Sold",
                timestamp=sale_date
            )
            session.add(inventory_log)

            # Add InventoryChange record to track stock changes over time
            previous_stock = prod.stock - total_sold
            new_stock = previous_stock + inventory_change
            inv_change = InventoryChange(
                product_id=prod.id,
                previous_stock=previous_stock,
                new_stock=new_stock,
                change_amount=inventory_change,
                timestamp=sale_date
            )
            session.add(inv_change)

            total_sold += quantity_sold

        # Update product stock after all sales
        prod.stock -= total_sold

    session.commit()
    session.close()

if __name__ == "__main__":
    populate()
