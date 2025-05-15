from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)  # Index added here for filtering by category
    price = Column(Float)
    stock = Column(Integer)
    
    inventory_changes = relationship(
        "InventoryChange", back_populates="product", cascade="all, delete-orphan"
    )
    sales = relationship("Sale", back_populates="product")
    logs = relationship("InventoryLog", back_populates="product")

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    quantity = Column(Integer)
    total_price = Column(Float)
    sale_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    
    product = relationship("Product", back_populates="sales")

    __table_args__ = (
        Index('ix_sales_product_date', 'product_id', 'sale_date'),  # composite index for faster querying by product + date
    )

class InventoryChange(Base):
    __tablename__ = "inventory_changes"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), index=True)
    previous_stock = Column(Integer)
    new_stock = Column(Integer)
    change_amount = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    product = relationship("Product", back_populates="inventory_changes")

class InventoryLog(Base):
    __tablename__ = 'inventory_logs'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    change = Column(Integer)
    reason = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    product = relationship("Product", back_populates="logs")

