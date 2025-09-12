from pydantic import EmailStr

from src.schemas.base import BaseSchema


class UserRequestAdd(BaseSchema):
    email: EmailStr
    password: str


class UserAdd(BaseSchema):
    email: EmailStr
    hashed_password: str


class User(BaseSchema):
    id: int
    email: EmailStr
