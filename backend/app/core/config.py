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

    # Google Sheets
    GOOGLE_SERVICE_ACCOUNT_FILE: str | None = None  # path to service account JSON

    # Sheet sync
    SHEET_SYNC_INTERVAL_SECONDS: int = 300  # 5 minutes

    # Qdrant
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_RENTALS: str = "rentals"
    QDRANT_EMBED_DIM: int = 768

    class Config:
        env_file = ".env"


settings = Settings()
