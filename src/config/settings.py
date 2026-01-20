from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr


class Settings(BaseSettings):
    environment: str = Field("development")
    db_url: SecretStr = Field(..., description="Database connection URL")
    db_pool_size: int = Field(8)


settings = Settings(_env_file=(".env", ".env.local", ".env.dev", ".env.prod"), _env_file_encoding="utf-8")
