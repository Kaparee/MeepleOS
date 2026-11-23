import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Table, Column, ForeignKey, String, Integer, SmallInteger, Numeric, Boolean, Text, DateTime, func, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), default=None)
    session_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("match_sessions.id", ondelete="SET NULL"), default=None)
    game_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), nullable=False)
    score: Mapped[Decimal] = mapped_column(Numeric(6, 4), nullable=False)
    algorithm_type: Mapped[str] = mapped_column(String(30), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    game: Mapped["Game"] = relationship("Game")
    user: Mapped["User | None"] = relationship("User")
    session: Mapped["MatchSession | None"] = relationship("MatchSession")
    feedback: Mapped["RecommendationFeedback | None"] = relationship("RecommendationFeedback", back_populates="recommendation", uselist=False)

class RecommendationFeedback(Base):
    __tablename__ = "recommendation_feedbacks"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    recommendation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("recommendations.id", ondelete="CASCADE"), unique=True, nullable=False)
    rating_stars: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    recommendation: Mapped["Recommendation"] = relationship("Recommendation", back_populates="feedback")
    __table_args__ = (
        CheckConstraint("rating_stars >= 1 AND rating_stars <= 5", name="chk_recommendation_feedback_stars"),
    )