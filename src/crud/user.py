from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.auth import hash_password
from src.schemas.user import UserCreate


async def get_user_by_username(username: str, db: AsyncSession) -> User | None:
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    return user


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    return user


async def create_user(user_data: UserCreate, db: AsyncSession) -> User:
    user = User(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        middle_name=user_data.middle_name,
        last_name=user_data.last_name,
        is_public=user_data.is_public,
        password_hash=hash_password(user_data.password),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


# async def add_user(user: None, db: AsyncSession):
#     # TODO: реализовать добавление пользователя после того как будет добавлена авторизация
#     pass
#
#
# async def get_user(user: None, db: AsyncSession):
#     # TODO: реализовать получение пользователя после того как будет добавлена авторизация
#     pass
#
#
# async def get_users(user: None, db: AsyncSession):
#     # TODO: реализовать получение всех пользователей после того как будет добавлена авторизация
#     pass
#
#
# async def update_user(user: None, db: AsyncSession):
#     # TODO: реализовать обновление пользователя после того как будет добавлена авторизация
#     pass
#
#
# async def delete_user(user: None, db: AsyncSession):
#     # TODO: реализовать удаление пользователя после того как будет добавлена авторизация
#     pass
