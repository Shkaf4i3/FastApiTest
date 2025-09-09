from datetime import date
from typing import AsyncGenerator, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api_v1.users.schemas import User, UserUpdate
from api_v1.database_manager.models.api_keys import ApiKeys
from api_v1.database_manager.db_helper import db_helper
from api_v1.users import crud


router = APIRouter(prefix="/app", tags=["Users"])


async def open_session() -> AsyncGenerator[Any, Any]:
    async with db_helper.session_factory() as session:
        yield session
        await session.close()


async def validate_api_key(
        api_key: str,
        session: AsyncSession = Depends(open_session)
) -> str | HTTPException:
    exp = select(ApiKeys).where(ApiKeys.api_key == api_key)
    result = await session.execute(exp)

    if result.scalar():
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect api_key",
        )


@router.post(path="/create_user/", description="Create User")
async def create_user(
    user: User,
    session: AsyncSession = Depends(open_session),
    api_key: str = Depends(validate_api_key),
):
    return await crud.create_user(user=user, session=session)


@router.post(
        path="/create_list_users/",
        description="Create list Users",
        response_model=list[User] | dict[str, bool| str]
)
async def create_list_users(
    users: list[User],
    session: AsyncSession = Depends(open_session),
    api_key: str = Depends(validate_api_key),
    ):
    return await crud.create_list_users(users=users, session=session)


@router.get(path="/get_user/", description="Get Users by optional filters")
async def get_users(
    session: AsyncSession = Depends(open_session),
    api_key: str = Depends(validate_api_key),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    phone_prefix: Optional[str] = None,
    status_filter: Optional[str] = None,
):
    """
    Get users by optional parameters

    important: - phone number sending in format "+7-906-e.t.c"
    """
    return await crud.get_users(
        session=session,
        start_date=start_date,
        end_date=end_date,
        phone_prefix=phone_prefix,
        status_filter=status_filter,
    )


@router.get(path="/get_user_by_api_key/", description="Get Users by api key")
async def get_users_by_api_key(
    source_id: int,
    api_key: str = Depends(validate_api_key),
    session: AsyncSession = Depends(open_session),

):
    """
    In field "source_id" send id, which set in Users Table(foreign key for ApiKeys Table)
    """
    return await crud.get_users_by_api_key(session=session, source_id=source_id)


@router.patch(path="/update_status_user/", description="Update status Users")
async def update_status_user(
    user: UserUpdate,
    session: AsyncSession = Depends(open_session),
    api_key: str = Depends(validate_api_key),
):
    return await crud.update_status_user(user=user, session=session)
