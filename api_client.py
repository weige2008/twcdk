# api_client.py - HTTP client for CDK mining (GitHub Actions)
# cdk_linux/api_client.py

import time
from typing import Optional

import requests
from loguru import logger

from .config import API_URL, API_TOKEN, WORKER_ID


class APIClient:
    def __init__(self, base_url: str = API_URL, token: str = API_TOKEN):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.worker_id = WORKER_ID
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "X-Worker-Id": self.worker_id,
        })

    def get_idle_account(self, retries: int = 3) -> Optional[dict]:
        url = f"{self.base_url}/api/accounts/get_idle"
        for attempt in range(1, retries + 1):
            try:
                resp = self.session.get(url, timeout=15)
                data = resp.json()
                if data.get("code") == 0:
                    return data["data"]
                if resp.status_code == 404:
                    return None
                time.sleep(2)
            except requests.RequestException as e:
                logger.warning(f"get_idle attempt {attempt}/{retries}: {e}")
                if attempt < retries:
                    time.sleep(3)
        return None

    def update_status(self, account_id: int, status: str, cdk: str = "") -> bool:
        url = f"{self.base_url}/api/accounts/update_status"
        try:
            resp = self.session.post(url, json={"account_id": account_id, "status": status, "cdk": cdk}, timeout=15)
            return resp.json().get("code") == 0
        except Exception as e:
            logger.warning(f"update_status failed: {e}")
            return False

    def send_heartbeat(self, account_id: int) -> bool:
        url = f"{self.base_url}/api/accounts/heartbeat"
        try:
            resp = self.session.post(url, json={"account_id": account_id, "worker_id": self.worker_id}, timeout=10)
            return resp.status_code == 200
        except Exception:
            return False

    def worker_heartbeat(self) -> bool:
        url = f"{self.base_url}/api/workers/heartbeat"
        try:
            resp = self.session.post(url, json={"worker_name": self.worker_id, "worker_type": "cdk"}, timeout=10)
            return resp.status_code == 200
        except Exception:
            return False

    def claim_cdk(self, cdk_code: str, game_name: str, account_id: int) -> bool:
        url = f"{self.base_url}/api/cdks/claim"
        try:
            resp = self.session.post(url, json={"cdk_code": cdk_code, "game_name": game_name, "account_id": account_id}, timeout=15)
            return resp.json().get("code") == 0
        except Exception:
            return False
