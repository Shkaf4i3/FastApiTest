from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api_v1.core.config import settings


class TestDBHelper:
    def __init__(self):
        self.engine = create_async_engine(
            url=settings.test_db_url,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
        )


test_db_helper = TestDBHelper()
