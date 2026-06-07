import asyncio
import os
import sys
from pathlib import Path
from loguru import logger
from .MlXQfWNy import WORKER_ID, API_URL, CDK_THREADS
from .LJsRVHRE import jnyRVBYj
from .UifsiWmv import vJgKTYrj
logger.remove()
IKVBedAQ = os.environ.get('LOGURU_LEVEL', 'INFO')
logger.add(sys.stderr, format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>', level=IKVBedAQ)
logger.add(Path(__file__).parent / __import__('base64').b64decode('Y2RrX3t0aW1lOllZWVktTU0tRER9LmxvZw==').decode(), rotation='10 MB', retention='7 days', level='DEBUG')

async def IDGCxDGA(api_client: jnyRVBYj, worker_index: int) -> None:
    while True:
        account = api_client.get_idle_account()
        if not account:
            logger.debug(f'[W{worker_index}] No idle accounts, waiting 30s...')
            api_client.worker_heartbeat()
            await asyncio.sleep(30)
            continue
        username = account.get('username', '?')
        account_id = account.get('id', 0)
        logger.info(f'[W{worker_index}] Got account: {username} (id={account_id})')
        worker = vJgKTYrj(account, api_client)
        try:
            await worker.run()
        except Exception as e:
            logger.error(f'[W{worker_index}] Worker error for {username}: {e}')
            api_client.update_status(account_id, 'failed')
        api_client.worker_heartbeat()
        await asyncio.sleep(5)

async def oTaoQMOs() -> None:
    api_client = jnyRVBYj()
    logger.info(f'CDK Mining starting: {CDK_THREADS} workers, front={API_URL}')
    api_client.worker_heartbeat()
    semaphore = asyncio.Semaphore(CDK_THREADS)

    async def bounded_run(i: int):
        async with semaphore:
            await IDGCxDGA(api_client, i)
    tasks = [asyncio.create_task(bounded_run(i)) for i in range(CDK_THREADS)]
    await asyncio.gather(*tasks)
if __name__ == '__main__':
    asyncio.run(oTaoQMOs())