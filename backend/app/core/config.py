import json
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ============================================================
    # App
    # ============================================================
    APP_NAME: str = "MedAssist AI"
    ENV: str = "production"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # ============================================================
    # JWT
    # ============================================================
    JWT_SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080

    # ============================================================
    # MySQL
    # ============================================================
    DATABASE_URL: str | None = None

    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DB: str = "railway"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306

    # ============================================================
    # MongoDB
    # ============================================================
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "medassist_logs"

    # ============================================================
    # CORS
    # ============================================================
    CORS_ORIGINS: str | list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://med-assist-ai-mekalacybersecurity.vercel.app",
        "https://med-assist-ai-mekala123.vercel.app",
    ]

    @property
    def parsed_cors_origins(self) -> list[str]:
        if isinstance(self.CORS_ORIGINS, str):
            try:
                return json.loads(self.CORS_ORIGINS)
            except (ValueError, TypeError):
                return [
                    origin.strip()
                    for origin in self.CORS_ORIGINS.split(",")
                    if origin.strip()
                ]

        return self.CORS_ORIGINS

    # ============================================================
    # Database URL
    # ============================================================
    @property
    def SQL_DATABASE_URI(self) -> str:
        """
        AWS production SHOULD use DATABASE_URL.
        Local development can use individual MYSQL_* variables.
        """

        if self.DATABASE_URL:
            url = self.DATABASE_URL.strip()

            # Optional format conversion for aiomysql
            if url.startswith("mysql://"):
                url = url.replace(
                    "mysql://",
                    "mysql+aiomysql://",
                    1,
                )

            elif url.startswith("mysql+pymysql://"):
                url = url.replace(
                    "mysql+pymysql://",
                    "mysql+aiomysql://",
                    1,
                )

            elif not url.startswith("mysql+aiomysql://"):
                raise RuntimeError(
                    "Invalid DATABASE_URL format. "
                    "Expected mysql:// or mysql+aiomysql://"
                )

            return url

        # Fall back to individual components if DATABASE_URL is not set
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"

    # ============================================================
    # Pydantic Settings
    # ============================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
