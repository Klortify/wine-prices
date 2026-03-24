import requests
from config import settings

BASE_URL = settings.wine_api_base_url


class WineAPIClient:
    def __init__(self, timeout: int = 60):
        self.session = requests.Session()
        self.timeout = timeout

    def get_prices(self) -> list[dict]:
        url = f"{BASE_URL}/prices"
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()