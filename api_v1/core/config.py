from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "path to own db"
    test_db_url: str = "path to test db"


settings = Settings()
