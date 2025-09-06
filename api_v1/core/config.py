from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "path to postgres dsn"


settings = Settings()
