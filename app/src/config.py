from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn

class Settings(BaseSettings):
    # Database
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")  # Изменили на обычный str
    
    # RabbitMQ
    RABBITMQ_DEFAULT_USER: str = Field(..., env="RABBITMQ_DEFAULT_USER")
    RABBITMQ_DEFAULT_PASS: str = Field(..., env="RABBITMQ_DEFAULT_PASS")
    RABBITMQ_URL: str = Field(..., env="RABBITMQ_URL")

    # JWT
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()