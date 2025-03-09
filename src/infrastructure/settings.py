from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=Path(BASE_DIR, ".env"),
    )

    REDIS_URL: str = 'redis://localhost:6381/0'


settings = Settings()  # noqa
