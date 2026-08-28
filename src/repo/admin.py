from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..model import Admin


class AdminRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def create_admin(self, admin: Admin) -> Admin:
        self.session.add(instance=admin)
        await self.session.flush()
        await self.session.refresh(instance=admin)
        return admin


    async def get_admin_by_login(self, login: str) -> Admin | None:
        stmt = select(Admin).where(Admin.login == login)
        result = await self.session.execute(statement=stmt)
        return result.scalar()


    async def get_admin_by_password(self, password: str) -> Admin | None:
        stmt = select(Admin).where(Admin.password == password)
        result = await self.session.execute(statement=stmt)
        return result.scalar()
