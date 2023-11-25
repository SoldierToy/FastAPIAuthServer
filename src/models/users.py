import uuid
from typing import List

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tg_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    token: Mapped['RefreshTokens'] = relationship(back_populates='user', cascade='delete')
    role: Mapped[str] = mapped_column(nullable=False)


class RefreshTokens(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(primary_key=True)
    refresh_token: Mapped[str] = mapped_column(unique=True)
    user: Mapped["Users"] = relationship(back_populates='token')
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id'))
