from contextlib import asynccontextmanager

from fastapi import FastAPI

from model import User, Base
from core import db_manage


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    async with db_manage.session_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
