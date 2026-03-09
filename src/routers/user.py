from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from logs import logger
from src.database import get_obj_db
from src.crud import user as user_crud
from src.auth import create_jwt_token
from src.schemas.user import UserCreate, UserCreateResponse


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
            user_id=new_user.id,
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
        logger.exception(f'При попытке регистрации пользователя (username: {user_data.username}) произошла ошибка: {err}\n'
                     f'Функция/метод: create_user')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Произошла внутренняя ошибка. Попробуйте позже.',
        )


# @router.get("/{user_id}", summary="Получение данных о пользователе")
# async def get_user(
#     user_id: int = Query(..., description="ID пользователя"),
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать получение пользователя после того как будет добавлена авторизация
#     pass
#
#
# @router.get("/", summary="Получение данных о всех пользователях")
# async def get_users(
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать получение всех пользователей после того как будет добавлена авторизация
#     # TODO: добавить сюда пагинацию
#     pass
#
#
# @router.patch("/", summary="Обновление данных пользователя")
# async def update_user(
#     user_data: None = Query(..., description="Данные для апдейта информации о пользователе"),
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать обновление пользователя после того как будет добавлена авторизация
#     pass
#
#
# @router.delete("/{user_id}", summary="Удаление пользователя")
# async def delete_user(
#     user_id: int = Query(..., description="ID пользователя"),
#     db: AsyncSession = Depends(get_obj_db),
# ):
#     # TODO: реализовать удаление пользователя после того как будет добавлена авторизация
#     pass
