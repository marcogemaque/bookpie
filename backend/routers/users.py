import models
import schemas
from auth import create_access_token, verify_password
from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db:Session=Depends(get_db)): # noqa: B008
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=list[schemas.UserOut])
def get_user(db: Session = Depends(get_db)): # noqa: B008
    return db.query(models.User).all()

@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)): # noqa: B008
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}