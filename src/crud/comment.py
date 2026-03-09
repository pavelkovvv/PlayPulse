from sqlalchemy.ext.asyncio import AsyncSession

from src.models.comment import Comment


async def add_comment(comment: None, db: AsyncSession):
    # TODO: реализовать добавление комментария после того как будет добавлена авторизация и схемы
    pass


async def get_comment(comment_id: int, db: AsyncSession):
    # TODO: реализовать получение комментария по ID
    pass


async def get_comments(game_id: int, db: AsyncSession):
    # TODO: реализовать получение всех комментариев для игры
    pass


async def update_comment(comment_id: int, comment_data: None, db: AsyncSession):
    # TODO: реализовать обновление комментария
    pass


async def delete_comment(comment_id: int, db: AsyncSession):
    # TODO: реализовать удаление комментария
    pass
