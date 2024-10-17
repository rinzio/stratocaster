from datetime import datetime, timedelta, timezone
import json
from typing import Dict

import jwt
from passlib.context import CryptContext

from internal.env import AUTH_SECRET_KEY, AUTH_ALGORITHM
from internal.db.models.user import BaseUserModel
from internal.db.repository.user import UserRepo


class AuthManager:

    __ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password: str) -> str:
        return cls.__ctx.hash(password)
    
    @classmethod
    def verify(cls, plain: str, hashed: str) -> bool:
        return cls.__ctx.verify(plain, hashed)
    
    @classmethod
    def create_token(cls, data: Dict, expires_in: int) -> str:
        copy = data.copy()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_in)

        copy["expires_at"] = expires_at
        to_encode = json.dumps(copy, sort_keys=True, default=str)
        return jwt.encode(json.loads(to_encode), AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)
    
    @classmethod
    def login(cls, email: str, password: str) -> BaseUserModel | None:
        user = UserRepo.get(email=email)
        if not user:
            return None
        if not cls.verify(password, user.password):
            return None
        return user