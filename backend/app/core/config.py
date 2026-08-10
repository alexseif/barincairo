from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "BARINCAIRO.COM API"
    VERSION: str = "1.3.0"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "postgresql+asyncpg://barincairo_user:barincairo_password@db:5432/barincairo_db"
    SECRET_KEY: str = "super-secret-key-change-in-production"
    CORS_ORIGINS: List[str] = [
        "https://barincairo.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings: Settings = Settings()
