from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    environment: str = Field("development")
    db_url: SecretStr = Field(..., description="Database connection URL")
    db_pool_size: int = Field(8)
    port: int = Field(8080, description="Web-server listening port")


settings = Settings()
