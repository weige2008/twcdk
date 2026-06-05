# config.py - CDK mining config (GitHub Actions)
# cdk_linux/config.py

import os
from pathlib import Path

from dotenv import load_dotenv

_self_dir = Path(__file__).resolve().parent
load_dotenv(_self_dir / ".env")
load_dotenv(_self_dir.parent / ".env")

API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")
API_TOKEN = os.getenv("API_TOKEN", "")
CDK_THREADS = int(os.getenv("CDK_THREADS", "1"))
HEARTBEAT_INTERVAL = int(os.getenv("HEARTBEAT_INTERVAL", "30"))
WORKER_ID = os.getenv("WORKER_ID", "cdk_worker_1")
NO_HEADLESS = os.getenv("NO_HEADLESS", "false").lower() == "true"
CTF_MODE = os.getenv("TWITCH_CTF", "0") == "1"
STREAM_URL = os.getenv("STREAM_URL", "")
