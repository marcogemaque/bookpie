from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.models_and_classes.models import Note, ReadBooks
from backend.models_and_classes.schemas import (
    NoteCreate,
    NoteOut,
    ReadBookCreate,
    ReadBookOut,
)
from backend.utils.dependencies import get_db

router = APIRouter(prefix="/readBooks", tags=["readBooks"])

@router.post("/register_read_book", response_model=ReadBookOut)
def create_read_books(read_book: ReadBookCreate, db:Session=Depends(get_db)):  # noqa: B008
    db_read_book = ReadBooks(**read_book.model_dump())
    db.add(db_read_book)
    db.commit()
    db.refresh(db_read_book)
    return db_read_book

@router.get("/read_books", response_model=list[ReadBookOut])
def get_read_books(db: Session = Depends(get_db)): # noqa: B008
    return db.query(ReadBooks).all()

@router.post("/read_books/{read_books_id}/notes", response_model=NoteOut)
def add_note_to_book(read_books_id: int,note: NoteCreate,db: Session = Depends(get_db)): # noqa: B008
    db_note = Note(**note.model_dump(), read_books_id=read_books_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/read_books/{read_books_id}/notes", response_model=list[NoteOut])
def get_all_notes_from_books(read_books_id: int, db: Session = Depends(get_db)):  # noqa: B008
    return db.query(Note).filter(Note.read_books_id == read_books_id).all()