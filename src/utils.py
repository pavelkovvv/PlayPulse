from fastapi import HTTPException, status

from models import User
from logs import logger


async def verification_user_action(current_user: User, other_user: User) -> None:
    """Позволяет понять, пытается ли пользователь изменить данные именно своего аккаунта"""
    if other_user.id != current_user.id:
        logger.error(
            f'Пользователь {current_user.username} пытался совершить действия связанные с аккаунтом пользователя:'
            f' {other_user.username}'
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Вы можете изменять/удалять данные только своего профиля.'
        )
