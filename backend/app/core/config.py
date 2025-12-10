from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Project EXi"
    ENVIRONMENT: str = "local"

    # DB
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "exi_user"
    POSTGRES_PASSWORD: str = "exi_password"
    POSTGRES_DB: str = "exi_db"

    # API key header names
    CLIENT_ID_HEADER: str = "x-client-id"
    API_KEY_HEADER: str = "x-api-key"

    class Config:
        env_file = ".env"


settings = Settings()
