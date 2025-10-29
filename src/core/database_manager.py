from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ..core import settings


class DataBaseManager:
    def __init__(self):
        self.session_engine = create_async_engine(
            url=settings.dsn.encoded_string(),
        )
        self.session_factory = async_sessionmaker(
            bind=self.session_engine,
        )

        self.test_session_engine = create_async_engine(
            url=settings.test_dsn.encoded_string(),
        )
        self.test_session_factory = async_sessionmaker(
            bind=self.test_session_engine,
        )


db_manage = DataBaseManager()
