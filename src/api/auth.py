from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService


auth_router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@auth_router.post("/register")
async def register_user(user_data: UserRequestAdd):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:
        users_repository = UsersRepository(session)
        try:
            await users_repository.add(new_user_data)
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {user_data.email} already exists!"
            )

    return {"status": "Created"}


@auth_router.post("/login")
async def login_user(user_data: UserRequestAdd, response: Response):
    auth_service = AuthService()

    async with async_session_maker() as session:
        users_repository = UsersRepository(session)
        user = await users_repository.get_user_with_hashed_password(email=user_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid username or password!"
            )

        pwd_is_valid = auth_service.verify_password(user_data.password, user.hashed_password)
        if not pwd_is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid username or password!"
            )

        access_token = auth_service.create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)

    return {"access_token": access_token}

