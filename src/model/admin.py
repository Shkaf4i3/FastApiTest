from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, LargeBinary

from ..model import Base


class Admin(Base):
    __tablename__ = "Admins"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    login: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
