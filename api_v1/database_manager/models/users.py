from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from api_v1.database_manager.models.base import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default="NEW")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    source_id: Mapped[int] = mapped_column(ForeignKey(column="api_keys.source_id"))
