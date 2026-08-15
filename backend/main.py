from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import books, read_books, users
from backend.utils.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #we'll replace once out of dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(users.router)
app.include_router(read_books.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}