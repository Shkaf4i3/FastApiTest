from ..repo import UserRepo, UnitOfWork, transactional
from ..model import User
from ..mappings import user_mapping
from ..dto import UserDto


class UserService:
    def __init__(self, unit_of_work: UnitOfWork, user_repo: UserRepo):
        self.unit_of_work = unit_of_work
        self.user_repo = user_repo


    @transactional
    async def create_user(self, dto: UserDto) -> UserDto | str:
        exist_user = await self.user_repo.get_user_by_email(email=dto.email)
        if exist_user:
            raise KeyError(f"User with email - {dto.email} already exists")

        new_user = User(username=dto.username, age=dto.age, email=dto.email)
        created_user = await self.user_repo.create_user(user=new_user)
        return user_mapping.mapping_user(user=created_user)


    async def get_user_by_email(self, email: str) -> UserDto | None:
        exist_user = await self.user_repo.get_user_by_email(email=email)
        if not exist_user:
            raise KeyError(f"User with email - {email} not found")

        return user_mapping.mapping_user(user=exist_user)


    @transactional
    async def delete_user_by_email(self, email: str) -> str:
        exist_user = await self.user_repo.get_user_by_email(email=email)
        if not exist_user:
            raise KeyError(f"User with email - {email} not found")
        await self.user_repo.delete_user(user=exist_user)
        return {
            "status": "Success",
            "message": f"User with email {email} successfully deleted",
        }

    async def get_list_users(self) -> list[UserDto] | None:
        users = await self.user_repo.get_list_users()
        if not users:
            return []
        return [user_mapping.mapping_user(user) for user in users]
