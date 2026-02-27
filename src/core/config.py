from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    admin_login: str
    admin_password: str
    jwt_key: str
    jwt_algorithm: str
    dsn: PostgresDsn
    test_dsn: PostgresDsn
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
