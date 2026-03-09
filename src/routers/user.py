from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_obj_db
from src.crud import user as user_crud


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/", summary="Регистрация пользователя")
async def add_user(
    user_data: None = Query(..., description="Данные для регистрации пользователя"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать добавление пользователя после того как будет добавлена авторизация
    pass


@router.get("/{user_id}", summary="Получение данных о пользователе")
async def get_user(
    user_id: int = Query(..., description="ID пользователя"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать получение пользователя после того как будет добавлена авторизация
    pass


@router.get("/", summary="Получение данных о всех пользователях")
async def get_users(
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать получение всех пользователей после того как будет добавлена авторизация
    # TODO: добавить сюда пагинацию
    pass


@router.patch("/", summary="Обновление данных пользователя")
async def update_user(
    user_data: None = Query(..., description="Данные для апдейта информации о пользователе"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать обновление пользователя после того как будет добавлена авторизация
    pass


@router.delete("/{user_id}", summary="Удаление пользователя")
async def delete_user(
    user_id: int = Query(..., description="ID пользователя"),
    db: AsyncSession = Depends(get_obj_db),
):
    # TODO: реализовать удаление пользователя после того как будет добавлена авторизация
    pass
