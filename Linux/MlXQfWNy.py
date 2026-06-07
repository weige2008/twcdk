import os
from pathlib import Path
from dotenv import load_dotenv
KvAMfnzW = Path(__file__).resolve().parent
load_dotenv(KvAMfnzW / '.env')
load_dotenv(KvAMfnzW.parent / '.env')
API_URL = os.getenv('API_URL', __import__('base64').b64decode('aHR0cDovLzEyNy4wLjAuMTo1MDAw').decode())
API_TOKEN = os.getenv(__import__('base64').b64decode('QVBJX1RPS0VO').decode(), '')
CDK_THREADS = int(os.getenv(__import__('base64').b64decode('Q0RLX1RIUkVBRFM=').decode(), '1'))
HEARTBEAT_INTERVAL = int(os.getenv('HEARTBEAT_INTERVAL', '30'))
WORKER_ID = os.getenv(__import__('base64').b64decode('V09SS0VSX0lE').decode(), __import__('base64').b64decode('Y2RrX3dvcmtlcl8x').decode())
NO_HEADLESS = os.getenv('NO_HEADLESS', 'false').lower() == 'true'
lpHstKVE = os.getenv(__import__('base64').b64decode('VFdJVENIX0NURg==').decode(), '0') == '1'
STREAM_URL = os.getenv(__import__('base64').b64decode('U1RSRUFNX1VSTA==').decode(), '')