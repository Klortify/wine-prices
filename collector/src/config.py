from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # -------------------------
    # Postgres
    # -------------------------
    postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "agri_db")
    postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    postgres_schema: str = os.getenv("POSTGRES_SCHEMA", "public")

    @property
    def postgres_dsn(self) -> str:
        return (
            f"dbname={self.postgres_db} "
            f"user={self.postgres_user} "
            f"password={self.postgres_password} "
            f"host={self.postgres_host} "
            f"port={self.postgres_port}"
        )

    # -------------------------
    # External API
    # -------------------------
    wine_api_base_url: str = os.getenv(
        "WINE_API_BASE_URL",
        "https://ec.europa.eu/agrifood/api/wine"
    )

    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "60"))


settings = Settings()