from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.routers import books, read_books, users
from backend.utils.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        error.pop("input", None)
        error.pop("url", None)
        error.pop("ctx", None)
        errors.append(error)
    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )

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