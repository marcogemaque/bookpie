import models
import schemas
from dependencies import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/readBooks", tags=["readBooks"])

@router.post("/register_read_book", response_model=schemas.ReadBookOut)
def create_read_books(read_book: schemas.ReadBookCreate, db:Session=Depends(get_db)):  # noqa: B008
    db_read_book = models.ReadBooks(**read_book.model_dump())
    db.add(db_read_book)
    db.commit()
    db.refresh(db_read_book)
    return db_read_book

@router.get("/read_books", response_model=list[schemas.ReadBookOut])
def get_read_books(db: Session = Depends(get_db)): # noqa: B008
    return db.query(models.ReadBooks).all()