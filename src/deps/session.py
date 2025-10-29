from core import db_manage


async def open_session():
    async with db_manage.session_factory() as session:
        yield session
