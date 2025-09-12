from fastapi import APIRouter
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd


auth_router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


context = CryptContext(schemes=["argon2"], deprecated="auto")


@auth_router.post("/register")
async def register_user(user_data: UserRequestAdd):
    hashed_password = context.hash(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:
        users_repository = UsersRepository(session)
        try:
            await users_repository.add(new_user_data)
            await session.commit()
        except IntegrityError:
            return {"status": "Bad request", "data": f"User with email {user_data.email} already exists!"}

    return {"status": "Created"}
