# import re will use this eventually
import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookBase(BaseModel):
    title: str
    cover_img: str | None = None
    author: list[str]
    genre: list[str]

class BookCreate(BookBase):
    pass

class BookOut(BookBase):
    book_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Username cannot be blank")
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(v) > 30:
            raise ValueError("Username must be at most 30 characters")
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", v):
            raise ValueError("Username must start with a letter and contain only letters, numbers, _ or -")
        return v

class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def strong_password(cls, v):
        if len(v.replace(" ","")) < 12:
            raise ValueError("Password must be at least 12 characters")
        return v

class UserOut(UserBase):
    user_id: int
    role: str
    created_at: datetime

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ReadBookBase(BaseModel):
    user_id: int
    book_id: int
    started: bool = False
    finished: bool = False
    started_date: datetime | None = None
    finished_date: datetime | None = None

class ReadBookCreate(ReadBookBase):
    pass

class ReadBookOut(ReadBookBase):
    read_books_id: int
    notes: list = []

    model_config = ConfigDict(from_attributes=True)

class NoteCreate(BaseModel):
    content: str = Field(max_length=250)

class NoteOut(BaseModel):
    note_id: int
    read_books_id: int
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)