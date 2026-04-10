from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from logs import logger
from src.models.user import User
from src.auth import create_jwt_token
from src.crud import user as user_crud
from src.services.errors import ServiceError
from src.utils import verification_user_action
from src.schemas.user import UserCreate, UserCreateResponse, UserUpdate


async def register_user(db: AsyncSession, user_data: UserCreate) -> UserCreateResponse:
    """
    Регистрирует нового пользователя: проверка занятости username/email, запись в БД,
    выдача JWT. При гонке по уникальному индексу — ServiceError с кодом 400.

    :param db: Асинхронная сессия БД.
    :param user_data: Данные регистрации из API.
    :returns: Ответ с полями профиля, токеном и временем истечения.
    :raises ServiceError: 400 — занят username/email или нарушение уникальности в БД.
    """
    exist_user = await user_crud.get_user_by_username(username=user_data.username, db=db)
    if exist_user:
        logger.warning(
            f'Пользователь пытался зарегистрироваться под username: {user_data.username}, который уже занят'
        )
        raise ServiceError(status.HTTP_400_BAD_REQUEST, 'username уже занят, попробуйте другой')

    if user_data.email:
        exist_email_user = await user_crud.get_user_by_email(email=user_data.email, db=db)
        if exist_email_user:
            logger.warning(
                f'Пользователь попытался зарегистрироваться с email: {user_data.email}, который уже используется'
            )
            raise ServiceError(status.HTTP_400_BAD_REQUEST, 'email уже используется, попробуйте другой')

    try:
        new_user = await user_crud.create_user(user_data, db)
    except IntegrityError:
        await db.rollback()
        logger.warning(
            f'Регистрация отклонена из‑за нарушения уникальности (username: {user_data.username}, '
            f'email: {user_data.email}) — вероятна гонка или обход предварительной проверки'
        )
        raise ServiceError(status.HTTP_400_BAD_REQUEST, 'Пользователь с таким username или email уже существует.')

    access_token, expiration = create_jwt_token(data={'sub': new_user.username})

    logger.info(f'Пользователь {user_data.username} успешно зарегистрирован')

    return UserCreateResponse(
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


async def list_users_for_actor(db: AsyncSession, actor: User) -> dict:
    """
    Возвращает всех пользователей и их количество. Доступно только администраторам.

    :param db: Асинхронная сессия БД.
    :param actor: Текущий пользователь (из токена).
    :returns: Словарь с ключами ``users`` и ``total``.
    :raises ServiceError: 403 — у ``actor`` нет флага ``is_admin``.
    """
    if not actor.is_admin:
        logger.warning(
            f'Пользователь {actor.username} пытался получить данные о всех пользователях, но у него нет доступа.'
        )
        raise ServiceError(status.HTTP_403_FORBIDDEN, 'У вас нет доступа к данным всех пользователей.')

    users = await user_crud.get_all_users(db)
    return {'users': users, 'total': len(users)}


async def get_user_for_viewer(db: AsyncSession, user_id: int, viewer: User) -> User:
    """
    Возвращает профиль пользователя по id, если запрашивающий — сам пользователь
    или целевой профиль публичный.

    :param db: Асинхронная сессия БД.
    :param user_id: Идентификатор запрашиваемого пользователя.
    :param viewer: Текущий пользователь (из токена).
    :returns: ORM-модель ``User``.
    :raises ServiceError: 404 — пользователь не найден; 403 — чужой закрытый профиль.
    """
    user = await user_crud.get_user_by_user_id(user_id, db)
    if not user:
        logger.warning(f'Пользователь с ID: {user_id} не найден.')
        raise ServiceError(status.HTTP_404_NOT_FOUND, f'Пользователь с ID: {user_id} не найден.')

    if user.id == viewer.id or user.is_public:
        return user

    logger.warning(
        f'Пользователь {viewer.username} пытался получить данные о пользователе:'
        f' {user.username}, но у него нет доступа.'
    )
    raise ServiceError(status.HTTP_403_FORBIDDEN, 'У вас нет доступа к данным этого пользователя.')


async def update_user_for_actor(
    db: AsyncSession,
    user_id: int,
    actor: User,
    user_data: UserUpdate,
) -> User:
    """
    Частично обновляет данные профиля. Разрешено только для своей учётной записи.

    :param db: Асинхронная сессия БД.
    :param user_id: Идентификатор пользователя из URL.
    :param actor: Текущий пользователь (из токена).
    :param user_data: Поля для обновления (только явно переданные и не ``None``).
    :returns: Обновлённая ORM-модель ``User``.
    :raises ServiceError: 404 — пользователь не найден; 403 — попытка изменить чужой профиль.
    """
    user_from_db = await user_crud.get_user_by_user_id(user_id, db)
    if not user_from_db:
        logger.warning(f'Пользователь с ID: {user_id} не найден.')
        raise ServiceError(status.HTTP_404_NOT_FOUND, f'Пользователь с ID: {user_id} не найден.')

    await verification_user_action(actor, user_from_db)
    return await user_crud.update_user(user_from_db, user_data, db)


async def delete_user_for_actor(db: AsyncSession, user_id: int, actor: User) -> None:
    """
    Удаляет учётную запись. Разрешено только для своего профиля.

    :param db: Асинхронная сессия БД.
    :param user_id: Идентификатор пользователя из URL.
    :param actor: Текущий пользователь (из токена).
    :raises ServiceError: 404 — пользователь не найден; 403 — попытка удалить чужой профиль.
    """
    user_from_db = await user_crud.get_user_by_user_id(user_id, db)
    if not user_from_db:
        logger.warning(f'Пользователь с ID: {user_id} не найден.')
        raise ServiceError(status.HTTP_404_NOT_FOUND, f'Пользователь с ID: {user_id} не найден.')

    await verification_user_action(actor, user_from_db)
    await user_crud.delete_user(user_from_db, db)
