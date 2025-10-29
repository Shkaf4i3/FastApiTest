from pytest_asyncio import fixture
from pytest import mark
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import User, Base
from src.core import db_manage
from src.service import UserService
from src.repo import UnitOfWork, UserRepo
from src.dto import UserDto


# Fixtures
@fixture(autouse=True, loop_scope="module")
async def test_engine():
    async with db_manage.test_session_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_manage.test_session_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@fixture(loop_scope="module")
async def test_session():
    async with db_manage.test_session_factory() as session:
        yield session
        await session.close()

@fixture(loop_scope="module")
async def get_user_repo(test_session: AsyncSession) -> UserRepo:
    return UserRepo(session=test_session)

@fixture(loop_scope="module")
async def get_test_user_service(test_session: AsyncSession) -> UserService:
    return UserService(
        unit_of_work=UnitOfWork(session=test_session),
        user_repo=UserRepo(session=test_session),
    )


@fixture
def get_user() -> UserDto:
    return UserDto(username="Test", age=56, email="fleximes@yandex.ru")


# Tests
@mark.asyncio(loop_scope="module")
async def test_create_user(
    get_test_user_service: UserService,
    get_user_repo: UserRepo,
    get_user: UserDto,
) -> None:
    await get_test_user_service.create_user(dto=get_user)
    exists_user = await get_user_repo.get_user_by_email(email=get_user.email)

    assert get_user.email == exists_user.email
    assert get_user.age == exists_user.age
    assert get_user.username == exists_user.username


@mark.asyncio(loop_scope="module")
async def test_get_list_users(
    get_test_user_service: UserService,
    get_user_repo: UserRepo,
) -> None:
    users: list[UserDto] = []

    for i in range(0, 5):
        new_user = UserDto(username=f"Test_{i}", age=i, email=f"flexime{i}@yandex.ru")
        users.append(new_user)

    for user in users:
        await get_test_user_service.create_user(dto=user)

    created_users = await get_user_repo.get_list_users()
    assert created_users != []


@mark.asyncio(loop_scope="module")
async def test_get_user_by_email(
    get_test_user_service: UserService,
    get_user_repo: UserRepo,
    get_user: UserDto,
):
    await get_test_user_service.create_user(dto=get_user)

    created_user = await get_user_repo.get_user_by_email(email=get_user.email)
    assert get_user.email == created_user.email
