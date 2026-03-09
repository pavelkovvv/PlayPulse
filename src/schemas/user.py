from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., description='Ник пользователя')
    email: str = Field(None, description='Почта пользователя')
    first_name: str = Field(None, description='Имя пользователя')
    middle_name: str = Field(None, description='Отчество пользователя')
    last_name: str = Field(None, description='Фамилия пользователя')
    is_public: bool = Field(..., description='Является ли профиль публичным')


class UserCreate(UserBase):
    password: str = Field(..., description='Пароль пользователя')


class UserCreateResponse(UserBase):
    user_id: int = Field(..., description='ID нового пользователя')
    access_token: str = Field(..., description='Токен авторизации для пользователя')
    token_exp: int = Field(..., description='Время в UNIX, когда сгорит токен')
