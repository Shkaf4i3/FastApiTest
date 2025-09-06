from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class User(BaseModel):
    first_name: str
    last_name: str
    phone: PhoneNumber
    email: EmailStr
    source_id: int


class UserUpdate(BaseModel):
    phone: PhoneNumber
    status: str
