from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..service import UserService, AuthService, PasswordService
from ..repo import UnitOfWork, UserRepo, AdminRepo
from ..deps import open_session


def get_admin_repo(session: Annotated[AsyncSession, Depends(open_session)]) -> AdminRepo:
    return AdminRepo(session=session)


def get_password_service() -> PasswordService:
    return PasswordService()


def get_user_service(session: Annotated[AsyncSession, Depends(open_session)]) -> UserService:
    return UserService(
        unit_of_work=UnitOfWork(session=session),
        user_repo=UserRepo(session=session),
    )


def get_auth_service(
    admin_repo: Annotated[AdminRepo, Depends(get_admin_repo)],
    password_service: Annotated[PasswordService, Depends(get_password_service)],
) -> AuthService:
    return AuthService(
        admin_repo=admin_repo,
        password_service=password_service,
    )
