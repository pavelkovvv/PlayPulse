from datetime import datetime
from sqlalchemy import String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Game(Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(75), nullable=False)
    description: Mapped[str] = mapped_column()
    release_date: Mapped[datetime] = mapped_column()
    external_source: Mapped[str] = mapped_column()
    external_id: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)

    comments: Mapped[list['Comment']] = relationship(back_populates='game', cascade="all, delete-orphan")
    ratings: Mapped[list['Rating']] = relationship(back_populates='game', cascade="all, delete-orphan")
    reviews: Mapped[list['Review']] = relationship(back_populates='game', cascade="all, delete-orphan")
    game_statuses: Mapped[list['UserGameStatus']] = relationship(back_populates='game', cascade="all, delete-orphan")
