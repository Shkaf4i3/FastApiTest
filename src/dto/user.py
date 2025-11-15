from pydantic import BaseModel, EmailStr

from ..model import UserStatus


class UserDto(BaseModel):
    username: str
    age: int
    email: EmailStr
    status: UserStatus | None = None
