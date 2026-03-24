from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # -------------------------
    # External API
    # -------------------------
    wine_api_base_url: str = os.getenv(
        "WINE_API_BASE_URL",
        "https://ec.europa.eu/agrifood/api/wine"
    )

    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "60"))

    # -------------------------
    # Repository Service
    # -------------------------
    repository_url: str = os.getenv("REPOSITORY_URL", "http://repository:8000")

    # -------------------------
    # RabbitMQ
    # -------------------------
    rabbitmq_host: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
    rabbitmq_port: int = int(os.getenv("RABBITMQ_PORT", "5672"))
    rabbitmq_user: str = os.getenv("RABBITMQ_USER", "wineapp")
    rabbitmq_password: str = os.getenv("RABBITMQ_PASSWORD", "wineapp")
    rabbitmq_exchange: str = os.getenv("RABBITMQ_EXCHANGE", "agri.events")

    @property
    def rabbitmq_url(self) -> str:
        return (
            f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}"
            f"@{self.rabbitmq_host}:{self.rabbitmq_port}/"
        )



settings = Settings()