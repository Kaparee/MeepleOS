import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Table, Column, ForeignKey, String, Integer, SmallInteger, Numeric, Boolean, Text, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

game_mechanics = Table("game_mechanics",
    Base.metadata,
            Column("mechanic_id", ForeignKey("mechanics.id", ondelete="CASCADE"), primary_key=True),
                  Column("game_id", ForeignKey("games.id", ondelete="CASCADE"), primary_key=True)
)

game_categories = Table("game_categories",
    Base.metadata,
            Column("game_id", ForeignKey("games.id", ondelete="CASCADE"), primary_key=True),
                  Column("category_id", ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True)
)

class Mechanic(Base):
    __tablename__ = "mechanics"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    bgg_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    group_name: Mapped[str | None] = mapped_column(String(50), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    games: Mapped[list["Game"]] = relationship(secondary=game_mechanics, back_populates="mechanics")
    __table_args__ = (
        Index("uq_mechanics_bgg_id", bgg_id, unique=True, postgresql_where=(deleted_at.is_(None))),
    )

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    bgg_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    games: Mapped[list["Game"]] = relationship(secondary=game_categories, back_populates="categories")
    __table_args__ = (
        Index("uq_categories_bgg_id", bgg_id, unique=True, postgresql_where=(deleted_at.is_(None))),
    )

class Game(Base):
    __tablename__ = "games"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    bgg_id: Mapped[int] = mapped_column(nullable=False)
    parent_game_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("games.id"), default=None)
    is_expansion: Mapped[bool] = mapped_column(Boolean, default=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    polish_title: Mapped[str | None] = mapped_column(String(255))
    text_heaviness: Mapped[int | None] = mapped_column(SmallInteger, default=None)
    tutorial_video_url_pl : Mapped[str | None] = mapped_column(String(500))
    tutorial_video_url_eng : Mapped[str | None] = mapped_column(String(500))
    publisher: Mapped[str | None] = mapped_column(String(255))
    designer: Mapped[str | None] = mapped_column(String(255))
    min_player: Mapped[int | None] = mapped_column(Integer)
    max_player: Mapped[int | None] = mapped_column(Integer)
    optimal_player: Mapped[int | None] = mapped_column(Integer)
    community_players_min : Mapped[int | None] = mapped_column(Integer)
    community_players_max: Mapped[int | None] = mapped_column(Integer)
    min_age: Mapped[int | None] = mapped_column(Integer)
    community_min_age: Mapped[int | None] = mapped_column(Integer)
    min_playtime: Mapped[int | None] = mapped_column(Integer)
    max_playtime: Mapped[int | None] = mapped_column(Integer)
    optimal_playtime: Mapped[int | None] = mapped_column(Integer)
    weight: Mapped[Decimal | None] = mapped_column(Numeric(6, 4))
    bayes_avg: Mapped[Decimal | None] = mapped_column(Numeric(6, 4))
    stddev: Mapped[Decimal | None] = mapped_column(Numeric(6, 4))
    bgg_rank: Mapped[int | None] = mapped_column(Integer)
    users_rated: Mapped[int | None] = mapped_column(Integer)
    year_published: Mapped[int | None] = mapped_column(Integer)
    image_url: Mapped[str | None] = mapped_column(Text)
    thumbnail_url: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    local_play_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    local_avg_playtime: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    local_avg_rating: Mapped[Decimal | None] = mapped_column(Numeric(4, 2))
    local_rating_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    expansions: Mapped[list["Game"]] = relationship("Game", back_populates="parent_game")
    parent_game: Mapped["Game | None"] = relationship("Game", back_populates="expansions", remote_side=[id])
    mechanics: Mapped[list["Mechanic"]] = relationship(secondary=game_mechanics, back_populates="games")
    categories: Mapped[list["Category"]] = relationship(secondary=game_categories, back_populates="games")
    owned: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)
    shelf_of_shame_index: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)
    __table_args__ = (
        Index("uq_games_bgg_id", bgg_id, unique=True, postgresql_where=(deleted_at.is_(None))),
    )

