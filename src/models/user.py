from datetime import datetime
from sqlalchemy import String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    is_public: Mapped[bool] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)

    comments: Mapped[list['Comment']] = relationship(back_populates='user', cascade="all, delete-orphan")
    ratings: Mapped[list['Rating']] = relationship(back_populates='user', cascade="all, delete-orphan")
    reviews: Mapped[list['Review']] = relationship(back_populates='user', cascade="all, delete-orphan")
    game_statuses: Mapped[list['UserGameStatus']] = relationship(back_populates='user', cascade="all, delete-orphan")
