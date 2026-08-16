# auth.py
import hashlib
import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

class Auth:
    @staticmethod
    def _pre_hash(password: str) -> bytes:
        # Pre-hashes to a fixed 32-byte digest to permanently eliminate the 72-byte limit
        return hashlib.sha256(password.encode("utf-8")).digest()

    @staticmethod
    def hash_password(plain_password: str) -> str:
        digest = Auth._pre_hash(plain_password)
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(digest, salt).decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        digest = Auth._pre_hash(plain_password)
        return bcrypt.checkpw(digest, hashed_password.encode("utf-8"))

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(hours=24)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)