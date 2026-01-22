from bcrypt import hashpw, gensalt, checkpw


class PasswordService:
    def get_password_hash(self, password: bytes) -> bytes:
        salt = gensalt()
        return hashpw(password=password, salt=salt)

    def check_password(self, plain_password: bytes, hashed_password: bytes) -> bool:
        return checkpw(password=plain_password, hashed_password=hashed_password)
