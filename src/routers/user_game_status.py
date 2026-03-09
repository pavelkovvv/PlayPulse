# from fastapi import APIRouter, Query, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.database import get_obj_db
# from src.crud import user_game_status as user_game_status_crud
#
#
# router = APIRouter(
#     prefix="/user-game-status",
#     tags=["user_game_status"],
# )
#
#
# @router.post("/", summary="Добавление статуса игры пользователя")
# async def add_user_game_status(
#     status_data: None = Query(..., description="Данные для добавления статуса игры пользователя"),
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать добавление статуса игры пользователя после того как будет добавлена авторизация и схемы
#     pass
#
#
# @router.get("/", summary="Получение статуса игры пользователя")
# async def get_user_game_status(
#     user_id: int = Query(..., description="ID пользователя"),
#     game_id: int = Query(..., description="ID игры"),
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать получение статуса игры пользователя по пользователю и игре
#     pass
#
#
# @router.get("/user/{user_id}", summary="Получение всех статусов игр пользователя")
# async def get_user_game_statuses_for_user(
#     user_id: int = Query(..., description="ID пользователя"),
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать получение всех статусов игр для пользователя
#     pass
#
#
# @router.patch("/", summary="Обновление статуса игры пользователя")
# async def update_user_game_status(
#     user_id: int = Query(..., description="ID пользователя"),
#     game_id: int = Query(..., description="ID игры"),
#     status_data: None = Query(..., description="Данные для апдейта статуса игры пользователя"),
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать обновление статуса игры пользователя
#     pass
#
#
# @router.delete("/", summary="Удаление статуса игры пользователя")
# async def delete_user_game_status(
#     user_id: int = Query(..., description="ID пользователя"),
#     game_id: int = Query(..., description="ID игры"),
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать удаление статуса игры пользователя
#     pass
