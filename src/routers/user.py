from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status, Path, Body

from logs import logger
from src.models.user import User
from src.database import get_obj_db
from src.crud import user as user_crud
from src.utils import verification_user_action
from src.auth import create_jwt_token, verify_token
from src.schemas.user import UserCreate, UserCreateResponse, GetUserResponse, GetUsersListResponse, UserUpdate

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
    exist_user = await user_crud.get_user_by_username(username=user_data.username, db=db)
    if exist_user:
        logger.warning(f'Пользователь пытался зарегистрироваться под username: {user_data.username}, который уже занят')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='username уже занят, попробуйте другой'
        )

    if user_data.email:
        exist_email_user = await user_crud.get_user_by_email(email=user_data.email, db=db)
        if exist_email_user:
            logger.warning(
                f'Пользователь попытался зарегистрироваться с email: {user_data.email}, который уже используется'
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='email уже используется, попробуйте другой',
            )

    try:
        new_user = await user_crud.create_user(user_data, db)
        access_token, expiration = create_jwt_token(
            data={'sub': new_user.username},
        )

        response_data = UserCreateResponse(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            middle_name=new_user.middle_name,
            is_public=new_user.is_public,
            access_token=access_token,
            token_exp=expiration,
        )
        logger.info(f'Пользователь {user_data.username} успешно зарегистрирован')

        return response_data

    except Exception as err:
        logger.exception(
            f'При попытке регистрации пользователя (username: {user_data.username}) произошла ошибка: {err}\n'
            f'Функция/метод: create_user'
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
        user = await user_crud.get_user_by_user_id(user_id, db)
        if not user:
            logger.warning(f'Пользователь с ID: {user_id} не найден.')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Пользователь с ID: {user_id} не найден.'
            )
        return user
    except HTTPException:
        raise
    except Exception as err:
        logger.exception(
            f'При попытке получения пользователя по ID: {user_id} произошла ошибка: {err}\n'
            f'Функция/метод: get_user'
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
        users = await user_crud.get_all_users(db)
        return {
            'users': users,
            'total': len(users),
        }
    except Exception as err:
        logger.exception(
            f'При попытке получения всех пользователей произошла ошибка: {err}\n'
            f'Функция/метод: get_users'
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
        user_from_db = await user_crud.get_user_by_user_id(user_id, db)
        if not user_from_db:
            logger.warning(f'Пользователь с ID: {user_id} не найден.')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Пользователь с ID: {user_id} не найден.'
            )
        await verification_user_action(current_user, user_from_db)
        return await user_crud.update_user(user_from_db, user_data, db)
    except HTTPException:
        raise
    except Exception as err:
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
        user_from_db = await user_crud.get_user_by_user_id(user_id, db)
        if not user_from_db:
            logger.warning(f'Пользователь с ID: {user_id} не найден.')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Пользователь с ID: {user_id} не найден.'
            )
        await verification_user_action(current_user, user_from_db)
        await user_crud.delete_user(user_from_db, db)
    except HTTPException:
        raise
    except Exception as err:
        logger.exception(
            f'При попытке удаления пользователя по ID: {user_id} произошла ошибка: {err}\n'
            f'Функция/метод: delete_user'
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Произошла внутренняя ошибка. Попробуйте позже.',
        )
