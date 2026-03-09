from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_obj_db
from src.crud import rating as rating_crud


router = APIRouter(
    prefix="/rating",
    tags=["rating"],
)


@router.post("/", summary="Добавление оценки")
async def add_rating(
    rating_data: None = Query(..., description="Данные для добавления оценки"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать добавление оценки после того как будет добавлена авторизация и схемы
    pass


@router.get("/", summary="Получение оценки пользователя по игре")
async def get_rating(
    user_id: int = Query(..., description="ID пользователя"),
    game_id: int = Query(..., description="ID игры"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать получение оценки по пользователю и игре
    pass


@router.get("/game/{game_id}", summary="Получение всех оценок по игре")
async def get_ratings_for_game(
    game_id: int = Query(..., description="ID игры"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать получение всех оценок по игре
    pass


@router.patch("/", summary="Обновление оценки")
async def update_rating(
    user_id: int = Query(..., description="ID пользователя"),
    game_id: int = Query(..., description="ID игры"),
    rating_data: None = Query(..., description="Данные для апдейта оценки"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать обновление оценки
    pass


@router.delete("/", summary="Удаление оценки")
async def delete_rating(
    user_id: int = Query(..., description="ID пользователя"),
    game_id: int = Query(..., description="ID игры"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать удаление оценки
    pass
