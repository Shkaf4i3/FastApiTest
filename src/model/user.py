from uuid import uuid4
from enum import Enum as enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Enum
from pydantic import EmailStr

from ..model import Base


class UserStatus(enum):
    USER = "user"
    SUPPORT = "support"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    username: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[EmailStr] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.USER)
