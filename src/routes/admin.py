from typing import Annotated, Dict

from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from ..deps import services
from ..service import AuthService


router = APIRouter(prefix="/admin/auth", tags=["Admins Router"])


@router.post(path="/token", summary="Get access token", description="Get access token")
async def auth_user(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(services.get_auth_service)],
) -> Dict[str, bool]:
    exists_admin = await auth_service.auth_admin(
        login=form_data.username,
        password=form_data.password,
    )
    if not exists_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    data = {"sub": exists_admin.login}
    access_token = auth_service.create_access_token(data=data)
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=3600,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )
    return {"ok": True}
