from typing import Optional
from fastapi import APIRouter, Depends, Query
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