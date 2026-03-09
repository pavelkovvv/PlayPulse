from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.game import Game


async def add_game(game: None, db: AsyncSession):
    # TODO: реализовать добавление игры после того как будет добавлена авторизация и схемы
    pass


async def get_game(game_id: int, db: AsyncSession):
    # TODO: реализовать получение игры по ID
    pass


async def get_games(db: AsyncSession):
    # TODO: реализовать получение всех игр (добавить пагинацию при необходимости)
    pass


async def update_game(game_id: int, game_data: None, db: AsyncSession):
    # TODO: реализовать обновление игры
    pass


async def delete_game(game_id: int, db: AsyncSession):
    # TODO: реализовать удаление игры
    pass
