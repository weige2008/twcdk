import time
from typing import Optional
import requests
from loguru import logger
from .MlXQfWNy import API_URL, API_TOKEN, WORKER_ID

class jnyRVBYj:

    def __init__(self, base_url: str=API_URL, token: str=API_TOKEN):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.worker_id = WORKER_ID
        self.session = requests.Session()
        self.session.headers.update({__import__('base64').b64decode('QXV0aG9yaXphdGlvbg==').decode(): f'Bearer {self.token}', 'Content-Type': 'application/json', __import__('base64').b64decode('WC1Xb3JrZXItSWQ=').decode(): self.worker_id})

    def get_idle_account(self, retries: int=3) -> Optional[dict]:
        url = f'{self.base_url}/api/accounts/get_idle'
        for attempt in range(1, retries + 1):
            try:
                resp = self.session.get(url, timeout=15)
                data = resp.json()
                if data.get('code') == 0:
                    return data['data']
                if resp.status_code == 404:
                    return None
                time.sleep(2)
            except requests.RequestException as e:
                logger.warning(f'get_idle attempt {attempt}/{retries}: {e}')
                if attempt < retries:
                    time.sleep(3)
        return None

    def update_status(self, account_id: int, status: str, cdk: str='') -> bool:
        url = f'{self.base_url}/api/accounts/update_status'
        try:
            resp = self.session.post(url, json={'account_id': account_id, 'status': status, __import__('base64').b64decode('Y2Rr').decode(): cdk}, timeout=15)
            return resp.json().get('code') == 0
        except Exception as e:
            logger.warning(f'update_status failed: {e}')
            return False

    def send_heartbeat(self, account_id: int) -> bool:
        url = f'{self.base_url}/api/accounts/heartbeat'
        try:
            resp = self.session.post(url, json={'account_id': account_id, __import__('base64').b64decode('d29ya2VyX2lk').decode(): self.worker_id}, timeout=10)
            return resp.status_code == 200
        except Exception:
            return False

    def worker_heartbeat(self) -> bool:
        url = f'{self.base_url}/api/workers/heartbeat'
        try:
            resp = self.session.post(url, json={__import__('base64').b64decode('d29ya2VyX25hbWU=').decode(): self.worker_id, __import__('base64').b64decode('d29ya2VyX3R5cGU=').decode(): __import__('base64').b64decode('Y2Rr').decode()}, timeout=10)
            return resp.status_code == 200
        except Exception:
            return False

    def claim_cdk(self, cdk_code: str, game_name: str, account_id: int) -> bool:
        url = f'{self.base_url}/api/cdks/claim'
        try:
            resp = self.session.post(url, json={__import__('base64').b64decode('Y2RrX2NvZGU=').decode(): cdk_code, 'game_name': game_name, 'account_id': account_id}, timeout=15)
            return resp.json().get('code') == 0
        except Exception:
            return False

    def remove_account(self, account_id: int) -> bool:
        __import__('base64').b64decode('UmVtb3ZlIGFuIGludmFsaWQgYWNjb3VudCB2aWEgZnJvbnRlbmQgQVBJLg==').decode()
        url = f'{self.base_url}{__import__("base64").b64decode("L2FwaS9hY2NvdW50cy8=").decode()}{account_id}{__import__("base64").b64decode("L3JlbW92ZQ==").decode()}'
        try:
            resp = self.session.post(url, timeout=15)
            if resp.status_code == 200:
                logger.info(f'Account {account_id} removed (cookie invalid)')
                return True
            logger.warning(f'remove_account {account_id}: HTTP {resp.status_code}')
            return False
        except Exception as e:
            logger.warning(f'remove_account {account_id} failed: {e}')
            return False