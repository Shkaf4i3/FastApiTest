from datetime import date
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from api_v1.users.schemas import User, UserUpdate
from api_v1.database_manager.models.users import Users
# from api_v1.database_manager.models.api_keys import ApiKeys


async def create_user(user: User, session: AsyncSession):
    exp = select(Users).where(Users.phone_number == user.phone.replace("tel:", ""))
    result = await session.execute(exp)

    try:
        if result.scalar():
            return {
                "success": False,
                "reason": "User alredy exists",
            }
        else:
            user_model = Users(
                first_name=user.first_name,
                last_name=user.last_name,
                phone_number=user.phone.replace("tel:", ""),
                email=user.email,
                source_id=user.source_id,
            )
            session.add(user_model)
            await session.commit()

            return {
                "success": True,
                "result": user.model_dump(),
            }
    except IntegrityError:
        return {
            f"User with source_id - {user.source_id} don't have the api key in DataBase",
        }


async def create_list_users(users: list[User], session: AsyncSession):
    result_users = []
    try:
        for user in users:
            phone_normalized = user.phone.replace("tel:", "")

            exp = select(Users).where(Users.phone_number == phone_normalized)
            result = await session.execute(exp)

            if result.scalar():
                await session.rollback()
                return {
                    "success": False,
                    "reason": f"User {user.phone} already exists",
                }

            user_model = Users(
                first_name=user.first_name,
                last_name=user.last_name,
                phone_number=phone_normalized,
                email=user.email,
                source_id=user.source_id,
            )
            session.add(user_model)
            result_users.append(user)

        await session.commit()
        return result_users
    except IntegrityError as e:
        await session.rollback()
        return {
            "success": False,
            "reason": f"Database integrity error: {str(e)}"
        }


async def get_users(
    session: AsyncSession,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    phone_prefix: Optional[str] = None,
    status_filter: Optional[str] = None,
):
    try:
        query = select(Users)

        if start_date:
            query = query.where(Users.created_at >= start_date)
        if end_date:
            query = query.where(Users.created_at <= end_date)
        if phone_prefix:
            query = query.where(Users.phone_number.startswith(phone_prefix))
        if status_filter:
            query = query.where(Users.status == status_filter)

        result = await session.execute(query)
        users = result.scalars().all()
        return users
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error",
        )


async def get_users_by_api_key(session: AsyncSession, source_id: int):
    exp = select(Users).where(Users.source_id == source_id)
    result = await session.execute(exp)
    return result.scalars().all()


async def update_status_user(user: UserUpdate, session: AsyncSession):
    exp = select(Users).where(Users.phone_number == user.phone.replace("tel:", ""))
    result = await session.execute(exp)
    user_result = result.scalar()

    if user_result:
        if user_result.status == user.status:
            return {
                "success": False,
                "reason": "This status already set",
            }
        else:
            exp_up = update(Users).where(
                Users.phone_number == user.phone.replace("tel:", "")
                ).values(status=user.status)
            await session.execute(exp_up)
            await session.commit()
            return {
                "success": True,
                "status": "Updated",
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
