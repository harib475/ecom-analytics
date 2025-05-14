from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float

class Sale(SaleBase):
    id: int
    sale_date: datetime

    class Config:
        orm_mode = True

class InventoryChange(BaseModel):
    product_id: int
    change: int
    timestamp: datetime

    class Config:
        orm_mode = True
