from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:////data/fastapi_db.sqlite3"

    model_config = SettingsConfigDict(env_file=".env")
