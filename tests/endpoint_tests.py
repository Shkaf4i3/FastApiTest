from typing import Any, AsyncGenerator

from pytest_asyncio import fixture
from pytest import mark
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from httpx import AsyncClient, ASGITransport

from api_v1.users.views import open_session
from tests.test_db_manager.test_db_helper import test_db_helper
from tests.test_db_manager.models.users import Users
from tests.test_db_manager.models.api_keys import ApiKeys
from tests.test_db_manager.models.base import Base
from api_v1.users.schemas import User, UserUpdate
from main import app as router


api_key = "testkey" # api_key should be getted from db


@fixture(autouse=True, loop_scope="module")
async def create_tables():
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@fixture(loop_scope="module")
async def session() -> AsyncGenerator[AsyncSession, Any]:
    async with test_db_helper.session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


@fixture(loop_scope="module")
async def client(session: AsyncSession):
    async def override_open_session():
        yield session
        await session.close()

    router.dependency_overrides[open_session] = override_open_session
    async with AsyncClient(transport=ASGITransport(app=router), base_url="http://app.io") as client:
        yield client

        router.dependency_overrides.clear()


@mark.asyncio(loop_scope="module")
async def test_success_create_user(client: AsyncClient, session: AsyncSession):
    params = {
        "api_key": api_key,
    }

    data = User(
        first_name="John",
        last_name="Bishop",
        phone="+79614781972",
        email="origin@example.com",
        source_id=1,
    )
    exp = select(Users).where(Users.phone_number == data.phone.replace("tel:", ""))
    result = await session.execute(exp)

    response = await client.post(
        url="/app/create_user/",
        json=data.model_dump(), params=params,
    )

    try:
        if result.scalar():
            assert response.json() == {"success": False, "reason": "User alredy exists"}
        else:
            assert response.status_code == 200
            assert response.json() == {"success": True, "result": data.model_dump()}
    except IntegrityError:
        assert response.json() == {
            f"User with source_id - {data.source_id} don't have the api key in DataBase",
            }


@mark.asyncio(loop_scope="module")
async def test_success_create_list_users(client: AsyncClient, session: AsyncSession):
    params = {
        "api_key": api_key,
    }

    users = [
        User(
            first_name="Bob",
            last_name="Posik",
            phone="+79884681702",
            email="flexim@yandex.ru",
            source_id=1,
        ),
        User(
            first_name="Michael",
            last_name="Nikola",
            phone="+78699604738",
            email="mikola@gmail.com",
            source_id=1,
        ),
    ]
    data = [user.model_dump() for user in users]

    existing_users = []
    for user in users:
        phone_normalized = user.phone.replace("tel:", "")
        exp = select(Users).where(Users.phone_number == phone_normalized)
        result = await session.execute(exp)
        if result.scalar():
            existing_users.append(user.phone)

    response = await client.post(
        url="/app/create_list_users/",
        json=data,
        params=params,
    )

    if existing_users:
        assert response.json()["success"] is False
        assert any(phone in response.json()["reason"] for phone in existing_users)
    else:
        assert response.status_code == 200
        assert response.json() == data


@mark.asyncio(loop_scope="module")
async def test_get_users(
    client: AsyncClient,
    session: AsyncSession,
):
    params = {
        "api_key": api_key,
    }

    response = await client.get(
        url="/app/get_user/",
        params=params,
    )

    try:
        assert response.status_code == 200
    except Exception:
        assert response.status_code == 500


@mark.asyncio(loop_scope="module")
async def test_get_users_by_api_key(
    client: AsyncClient,
    session: AsyncSession,
):
    params = {
        "source_id": 1,
        "api_key": api_key
    }

    exp = select(Users).where(Users.source_id == params["source_id"])
    result = await session.execute(exp)
    users = result.scalars().all()

    expected_users = []
    for user in users:
        user_dict = {
            "id": user.id,
            "phone_number": user.phone_number,
            "status": user.status,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "created_at": user.created_at.isoformat(),
            "source_id": user.source_id
        }
        expected_users.append(user_dict)

    response = await client.get(
        url="/app/get_user_by_api_key/",
        params=params,
    )

    assert response.status_code == 200
    assert response.json() == expected_users


@mark.asyncio(loop_scope="module")
async def test_update_status_user(
    client: AsyncClient,
    session: AsyncSession,
):
    params = {
        "api_key": api_key,
    }
    data = {
        "user": UserUpdate(
            phone="+79614781972",
            status="OLD",
        )
    }

    exp = select(Users).where(Users.phone_number == data["user"].phone.replace("tel:", ""))
    result = await session.execute(exp)
    user_result = result.scalar()

    response = await client.patch(
        url="/app/update_status_user/",
        params=params,
        json=data["user"].model_dump(),
    )

    if user_result:
        if user_result.status == data["user"].status:
            assert response.json() == {"success": False, "reason": "This status already set",}
        else:
            assert response.json() == {"success": True, "status": "Updated",}
    else:
        assert response.status_code == 404
