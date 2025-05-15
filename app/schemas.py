from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    """
    Base schema for product data shared across creation and response models.
    """
    name: str
    category: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    """
    Schema for creating a new product.
    Inherits all fields from ProductBase.
    """
    pass

class Product(ProductBase):
    """
    Schema for reading product data with an ID field.
    """
    id: int

    class Config:
        orm_mode = True

class SaleBase(BaseModel):
    """
    Base schema for sale-related data.
    """
    product_id: int
    quantity: int
    total_price: float

class Sale(SaleBase):
    """
    Schema for reading a sale record.
    Includes ID and sale_date fields.
    """
    id: int
    sale_date: datetime

    class Config:
        orm_mode = True

class InventoryChange(BaseModel):
    """
    Schema for summarizing inventory changes.
    """
    product_id: int
    change: int
    timestamp: datetime

    class Config:
        orm_mode = True

class RevenueComparisonResponse(BaseModel):
    """
    Schema for representing revenue comparison between two periods.
    """
    period1: dict
    period2: dict
    difference: float

    class Config:
        orm_mode = True

class InventoryUpdateRequest(BaseModel):
    """
    Schema for updating the stock value of a product.
    """
    new_stock: int

class InventoryChangeResponse(BaseModel):
    """
    Schema for returning inventory change history.
    """
    id: int
    product_id: int
    previous_stock: int
    new_stock: int
    change_amount: int
    timestamp: datetime

    class Config:
        orm_mode = True
