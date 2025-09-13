from datetime import datetime, timezone, timedelta
from typing import Any

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

from src.config import settings


class AuthService:
    context = CryptContext(schemes=["argon2"], deprecated="auto")
    algorithm = "HS256"
    access_token_expire_minutes = 30

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=self.algorithm)

        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.context.hash(password)

    def verify_password(self, pwd: str, hashed_pwd: str):
        return self.context.verify(pwd, hashed_pwd)

    def decode_token(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[self.algorithm])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен!")
