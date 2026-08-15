from fastapi import FastAPI

from backend.database import Base, engine
from backend.routers import books, read_books, users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(books.router)
app.include_router(users.router)
app.include_router(read_books.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
