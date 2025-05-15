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
    return crud.get_inventory(db, low_stock_threshold)


@router.put("/{product_id}/stock", response_model=schemas.Product)
def update_stock(
    product_id: int,
    payload: schemas.InventoryUpdateRequest,
    db: Session = Depends(get_db)
):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return crud.update_inventory(db, product, payload.new_stock)

@router.get("/{product_id}/changes", response_model=list[schemas.InventoryChangeResponse])
def get_inventory_changes(product_id: int, db: Session = Depends(get_db)):
    return crud.get_inventory_changes(db, product_id)