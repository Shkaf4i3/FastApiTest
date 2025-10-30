from ..model import User
from ..dto import UserDto


def mapping_user(user: User) -> UserDto:
    return UserDto(
        username=user.username,
        age=user.age,
        email=user.email,
        status=user.status
    )
