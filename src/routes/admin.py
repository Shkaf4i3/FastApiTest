from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..dto import TokenResult
from ..deps import services
from ..service import AuthService


router = APIRouter(prefix="/admin/auth", tags=["Admins Router"])


@router.post(path="/token", summary="Get access token", description="Get access token")
async def auth_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(services.get_auth_service)],
) -> TokenResult:
    exists_admin = await auth_service.auth_admin(login=form_data.username, password=form_data.password)
    if not exists_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    data = {"sub": exists_admin.login}
    access_token = auth_service.create_access_token(data=data)
    return TokenResult(access_token=access_token)
