from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.models_and_classes.models import User
from backend.models_and_classes.schemas import Token, UserCreate, UserLogin, UserOut
from backend.utils.auth import Auth
from backend.utils.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)): # noqa: B008
    db_user = User(
        username=user.username,
        password=Auth.hash_password(user.password)  # hash before storing
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=list[UserOut])
def get_user(db: Session = Depends(get_db)): # noqa: B008
    return db.query(User).all()

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)): # noqa: B008
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not Auth.verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = Auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}