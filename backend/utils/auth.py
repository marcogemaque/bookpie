# auth.py
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"])
    
    @staticmethod
    def hash_password(plain_password: str) -> str:
        return Auth.pwd_context.hash(plain_password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return Auth.pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(hours=24)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)