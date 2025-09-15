from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService


auth_router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@auth_router.post("/register")
async def register_user(user_data: UserRequestAdd, db: DBDep):
    hashed_password = AuthService().hash_password(user_data.password)
    new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)

    try:
        await db.users.add(new_user_data)
        await db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User with email {user_data.email} already exists!"
        )

    return {"status": "Created"}


@auth_router.post("/login")
async def login_user(user_data: UserRequestAdd, db: DBDep, response: Response):
    auth_service = AuthService()

    user = await db.users.get_user_with_hashed_password(email=user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid username or password!"
        )

    pwd_is_valid = auth_service.verify_password(user_data.password, user.hashed_password)
    if not pwd_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid username or password!"
        )

    access_token = auth_service.create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}


@auth_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")

    return {"status": "OK"}


@auth_router.get("/me")
async def me(user_id: UserIdDep, db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user
