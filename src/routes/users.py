from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from ..dto import UserDto
from ..deps import services
from ..service import UserService
from ..model import UserStatus


router = APIRouter(prefix="/users", tags=["Users Router"])


@router.post(
    path="/create_user/",
    summary="Create User",
    description="Create new User with transmitted dto model",
)
async def create_user(
    dto: UserDto,
    user_service: Annotated[UserService, Depends(services.get_user_service)],
) -> UserDto | dict[str, str]:
    try:
        new_user = await user_service.create_user(dto=dto)
        return new_user
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    path="/get_user/{email}",
    summary="Get User",
    description="Get User from db by email",
)
async def get_user_by_email(
    email: str,
    user_service: Annotated[UserService, Depends(services.get_user_service)],
) -> UserDto | dict[str, str]:
    try:
        exists_user = await user_service.get_user_by_email(email=email)
        return exists_user
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    path="/delete_user/{email}",
    summary="Delete User",
    description="Delete User from db by email",
)
async def delete_user_by_email(
    email: str,
    user_service: Annotated[UserService, Depends(services.get_user_service)],
) -> dict[str, str]:
    try:
        return await user_service.delete_user_by_email(email=email)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    path="/get_list_users/",
    summary="Get Users",
    description="Get list Users from db",
    response_model=list[UserDto],
)
async def get_list_users(
    user_service: Annotated[UserService, Depends(services.get_user_service)],
) -> list[UserDto]:
    try:
        users = await user_service.get_list_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch(
    path="/update_status_user",
    summary="Update User",
    description="Update User by status",
)
async def update_status_user(
    status_user: UserStatus,
    email: str,
    user_service: Annotated[UserService, Depends(services.get_user_service)],
) -> UserDto | dict[str, str]:
    try:
        user = await user_service.update_user(status=status_user, email=email)
        return user
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
