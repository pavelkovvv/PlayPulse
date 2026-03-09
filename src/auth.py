import os

from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from settings import config_loader


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
