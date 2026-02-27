from contextlib import asynccontextmanager

from fastapi import FastAPI

from ..model import Base, Admin
from ..service import PasswordService
from ..repo import AdminRepo
from ..core import db_manage, settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with db_manage.session_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with db_manage.session_factory.begin() as session:
        admin_repo = AdminRepo(session=session)
        exists_user = await admin_repo.get_admin_by_login(login=settings.admin_login)
        if not exists_user:
            password_service = PasswordService()
            hashed_password = password_service.get_password_hash(
                password=settings.admin_password.encode(),
            )
            new_admin = Admin(login=settings.admin_login, password=hashed_password)
            session.add(new_admin)
            await session.flush()
            await session.refresh(new_admin)
            await session.commit()
    yield
