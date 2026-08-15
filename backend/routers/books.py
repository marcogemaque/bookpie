from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.models import Book
from backend.schemas import BookCreate, BookOut
from backend.utils.dependencies import get_db

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=list[BookOut])
def get_books(db: Session = Depends(get_db)): # noqa: B008
    return db.query(Book).all()

@router.post("/", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)): # noqa: B008
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book