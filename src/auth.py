import os
import jwt as py_jwt

from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from logs import logger
from src.models.user import User
from settings import config_loader
from src.database import get_obj_db
from src.crud import user as user_crud


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
EXPIRATION_TIME: timedelta = timedelta(hours=config_loader('EXPIRATION_TOKEN_HOURS'))
ALGORITHM: str = 'HS256'


def hash_password(password: str) -> str:
    """Преобразует строковый пароль в хэшированный пароль (который можно хранить в БД)"""
    return pwd_context.hash(password)


def create_jwt_token(data: dict) -> tuple[str, int]:
    """
    Генерация JWT токена.

    :param data: Вспомогательная информация для создания токена;

    Returns:
        token - сгенерированный токен в строковом формате;
        unix_time - время, которое показывает когда сгорит токен, в unix-формате
    """

    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({'exp': expiration})
    token = jwt.encode(data, os.getenv('SECRET_KEY'), algorithm=ALGORITHM)
    unix_time = int(expiration.timestamp())

    return token, unix_time


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие обычного и хешированного паролей.

    :param plain_password: Обычный (нехешированный) пароль, который нужно проверить;
    :param hashed_password: Хешированный пароль, с которым будет сравниваться обычный пароль;

    :return: Bool - булево значение с результатом проверки пароля.
    """

    return pwd_context.verify(plain_password, hashed_password)


def verify_jwt_token(token: str) -> bool | None:
    """
    Проверка JWT-токена.

    :param token: Токен в строковом формате;

    :return: Объект с результатом декодирования токена.
    """

    try:
        decoded_data = py_jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[ALGORITHM])
        return decoded_data
    except py_jwt.PyJWTError:
        logger.exception(
            f'При попытке раскодировать токен: {token} произошла ошибка.\n'
            f'Функция/метод: verify_jwt_token'
        )
        return None


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_obj_db)
) -> User | None:
    """Авторизация пользователя по переданному токену"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось проверить учетные данные',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    if not credentials.credentials or credentials.scheme != 'Bearer':
        raise credentials_exception

    try:
        payload = jwt.decode(credentials.credentials, os.getenv('SECRET_KEY'), algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        user = await user_crud.get_user_by_username(username, db)

        return user
    except JWTError as err:
        logger.error(f'При попытке расшифровать JWT-токен произошла ошибка: {err}')
        raise credentials_exception
    except Exception:
        logger.exception(
            f'При попытке расшифровать JWT-токен произошла ошибка'
            f'Функция/метод: verify_token'
        )
        raise credentials_exception
