from typing import Annotated, Any

from jwt import decode
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from ..model import Admin
from ..repo import AdminRepo
from ..core import settings
from .services import get_admin_repo


class TokenData(BaseModel):
    login: str | None = None
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/auth/token")


async def get_oauth2_scheme(token: Annotated[str, Depends(oauth2_scheme)]):
    if not token:
        raise credentials_exception
    return token


async def get_current_user(
    token: Annotated[str, Depends(get_oauth2_scheme)],
    admin_repo: Annotated[AdminRepo, Depends(get_admin_repo)],
) -> Admin:
    try:
        payload: dict[str, Any] = decode(
            jwt=token,
            key=settings.jwt_key,
            algorithms=[settings.jwt_algorithm],
        )
        login: str | None = payload.get("sub")
        if not login:
            raise credentials_exception
        token_data = TokenData(login=login)
    except InvalidTokenError:
        raise credentials_exception
    exists_admin = await admin_repo.get_admin_by_login(login=token_data.login)
    if not exists_admin:
        raise credentials_exception
    return exists_admin
