from sqlalchemy.ext.asyncio import AsyncSession

from src.models.review import Review


async def add_review(review: None, db: AsyncSession):
    # TODO: реализовать добавление отзыва после того как будет добавлена авторизация и схемы
    pass


async def get_review(user_id: int, game_id: int, db: AsyncSession):
    # TODO: реализовать получение отзыва по пользователю и игре
    pass


async def get_reviews_for_game(game_id: int, db: AsyncSession):
    # TODO: реализовать получение всех отзывов для игры
    pass


async def update_review(user_id: int, game_id: int, review_data: None, db: AsyncSession):
    # TODO: реализовать обновление отзыва
    pass


async def delete_review(user_id: int, game_id: int, db: AsyncSession):
    # TODO: реализовать удаление отзыва
    pass
