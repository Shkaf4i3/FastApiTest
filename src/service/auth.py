from datetime import datetime, timezone, timedelta

from jwt import encode

from ..model import Admin
from ..repo import AdminRepo
from ..service import PasswordService


class AuthService:
    def __init__(self, admin_repo: AdminRepo, password_service: PasswordService):
        self.admin_repo = admin_repo
        self.password_service = password_service


    async def auth_admin(self, login: str, password: str) -> Admin | None:
        exists_admin = await self.admin_repo.get_admin_by_login(login=login)
        if not exists_admin:
            return None
        if not self.password_service.check_password(
            plain_password=password.encode(),
            hashed_password=exists_admin.password,
        ):
            return None

        return exists_admin


    def create_access_token(self, data: dict) -> str:
        copy_dict = data.copy()
        expires = datetime.now(tz=timezone.utc) + timedelta(seconds=3600)
        copy_dict.update({"exp": expires})
        return encode(
            payload=copy_dict,
            key="AAAA",
            algorithm="HS256",
        )
