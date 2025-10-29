from pydantic import BaseModel, EmailStr


class UserDto(BaseModel):
    username: str
    age: int
    email: EmailStr
