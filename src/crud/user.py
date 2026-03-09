from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


async def add_user(user: None, db: AsyncSession):
    # TODO: реализовать добавление пользователя после того как будет добавлена авторизация
    pass


async def get_user(user: None, db: AsyncSession):
    # TODO: реализовать получение пользователя после того как будет добавлена авторизация
    pass


async def get_users(user: None, db: AsyncSession):
    # TODO: реализовать получение всех пользователей после того как будет добавлена авторизация
    pass


async def update_user(user: None, db: AsyncSession):
    # TODO: реализовать обновление пользователя после того как будет добавлена авторизация
    pass


async def delete_user(user: None, db: AsyncSession):
    # TODO: реализовать удаление пользователя после того как будет добавлена авторизация
    pass
