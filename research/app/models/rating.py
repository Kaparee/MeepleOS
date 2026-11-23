import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Table, Column, ForeignKey, String, Integer, SmallInteger, Numeric, Boolean, Text, DateTime, func, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class UserRating(Base):
    __tablename__ = "user_ratings"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    game_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), primary_key=True)
    rating: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user: Mapped["User"] = relationship("User")
    game: Mapped["Game"] = relationship("Game")
    __table_args__ = (
        CheckConstraint("rating >= 1.0 AND rating <= 10.0", name="chk_user_ratings_range"),
    )