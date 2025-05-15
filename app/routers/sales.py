from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Sale])
def read_sales(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    product_id: Optional[int] = Query(None, description="Product ID"),
    category: Optional[str] = Query(None, description="Product category"),
    db: Session = Depends(get_db),
):
    """
    Retrieve a list of sales records with optional filters and pagination.

    Args:
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        start_date (Optional[str]): Start date to filter sales (YYYY-MM-DD).
        end_date (Optional[str]): End date to filter sales (YYYY-MM-DD).
        product_id (Optional[int]): Filter by product ID.
        category (Optional[str]): Filter by product category.
        db (Session): Database session dependency.

    Returns:
        List[schemas.Sale]: List of sales records.
    """
    return crud.get_sales(
        db,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        product_id=product_id,
        category=category
    )

@router.get("/revenue/{period}")
def get_revenue_report(
    period: str,
    db: Session = Depends(get_db),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    """
    Generate a revenue report for a specified period.

    Args:
        period (str): Time period for revenue aggregation (e.g., daily, monthly).
        db (Session): Database session dependency.
        start_date (Optional[date]): Optional start date filter.
        end_date (Optional[date]): Optional end date filter.

    Returns:
        Any: Revenue data grouped by the specified period.
    """
    return crud.get_revenue_by_period(db, period, start_date, end_date)

@router.get("/compare/revenue", response_model=schemas.RevenueComparisonResponse)
def compare(
    start1: str,
    end1: str,
    start2: str,
    end2: str,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Compare revenue between two different date ranges, optionally filtered by category.

    Args:
        start1 (str): Start date of the first period (YYYY-MM-DD).
        end1 (str): End date of the first period (YYYY-MM-DD).
        start2 (str): Start date of the second period (YYYY-MM-DD).
        end2 (str): End date of the second period (YYYY-MM-DD).
        category (Optional[str]): Optional product category filter.
        db (Session): Database session dependency.

    Returns:
        schemas.RevenueComparisonResponse: Revenue comparison data.
    """
    return crud.compare_revenue(db, start1, end1, start2, end2, category)
