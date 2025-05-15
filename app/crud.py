from datetime import date
import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import func

def create_product(db: Session, product: schemas.ProductCreate):
    """
    Create and store a new product in the database.

    Args:
        db (Session): Database session.
        product (schemas.ProductCreate): Product data to create.

    Returns:
        models.Product: The created product instance.
    """
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_sales(db: Session, skip: int = 0, limit: int = 100,
              start_date: Optional[str] = None,
              end_date: Optional[str] = None,
              product_id: Optional[int] = None,
              category: Optional[str] = None):
    """
    Retrieve sales records with optional filters and pagination.

    Args:
        db (Session): Database session.
        skip (int): Records to skip for pagination.
        limit (int): Maximum records to return.
        start_date (Optional[str]): Filter by minimum sale date.
        end_date (Optional[str]): Filter by maximum sale date.
        product_id (Optional[int]): Filter by product ID.
        category (Optional[str]): Filter by product category.

    Returns:
        List[models.Sale]: List of sales matching the criteria.
    """
    query = db.query(models.Sale).join(models.Product)

    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(models.Sale.product_id == product_id)
    if category:
        query = query.filter(models.Product.category == category)

    return query.offset(skip).limit(limit).all()

def get_inventory(db: Session, low_stock_threshold: Optional[int] = None):
    """
    Retrieve inventory products, optionally filtered by low stock.

    Args:
        db (Session): Database session.
        low_stock_threshold (Optional[int]): If provided, filters products with stock less than or equal to this value.

    Returns:
        List[models.Product]: List of products.
    """
    query = db.query(models.Product)
    if low_stock_threshold is not None:
        query = query.filter(models.Product.stock <= low_stock_threshold)
    return query.order_by(models.Product.id.desc()).all()

def compare_revenue(db: Session, start1: str, end1: str, start2: str, end2: str, category: Optional[str] = None):
    """
    Compare revenue between two time periods, optionally filtered by category.

    Args:
        db (Session): Database session.
        start1 (str): Start date for the first period.
        end1 (str): End date for the first period.
        start2 (str): Start date for the second period.
        end2 (str): End date for the second period.
        category (Optional[str]): Optional category filter.

    Returns:
        dict: Revenue comparison between the two periods.
    """
    query1 = db.query(func.sum(models.Sale.total_price)).join(models.Product)
    query2 = db.query(func.sum(models.Sale.total_price)).join(models.Product)

    if category:
        query1 = query1.filter(models.Product.category == category)
        query2 = query2.filter(models.Product.category == category)

    revenue1 = query1.filter(models.Sale.sale_date.between(start1, end1)).scalar() or 0
    revenue2 = query2.filter(models.Sale.sale_date.between(start2, end2)).scalar() or 0

    return {
        "period1": {"start": start1, "end": end1, "revenue": revenue1},
        "period2": {"start": start2, "end": end2, "revenue": revenue2},
        "difference": revenue2 - revenue1,
        "category": category
    }

def get_revenue_by_period(
    db: Session,
    period: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    """
    Get revenue report aggregated by a specific time period.

    Args:
        db (Session): Database session.
        period (str): Period to group by ('daily', 'weekly', 'monthly', 'annual').
        start_date (Optional[date]): Start date for filtering.
        end_date (Optional[date]): End date for filtering.

    Returns:
        List[dict]: Revenue data grouped by the specified period.
    """
    query = db.query(models.Sale)

    if start_date:
        query = query.filter(models.Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(models.Sale.sale_date <= end_date)

    if period == "daily":
        group_format = 'YYYY-MM-DD'
    elif period == "weekly":
        group_format = 'IYYY-IW'  # ISO week number
    elif period == "monthly":
        group_format = 'YYYY-MM'
    elif period == "annual":
        group_format = 'YYYY'
    else:
        return {"error": ("Invalid period. Use daily, weekly, monthly, or annual.")}

    group_by = func.to_char(models.Sale.sale_date, group_format)

    results = db.query(
        group_by.label("period"),
        func.sum(models.Sale.total_price).label("total_revenue")
    ).group_by(group_by).order_by(group_by).all()

    return [{"period": row.period, "total_revenue": float(row.total_revenue)} for row in results]

def get_product(db: Session, product_id: int):
    """
    Retrieve a product by its ID.

    Args:
        db (Session): Database session.
        product_id (int): ID of the product.

    Returns:
        models.Product | None: Product if found, else None.
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def update_inventory(db: Session, product: models.Product, new_stock: int):
    """
    Update the stock value of a product and log the inventory change.

    Args:
        db (Session): Database session.
        product (models.Product): Product instance to update.
        new_stock (int): New stock value to set.

    Returns:
        models.Product: Updated product instance.
    """
    previous_stock = product.stock
    change_amount = new_stock - previous_stock

    product.stock = new_stock
    db.add(product)

    inventory_change = models.InventoryChange(
        product_id=product.id,
        previous_stock=previous_stock,
        new_stock=new_stock,
        change_amount=change_amount,
        timestamp=datetime.datetime.utcnow()
    )
    db.add(inventory_change)
    db.commit()
    db.refresh(product)

    return product

def get_inventory_changes(db: Session, product_id: int):
    """
    Retrieve inventory change history for a specific product.

    Args:
        db (Session): Database session.
        product_id (int): ID of the product.

    Returns:
        List[models.InventoryChange]: List of inventory change records.
    """
    return db.query(models.InventoryChange).filter(models.InventoryChange.product_id == product_id).order_by(models.InventoryChange.timestamp.desc()).all()
