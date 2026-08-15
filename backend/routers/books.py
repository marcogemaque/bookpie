import models
import schemas
from dependencies import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=list[schemas.BookOut])
def get_books(db: Session = Depends(get_db)): # noqa: B008
    return db.query(models.Book).all()

@router.post("/", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)): # noqa: B008
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book