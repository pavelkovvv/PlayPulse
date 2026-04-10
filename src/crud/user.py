from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.auth import hash_password
from src.schemas.user import UserCreate, UserUpdate


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


async def get_user_by_user_id(user_id: int, db: AsyncSession) -> User | None:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    return user


async def get_all_users(db: AsyncSession) -> Sequence[Any]:
    query = select(User).order_by(User.id)
    result = await db.execute(query)
    users = result.scalars().all()

    return users


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


async def update_user(user: User, user_data: UserUpdate, db: AsyncSession) -> User:
    update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)
    if not update_data:
        return user

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user


async def delete_user(user: User, db: AsyncSession) -> None:
    await db.delete(user)
    await db.commit()
