import uuid
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Table, Column, ForeignKey, String, Integer, SmallInteger, Numeric, Boolean, Text, DateTime, Date, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    qr_hmac_secret: Mapped[str | None] = mapped_column(String(64))
    nickname: Mapped[str | None] = mapped_column(String(20), default=None)
    name: Mapped[str | None] = mapped_column(String(50), default=None)
    surname: Mapped[str | None] = mapped_column(String(50), default=None)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(50), default=None, nullable=True)
    hash_password: Mapped[str | None] = mapped_column(String(255), default=None)
    birth_date: Mapped[date | None] = mapped_column(Date, default=None)
    verification_code: Mapped[str | None] = mapped_column(String(255))
    reset_password_code: Mapped[str | None] = mapped_column(String(255))
    account_status: Mapped[str] = mapped_column(String(20), default="normal")
    user_role: Mapped[str] = mapped_column(String(20), default="customer")
    experience_points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    verification_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    reset_token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    __table_args__ = (
        Index(
           "uq_users_nickname",
            nickname,
            unique=True,
            postgresql_where=(deleted_at.is_(None))
        ),
        Index(
            "uq_users_email",
            email,
            unique=True,
            postgresql_where=(deleted_at.is_(None))
        ),
        Index(
            "uq_users_phone",
            phone_number,
            unique=True,
            postgresql_where=(deleted_at.is_(None))
        )
    )