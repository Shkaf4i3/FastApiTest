from sqlalchemy.orm import Mapped, mapped_column

from api_v1.database_manager.models.base import Base


class ApiKeys(Base):
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(primary_key=True)
    api_key: Mapped[str] = mapped_column(nullable=False)
    source_id: Mapped[int] = mapped_column(unique=True)
