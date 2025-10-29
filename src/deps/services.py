from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from service import UserService
from repo import UnitOfWork, UserRepo
from deps import open_session


def get_user_service(session: AsyncSession = Depends(open_session)) -> UserService:
    return UserService(
        unit_of_work=UnitOfWork(session=session),
        user_repo=UserRepo(session=session),
    )
