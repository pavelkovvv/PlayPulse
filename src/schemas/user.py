from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(..., description='Ник пользователя')
    email: EmailStr = Field(None, description='Почта пользователя')
    first_name: str = Field(None, description='Имя пользователя')
    middle_name: str = Field(None, description='Отчество пользователя')
    last_name: str = Field(None, description='Фамилия пользователя')
    is_public: bool = Field(..., description='Является ли профиль публичным')


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description='Пароль пользователя')


class UserCreateResponse(UserBase):
    id: int = Field(..., description='ID нового пользователя')
    access_token: str = Field(..., description='Токен авторизации для пользователя')
    token_exp: int = Field(..., description='Время в UNIX, когда сгорит токен')


class GetUserResponse(UserBase):
    id: int = Field(..., description='ID пользователя')
    created_at: datetime = Field(..., description='Время создания учетной записи пользователя')
    class Config:
        model_config = {"from_attributes": True}


class GetUsersListResponse(BaseModel):
    users: list[GetUserResponse] = Field(..., description='Список пользователей')
    total: int = Field(..., description='Количество объектов')


class UserUpdate(BaseModel):
    first_name: str = Field(None, description='Имя пользователя')
    middle_name: str = Field(None, description='Отчество пользователя')
    last_name: str = Field(None, description='Фамилия пользователя')
