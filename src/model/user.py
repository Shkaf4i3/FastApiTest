from uuid import uuid4
from enum import Enum as enum
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Enum, DateTime
from pydantic import EmailStr

from .base import Base


class UserStatus(enum):
    USER = "user"
    SUPPORT = "support"


class User(Base):
    __tablename__ = "Users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    username: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[EmailStr] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.USER)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(tz=timezone.utc),
        nullable=False,
    )
