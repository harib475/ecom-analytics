from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import datetime
from sqlalchemy import Index

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    inventory_changes = relationship("InventoryChange", back_populates="product")
    sales = relationship("Sale", back_populates="product")

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    sale_date = Column(DateTime, default=datetime.datetime.utcnow)
    product = relationship("Product", back_populates="sales")

class InventoryChange(Base):
    __tablename__ = "inventory_changes"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    change = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    product = relationship("Product", back_populates="inventory_changes")


class InventoryLog(Base):
    __tablename__ = 'inventory_logs'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    change = Column(Integer)
    reason = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    product = relationship("Product", back_populates="logs")

# Relationship in Product model
Product.logs = relationship("InventoryLog", back_populates="product")

# Add Indexes for faster querying
Index("idx_sales_date", Sale.sale_date)
Index("idx_product_category", Product.category)
