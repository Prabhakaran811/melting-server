
# from functools import lru_cache

# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     APP_NAME: str = "Melting MES API"
#     APP_VERSION: str = "1.0.0"
#     API_V1_PREFIX: str = "/api/v1"

#     DATABASE_URL: str

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         case_sensitive=True,
#         extra="ignore",
#     )


# @lru_cache
# def get_settings() -> Settings:
#     return Settings()


# settings = get_settings()



from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Melting MES API"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str

    # Initial Admin Details
    ADMIN_EMPLOYEE_ID: str
    ADMIN_FULL_NAME: str
    ADMIN_EMAIL: str
    ADMIN_PHONE: str
    ADMIN_PASSWORD: str

    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
