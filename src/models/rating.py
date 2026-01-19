from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Rating(Base):
    __tablename__ = "rating"

    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'),
        index=True,
        nullable=False,
    )
    game_id: Mapped[int] = mapped_column(
        ForeignKey('game.id'),
        index=True,
        nullable=False,
    )
    score: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)

    user: Mapped['User'] = relationship(back_populates='ratings')
    game: Mapped['Game'] = relationship(back_populates='ratings')

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'game_id'),
    )