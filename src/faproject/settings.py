from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "BStore"
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key"  # Move to environment variables

    class Config:
        case_sensitive = True


settings = Settings()
