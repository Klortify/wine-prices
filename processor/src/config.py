from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    # -------------------------
    # Repository Service
    # -------------------------
    repository_url: str = os.getenv("REPOSITORY_URL", "http://repository:8000")

    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "60"))

    # -------------------------
    # RabbitMQ
    # -------------------------
    rabbitmq_host: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
    rabbitmq_port: int = int(os.getenv("RABBITMQ_PORT", "5672"))
    rabbitmq_user: str = os.getenv("RABBITMQ_USER", "wineapp")
    rabbitmq_password: str = os.getenv("RABBITMQ_PASSWORD", "wineapp")
    rabbitmq_exchange: str = os.getenv("RABBITMQ_EXCHANGE", "agri.events")


settings = Settings()
