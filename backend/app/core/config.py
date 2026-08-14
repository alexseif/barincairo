import os
from pathlib import Path

from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env" if (BASE_DIR / ".env").exists() else BASE_DIR.parent / ".env"


class Settings(BaseSettings):
    PROJECT_NAME: str = "BARINCAIRO.COM API"
    VERSION: str = "1.3.0"
    API_V1_STR: str = "/api/v1"

    POSTGRES_USER: str = "barincairo_user"
    POSTGRES_PASSWORD: str = "change_me_in_env"
    POSTGRES_DB: str = "barincairo_db"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    DATABASE_URL: str = ""
    SECRET_KEY: str = "change_me_in_env"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = [
        "https://barincairo.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> str:
        if isinstance(v, str) and v.strip():
            url = v
        else:
            user = info.data.get("POSTGRES_USER", "barincairo_user")
            password = info.data.get("POSTGRES_PASSWORD", "change_me_in_env")
            host = info.data.get("POSTGRES_HOST", "db")
            port = info.data.get("POSTGRES_PORT", 5432)
            db = info.data.get("POSTGRES_DB", "barincairo_db")
            url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

        if "@db:" in url and not os.path.exists("/.dockerenv"):
            url = url.replace("@db:", "@127.0.0.1:")
        return url

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH) if ENV_FILE_PATH.exists() else ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings: Settings = Settings()
