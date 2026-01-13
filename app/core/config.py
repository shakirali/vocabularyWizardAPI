from typing import List

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    Copy .env.example to .env and configure your values.
    """

    # Database (required)
    DATABASE_URL: str

    # Security - SECRET_KEY is required, must be set in .env
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # Environment: development, staging, production (required)
    ENVIRONMENT: str

    # API
    API_V1_PREFIX: str = "/api/v1"

    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gemma2:2b"
    OLLAMA_TIMEOUT: int = 30

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @model_validator(mode="after")
    def validate_production_settings(self):
        """Ensure production environment has proper configuration."""
        if self.ENVIRONMENT == "production":
            if "sqlite" in self.DATABASE_URL.lower():
                raise ValueError(
                    "SQLite cannot be used in production. "
                    "Set DATABASE_URL to a PostgreSQL connection string."
                )
            if "*" in self.CORS_ORIGINS:
                raise ValueError(
                    "CORS_ORIGINS cannot contain '*' in production. "
                    "Specify allowed origins explicitly."
                )
        return self


settings = Settings()
