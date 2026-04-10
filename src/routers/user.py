from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Path, Body

from logs import logger
from src.models.user import User
from src.auth import verify_token
from src.database import get_obj_db
from src.services.errors import ServiceError
from src.schemas.user import UserCreate, UserCreateResponse, GetUserResponse, GetUsersListResponse, UserUpdate
from src.services.user import (
    delete_user_for_actor,
    get_user_for_viewer,
    list_users_for_actor,
    register_user,
    update_user_for_actor,
)


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post(
    "/",
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация пользователя"
)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_obj_db),
):
    try:
        return await register_user(db, user_data)
    except ServiceError as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception as err:
        await db.rollback()
        logger.exception(
            f'При попытке регистрации пользователя (username: {user_data.username}) произошла ошибка: {err}\n'
            f'Функция/метод: create_user'
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Произошла внутренняя ошибка. Попробуйте позже.',
        )


@router.get(
    "/",
    response_model=GetUsersListResponse,
    status_code=status.HTTP_200_OK,
    summary="Получение данных о всех пользователях"
)
async def get_users(
    db: AsyncSession = Depends(get_obj_db),
    current_user: User = Depends(verify_token),
):
    try:
        return await list_users_for_actor(db, current_user)
    except ServiceError as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception as err:
        logger.exception(
            f'При попытке получения всех пользователей произошла ошибка: {err}\n'
            f'Функция/метод: get_users'
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Произошла внутренняя ошибка. Попробуйте позже.',
        )


@router.get(
    "/{user_id}",
    response_model=GetUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Получение данных о пользователе"
)
async def get_user(
    user_id: int = Path(..., description="ID пользователя"),
    db: AsyncSession = Depends(get_obj_db),
    current_user: User = Depends(verify_token)
):
    try:
        return await get_user_for_viewer(db, user_id, current_user)
    except ServiceError as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception as err:
        logger.exception(
            f'При попытке получения пользователя по ID: {user_id} произошла ошибка: {err}\n'
            f'Функция/метод: get_user'
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Произошла внутренняя ошибка. Попробуйте позже.',
        )


@router.patch(
    "/{user_id}",
    response_model=GetUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновление данных о пользователе",
)
async def update_user(
    user_id: int = Path(..., description='ID пользователя'),
    user_data: UserUpdate = Body(..., description="Данные для апдейта информации о пользователе"),
    db: AsyncSession = Depends(get_obj_db),
    current_user: User = Depends(verify_token),
):
    try:
        return await update_user_for_actor(db, user_id, current_user, user_data)
    except ServiceError as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception as err:
        await db.rollback()
        logger.exception(
            f'При попытке обновления пользователя по ID: {user_id} произошла ошибка: {err}\n'
            f'Функция/метод: update_user'
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Произошла внутренняя ошибка. Попробуйте позже.',
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление пользователя",
)
async def delete_user(
    user_id: int = Path(..., description="ID пользователя"),
    db: AsyncSession = Depends(get_obj_db),
    current_user: User = Depends(verify_token),
):
    try:
        await delete_user_for_actor(db, user_id, current_user)
    except ServiceError as err:
        raise HTTPException(status_code=err.status_code, detail=err.detail)
    except Exception as err:
        await db.rollback()
        logger.exception(
            f'При попытке удаления пользователя по ID: {user_id} произошла ошибка: {err}\n'
            f'Функция/метод: delete_user'
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Произошла внутренняя ошибка. Попробуйте позже.',
        )
