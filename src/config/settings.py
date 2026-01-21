from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr


PROJECT_ROOT = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    environment: str = Field("development")
    db_url: SecretStr = Field(..., description="Database connection URL")
    db_pool_size: int = Field(8)


settings = Settings(
    _env_file=(
        PROJECT_ROOT / ".env",
        PROJECT_ROOT / ".env.local",
        PROJECT_ROOT / ".env.dev",
        PROJECT_ROOT / ".env.prod",
    ),
    _env_file_encoding="utf-8",
)
