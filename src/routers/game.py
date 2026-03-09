# from fastapi import APIRouter, Query, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.database import get_obj_db
# from src.crud import game as game_crud
#
#
# router = APIRouter(
#     prefix="/game",
#     tags=["game"],
# )
#
#
# @router.post("/", summary="Добавление игры")
# async def add_game(
#     game_data: None = Query(..., description="Данные для добавления игры"),
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать добавление игры после того как будет добавлена авторизация и схемы
#     pass
#
#
# @router.get("/{game_id}", summary="Получение данных об игре")
# async def get_game(
#     game_id: int = Query(..., description="ID игры"),
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать получение игры после того как будет добавлена авторизация
#     pass
#
#
# @router.get("/", summary="Получение данных о всех играх")
# async def get_games(
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать получение всех игр
#     # TODO: добавить сюда пагинацию
#     pass
#
#
# @router.patch("/", summary="Обновление данных игры")
# async def update_game(
#     game_data: None = Query(..., description="Данные для апдейта информации об игре"),
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать обновление игры
#     pass
#
#
# @router.delete("/{game_id}", summary="Удаление игры")
# async def delete_game(
#     game_id: int = Query(..., description="ID игры"),
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать удаление игры
#     pass
