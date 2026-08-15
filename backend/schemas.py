from datetime import datetime

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    cover_img: str | None = None
    author: list

class BookCreate(BookBase):
    pass

class BookOut(BookBase):
    book_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    user_id: int
    role: str #unsure about this one yet

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ReadBookBase(BaseModel):
    user_id: int
    book_id: int

class ReadBookCreate(ReadBookBase):
    pass

class ReadBookOut(ReadBookBase):
    read_books_id: int
    started: bool
    finished: bool
    started_date: datetime | None
    finished_date: datetime | None

    class Config:
        from_attributes = True