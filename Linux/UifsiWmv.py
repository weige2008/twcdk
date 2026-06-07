import asyncio
import json
import os
import re
import time
from pathlib import Path
from typing import Optional
from loguru import logger
from .MlXQfWNy import HEARTBEAT_INTERVAL, STREAM_URL
from .LJsRVHRE import jnyRVBYj
from .fDoRgRNa import zLcaZPQp
zFDuLWFY = __import__('base64').b64decode('I2NoYW5uZWwtcGxheWVyLWdhdGUgPiBkaXYgPiBkaXYgPiBkaXYuTGF5b3V0LXNjLTF4Y3M2bWMtMC5pTklpRk4gPiBkaXYgPiBidXR0b24=').decode()
aSTfVZmp = __import__('base64').b64decode('aHR0cHM6Ly93d3cudHdpdGNoLnR2L2Ryb3BzL2ludmVudG9yeQ==').decode()
cPCFFSVb = 600000
UhgROXhk = 30000
oUlQeWEy = re.compile('[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}')

class vJgKTYrj:

    def __init__(self, account_data: dict, api_client: jnyRVBYj):
        self.account = account_data
        self.api = api_client
        self.account_id = account_data.get('id', 0)
        self.username = account_data.get('username', 'unknown')
        self.auth_token = account_data.get(__import__('base64').b64decode('YXV0aF90b2tlbg==').decode(), '')
        self.context = None
        self.stream_page = None
        self.drops_page = None
        self._running = False
        self._drops_found = 0

    async def run(self) -> None:
        self._running = True
        tag = f'[{self.username}]'
        if not self.auth_token and (not self.account.get(__import__('base64').b64decode('Y29va2llcw==').decode())):
            logger.error(f'{tag} No auth token or cookies')
            self.api.update_status(self.account_id, 'failed')
            return
        try:
            from cloakbrowser import launch_persistent_context_async
        except ImportError:
            logger.error(__import__('base64').b64decode('Y2xvYWticm93c2VyIG5vdCBpbnN0YWxsZWQ=').decode())
            self.api.update_status(self.account_id, 'failed')
            return
        session_dir = Path(__import__('base64').b64decode('Li9wcm9maWxlcw==').decode()) / f'cdk_profile_{self.account_id}'
        session_dir.mkdir(parents=True, exist_ok=True)
        try:
            launch_kwargs = {'user_data_dir': str(session_dir), 'headless': True, 'args': [f'--fingerprint={20000 + self.account_id}'], 'locale': 'zh-CN'}
            self.context = await launch_persistent_context_async(**launch_kwargs)
            if not self.context.pages:
                self.stream_page = await self.context.new_page()
            else:
                self.stream_page = self.context.pages[0]
            await self._inject_cookies()
            if not await self._validate_cookies():
                logger.error(f'{tag} Cookie invalid, removing account')
                self.api.remove_account(self.account_id)
                self.api.update_status(self.account_id, 'failed')
                return
            if not STREAM_URL:
                logger.error(f'{tag} No STREAM_URL configured')
                self.api.update_status(self.account_id, 'failed')
                return
            logger.info(f'{tag} Opening: {STREAM_URL}')
            await self.stream_page.goto(STREAM_URL, wait_until='domcontentloaded', timeout=30000)
            await self.stream_page.wait_for_timeout(3000)
            await self._click_player_gate()
            await self._click_reward_button()
            self.drops_page = await self.context.new_page()
            await self.drops_page.goto(aSTfVZmp, wait_until='domcontentloaded', timeout=30000)
            await self.drops_page.wait_for_timeout(3000)
            cdk = await self._poll_for_cdk()
            if cdk:
                self._drops_found += 1
                self.api.update_status(self.account_id, 'success', cdk=cdk)
                self.api.claim_cdk(cdk, '', self.account_id)
                logger.info(f'{tag} CDK claimed: {cdk}')
            else:
                logger.warning(f'{tag} No CDK found in 10 min, marking account failed')
                self.api.update_status(self.account_id, 'failed')
        except Exception as e:
            logger.error(f'{tag} Worker error: {e}')
            self.api.update_status(self.account_id, 'failed')
        finally:
            await self._cleanup()

    async def _cleanup(self) -> None:
        self._running = False
        if self.context:
            try:
                await self.context.close()
            except Exception:
                pass
        logger.info(f'[{self.username}] Done. Drops: {self._drops_found}')

    async def _inject_cookies(self) -> None:
        tag = f'[{self.username}]'
        cookies_json = self.account.get(__import__('base64').b64decode('Y29va2llcw==').decode(), '')
        if cookies_json:
            try:
                cookies_list = json.loads(cookies_json)
                twitch_cookies = [c for c in cookies_list if __import__('base64').b64decode('LnR3aXRjaC50dg==').decode() in c.get('domain', '')]
                if twitch_cookies:
                    await self.context.add_cookies(twitch_cookies)
                    logger.info(f'{tag} Injected {len(twitch_cookies)} cookies')
                    return
            except Exception as e:
                logger.warning(f'{tag} Cookie inject error: {e}')
        if self.auth_token:
            await self.context.add_cookies([{'name': __import__('base64').b64decode('YXV0aC10b2tlbg==').decode(), 'value': self.auth_token, 'domain': __import__('base64').b64decode('LnR3aXRjaC50dg==').decode(), 'path': '/'}])

    async def _validate_cookies(self) -> bool:
        __import__('base64').b64decode('VmFsaWRhdGUgY29va2llcyBieSBvcGVuaW5nIFR3aXRjaCBzaWdudXAgcGFnZS4=').decode()
        tag = f'[{self.username}]'
        VqnCxFma = __import__('base64').b64decode('aHR0cHM6Ly93d3cudHdpdGNoLnR2L3NpZ251cA==').decode()
        CLhLdVuK = {__import__('base64').b64decode('aHR0cHM6Ly93d3cudHdpdGNoLnR2Lw==').decode(), __import__('base64').b64decode('aHR0cHM6Ly93d3cudHdpdGNoLnR2Lz9uby1yZWxvYWQ9dHJ1ZQ==').decode()}
        try:
            logger.info(f'{tag} Validating cookies via {VqnCxFma}')
            await self.stream_page.goto(VqnCxFma, wait_until='domcontentloaded', timeout=30000)
            await self.stream_page.wait_for_timeout(5000)
            current_url = self.stream_page.url.rstrip('/')
            if current_url == 'https://www.twitch.tv':
                current_url = 'https://www.twitch.tv/'
            if current_url in CLhLdVuK:
                logger.info(f'{tag} Cookie valid (redirected to {current_url})')
                return True
            else:
                logger.warning(f'{tag} Cookie invalid (stayed at {current_url})')
                return False
        except Exception as e:
            logger.error(f'{tag} Cookie validation error: {e}')
            return False

    async def _click_player_gate(self) -> None:
        __import__('base64').b64decode('Q2xpY2sgJyNjaGFubmVsLXBsYXllci1nYXRlJyBidXR0b24gMyB0aW1lcyBpZiB2aXNpYmxlLCB0byBzdGFydCB3YXRjaGluZy4=').decode()
        try:
            gate = self.stream_page.locator(zFDuLWFY).first
            if await gate.is_visible():
                logger.debug('Clicking player gate...')
                for _ in range(3):
                    await gate.click(timeout=3000)
                    await self.stream_page.wait_for_timeout(200)
        except Exception:
            pass

    async def _click_reward_button(self) -> None:
        """Click bonus/reward button every 1s until it disappears."""
        reward_xpath = '/html/body/div/div[1]/div[1]/div/main/div[1]/div/div[2]/div/div[2]/div/div[4]/div[1]/div/div[4]/section/div/div/div[4]/div/button'
        try:
            for _ in range(30):
                btn = self.stream_page.locator(f'xpath={reward_xpath}').first
                if await btn.is_visible():
                    await btn.click(timeout=3000)
                    logger.debug('Clicked reward button')
                    await self.stream_page.wait_for_timeout(1000)
                else:
                    break
        except Exception:
            pass

    async def _poll_for_cdk(self) -> Optional[str]:
        __import__('base64').b64decode('UG9sbCBkcm9wcy9pbnZlbnRvcnkgZm9yIENESyBidXR0b25zIHVzaW5nIFhQYXRoLiBUaW1lb3V0IDEwIG1pbiwgY2hlY2sgZXZlcnkgMzAgc2VjLg==').decode()
        base_xpath = '/html/body/div/div[1]/div[1]/div/main/div[1]/div/div/div/div/div[2]/div[3]/div'
        modal_input_xpath = '/html/body/div[4]/div/div/div[2]/div/div[2]/div/div[2]/div[3]/div[1]/div/div/input'
        modal_close_xpath = '/html/body/div[4]/div/div/div[2]/div/div[3]/div/button'
        start_time = time.time()
        while self._running and (time.time() - start_time) * 1000 < cPCFFSVb:
            try:
                await self.drops_page.reload(wait_until='domcontentloaded', timeout=30000)
                await self.drops_page.wait_for_timeout(3000)
                for idx in range(1, 30):
                    btn_xpath = f'{base_xpath}/div[{idx}]/div/div[2]/button'
                    btn = self.drops_page.locator(f'xpath={btn_xpath}').first
                    try:
                        if not await btn.is_visible():
                            break
                    except Exception:
                        break
                    logger.debug(f'Clicking CDK button #{idx}')
                    await btn.click(timeout=3000)
                    await self.drops_page.wait_for_timeout(2000)
                    try:
                        inp = self.drops_page.locator(f'xpath={modal_input_xpath}').first
                        if await inp.is_visible():
                            value = (await inp.input_value()).strip()
                            if oUlQeWEy.search(value):
                                logger.info(f'CDK found: {value}')
                                return value
                    except Exception:
                        pass
                    try:
                        close_btn = self.drops_page.locator(f'xpath={modal_close_xpath}').first
                        if await close_btn.is_visible():
                            await close_btn.click(timeout=3000)
                            await self.drops_page.wait_for_timeout(500)
                    except Exception:
                        pass
                logger.debug(f'No CDK yet, waiting {UhgROXhk}ms...')
                await asyncio.sleep(UhgROXhk / 1000)
            except Exception as e:
                logger.debug(f'CDK poll error: {e}')
                await asyncio.sleep(10)
        return None