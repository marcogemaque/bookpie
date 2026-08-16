from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)

from backend.utils.database import Base


class Book(Base):
    __tablename__ = "book"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    cover_img = Column(String)
    author = Column(JSON)
    genre = Column(JSON)

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    created_at = Column(DateTime, server_default=func.now())

class ReadBooks(Base):
    __tablename__ = "read_book"

    read_books_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    book_id = Column(Integer, ForeignKey("book.book_id"))
    started = Column(Boolean, default=False)
    started_date = Column(DateTime)
    finished = Column(Boolean, default=False)
    finished_date = Column(DateTime)

class Note(Base):
    __tablename__ = "note"
    
    note_id = Column(Integer, primary_key=True, autoincrement=True)
    read_books_id = Column(Integer, ForeignKey("read_book.read_books_id"))
    content = Column(String(250), nullable=False)
    created_at = Column(DateTime, server_default=func.now())