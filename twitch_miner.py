# twitch_miner.py - CDK mining helper
# cdk/twitch_miner.py

import random
from typing import Optional

import requests
from urllib3 import disable_warnings as _dw
from loguru import logger

_dw()

URL_LIST = "https://gh.jasonzeng.dev/https://raw.githubusercontent.com/xbox-cn/autotwitchliveaddresss/main/url.txt"


def get_urls() -> dict:
    from .config import CTF_MODE
    if CTF_MODE:
        return {"CLIENT_URL": "http://www.twitch.tv"}
    return {"CLIENT_URL": "https://www.twitch.tv"}


async def fetch_stream_urls_from_browser(page=None) -> list:
    """Fetch live stream URLs from GitHub mirror."""
    try:
        resp = requests.get(URL_LIST, timeout=30, verify=False, proxies={"http": None, "https": None})
        if resp.status_code == 200:
            urls = [u.strip() for u in resp.text.strip().split("\n") if u.strip()]
            logger.info(f"Fetched {len(urls)} live URLs from GitHub mirror")
            return urls
        logger.warning(f"URL fetch failed: HTTP {resp.status_code}")
    except Exception as e:
        logger.warning(f"URL fetch error: {e}")
    return []


def pick_random_url(urls: list) -> Optional[str]:
    if not urls:
        return None
    return random.choice(urls)
