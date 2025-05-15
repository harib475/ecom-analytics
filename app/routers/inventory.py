from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Product])
def read_inventory(
    low_stock_threshold: Optional[int] = Query(None, description="Filter products with stock less or equal to this value"),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of products in inventory.

    Args:
        low_stock_threshold (Optional[int]): Optional threshold to filter products with stock less than or equal to this value.
        db (Session): Database session dependency.

    Returns:
        List[schemas.Product]: List of products matching the criteria.
    """
    return crud.get_inventory(db, low_stock_threshold)

@router.put("/{product_id}/stock", response_model=schemas.Product)
def update_stock(
    product_id: int,
    payload: schemas.InventoryUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Update the stock quantity of a specific product.

    Args:
        product_id (int): ID of the product to update.
        payload (schemas.InventoryUpdateRequest): Request body containing the new stock value.
        db (Session): Database session dependency.

    Returns:
        schemas.Product: The updated product object.
    
    Raises:
        HTTPException: If the product is not found.
    """
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return crud.update_inventory(db, product, payload.new_stock)

@router.get("/{product_id}/changes", response_model=list[schemas.InventoryChangeResponse])
def get_inventory_changes(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the history of inventory changes for a specific product.

    Args:
        product_id (int): ID of the product.
        db (Session): Database session dependency.

    Returns:
        List[schemas.InventoryChangeResponse]: List of inventory change records.
    """
    return crud.get_inventory_changes(db, product_id)
