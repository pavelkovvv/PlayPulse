from enum import Enum
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Enum as SAEnum
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class StatusGame(Enum):
    PLANNED = 'planned'
    COMPLETED = 'completed'
    DROPPED = 'dropped'


class UserGameStatus(Base):
    __tablename__ = "user_game_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), index=True, nullable=False)
    game_id: Mapped[int] = mapped_column(ForeignKey('game.id', ondelete='CASCADE'), index=True, nullable=False)
    status: Mapped[StatusGame] = mapped_column(SAEnum(StatusGame), nullable=False)
    completion_date: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)

    user: Mapped['User'] = relationship(back_populates='game_statuses', cascade="all, delete-orphan")
    game: Mapped['Game'] = relationship(back_populates='game_statuses')

    __table_args__ = (
        UniqueConstraint('user_id', 'game_id', name='unique_user_id_game_id'),
    )
