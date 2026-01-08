"""Application Configuration"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Smart Subway Guide API"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://subway:subway_dev_password@localhost:5432/subway_guide"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # 공공 데이터 API
    PUBLIC_API_KEY: str = ""
    PUBLIC_API_BASE_URL: str = "http://swopenAPI.seoul.go.kr/api/subway"

    # Cache TTL (seconds)
    ARRIVAL_CACHE_TTL: int = 30
    TRAVEL_AVG_CACHE_TTL: int = 3600
    STATION_INFO_CACHE_TTL: int = 86400

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()


settings = get_settings()
