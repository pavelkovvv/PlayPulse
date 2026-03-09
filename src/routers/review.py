from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_obj_db
from src.crud import review as review_crud


router = APIRouter(
    prefix="/review",
    tags=["review"],
)


@router.post("/", summary="Добавление отзыва")
async def add_review(
    review_data: None = Query(..., description="Данные для добавления отзыва"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать добавление отзыва после того как будет добавлена авторизация и схемы
    pass


@router.get("/", summary="Получение отзыва пользователя по игре")
async def get_review(
    user_id: int = Query(..., description="ID пользователя"),
    game_id: int = Query(..., description="ID игры"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать получение отзыва по пользователю и игре
    pass


@router.get("/game/{game_id}", summary="Получение всех отзывов по игре")
async def get_reviews_for_game(
    game_id: int = Query(..., description="ID игры"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать получение всех отзывов по игре
    pass


@router.patch("/", summary="Обновление отзыва")
async def update_review(
    user_id: int = Query(..., description="ID пользователя"),
    game_id: int = Query(..., description="ID игры"),
    review_data: None = Query(..., description="Данные для апдейта отзыва"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать обновление отзыва
    pass


@router.delete("/", summary="Удаление отзыва")
async def delete_review(
    user_id: int = Query(..., description="ID пользователя"),
    game_id: int = Query(..., description="ID игры"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать удаление отзыва
    pass
