from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product in the inventory.

    Args:
        product (schemas.ProductCreate): Product data to create.
        db (Session): Database session dependency.

    Returns:
        schemas.Product: The newly created product object.
    """
    return crud.create_product(db, product)
