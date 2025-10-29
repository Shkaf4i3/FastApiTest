from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from pydantic import EmailStr

from ..model import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    username: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[EmailStr] = mapped_column(String, nullable=False, unique=True)
