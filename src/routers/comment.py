from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_obj_db
from src.crud import comment as comment_crud


router = APIRouter(
    prefix="/comment",
    tags=["comment"],
)


@router.post("/", summary="Добавление комментария")
async def add_comment(
    comment_data: None = Query(..., description="Данные для добавления комментария"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать добавление комментария после того как будет добавлена авторизация и схемы
    pass


@router.get("/{comment_id}", summary="Получение комментария по ID")
async def get_comment(
    comment_id: int = Query(..., description="ID комментария"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать получение комментария по ID
    pass


@router.get("/game/{game_id}", summary="Получение всех комментариев к игре")
async def get_comments_for_game(
    game_id: int = Query(..., description="ID игры"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать получение всех комментариев к игре
    pass


@router.patch("/{comment_id}", summary="Обновление комментария")
async def update_comment(
    comment_id: int = Query(..., description="ID комментария"),
    comment_data: None = Query(..., description="Данные для апдейта комментария"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать обновление комментария
    pass


@router.delete("/{comment_id}", summary="Удаление комментария")
async def delete_comment(
    comment_id: int = Query(..., description="ID комментария"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать удаление комментария
    pass
