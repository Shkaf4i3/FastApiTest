from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from api_v1.database_manager.models.users import Users
from api_v1.database_manager.models.api_keys import ApiKeys
from api_v1.database_manager.models.base import Base
from api_v1.database_manager.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
