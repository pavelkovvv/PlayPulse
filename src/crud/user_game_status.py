from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user_game_status import UserGameStatus, StatusGame


async def add_user_game_status(status: None, db: AsyncSession):
    # TODO: реализовать добавление статуса игры пользователя после того как будет добавлена авторизация и схемы
    pass


async def get_user_game_status(user_id: int, game_id: int, db: AsyncSession):
    # TODO: реализовать получение статуса игры по пользователю и игре
    pass


async def get_user_game_statuses_for_user(user_id: int, db: AsyncSession):
    # TODO: реализовать получение всех статусов игр для пользователя
    pass


async def update_user_game_status(user_id: int, game_id: int, status_data: None, db: AsyncSession):
    # TODO: реализовать обновление статуса игры пользователя
    pass


async def delete_user_game_status(user_id: int, game_id: int, db: AsyncSession):
    # TODO: реализовать удаление статуса игры пользователя
    pass
