from sqlalchemy.ext.asyncio import AsyncSession

from src.models.rating import Rating


async def add_rating(rating: None, db: AsyncSession):
    # TODO: реализовать добавление оценки после того как будет добавлена авторизация и схемы
    pass


async def get_rating(user_id: int, game_id: int, db: AsyncSession):
    # TODO: реализовать получение оценки по пользователю и игре
    pass


async def get_ratings_for_game(game_id: int, db: AsyncSession):
    # TODO: реализовать получение всех оценок для игры
    pass


async def update_rating(user_id: int, game_id: int, rating_data: None, db: AsyncSession):
    # TODO: реализовать обновление оценки
    pass


async def delete_rating(user_id: int, game_id: int, db: AsyncSession):
    # TODO: реализовать удаление оценки
    pass
