from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Review(Base):
    __tablename__ = "review"

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
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)

    user: Mapped['User'] = relationship(back_populates='reviews')
    game: Mapped['Game'] = relationship(back_populates='reviews')

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'game_id'),
    )
