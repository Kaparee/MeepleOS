import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Table, Column, ForeignKey, String, Integer, SmallInteger, Numeric, Boolean, Text, DateTime, func, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class MatchSession(Base):
    __tablename__ = "match_sessions"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    game_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), nullable=False)
    host_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    chosen_recommendation_id: Mapped[uuid.UUID | None] = mapped_column(default=None)
    played_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    duration_minutes: Mapped[int | None] = mapped_column(Integer, default=None)
    predicted_duration_minutes: Mapped[int | None] = mapped_column(Integer, default=None)
    status: Mapped[str] = mapped_column(String(20), default="in_progress")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    game: Mapped["Game"] = relationship("Game")
    host: Mapped["User"] = relationship("User")
    scores: Mapped[list["MatchScore"]] = relationship("MatchScore", back_populates="session", cascade="all, delete-orphan")

class MatchScore(Base):
    __tablename__ = "match_scores"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    match_session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("match_sessions.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    score: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), default=None)
    result: Mapped[str] = mapped_column(String(20), nullable=False)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    session: Mapped["MatchSession"] = relationship("MatchSession", back_populates="scores")
    user: Mapped["User"] = relationship("User")
    __table_args__ = (
        Index("uq_match_scores_session_user", match_session_id, user_id, unique=True),
    )
