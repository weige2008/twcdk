import random
from typing import Optional
import requests
from urllib3 import disable_warnings as _dw
from loguru import logger
_dw()
aLOeJYWi = __import__('base64').b64decode('aHR0cHM6Ly9naC5qYXNvbnplbmcuZGV2L2h0dHBzOi8vcmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbS94Ym94LWNuL2F1dG90d2l0Y2hsaXZlYWRkcmVzc3MvbWFpbi91cmwudHh0').decode()

def zLcaZPQp() -> dict:
    from .MlXQfWNy import lpHstKVE
    if lpHstKVE:
        return {'CLIENT_URL': __import__('base64').b64decode('aHR0cDovL3d3dy50d2l0Y2gudHY=').decode()}
    return {'CLIENT_URL': __import__('base64').b64decode('aHR0cHM6Ly93d3cudHdpdGNoLnR2').decode()}

async def oAvxRwZl(page=None) -> list:
    __import__('base64').b64decode('RmV0Y2ggbGl2ZSBzdHJlYW0gVVJMcyBmcm9tIEdpdEh1YiBtaXJyb3Iu').decode()
    try:
        resp = requests.get(aLOeJYWi, timeout=30, verify=False, proxies={'http': None, 'https': None})
        if resp.status_code == 200:
            urls = [u.strip() for u in resp.text.strip().split('\n') if u.strip()]
            logger.info(f'Fetched {len(urls)} live URLs from GitHub mirror')
            return urls
        logger.warning(f'URL fetch failed: HTTP {resp.status_code}')
    except Exception as e:
        logger.warning(f'URL fetch error: {e}')
    return []

def mjDgFMqU(urls: list) -> Optional[str]:
    if not urls:
        return None
    return random.choice(urls)