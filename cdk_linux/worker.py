# worker.py - Per-account CDK mining orchestrator
# cdk/worker.py

import asyncio
import json
import os
import re
import time
from pathlib import Path
from typing import Optional

from loguru import logger

from .config import HEARTBEAT_INTERVAL, STREAM_URL
from .api_client import APIClient
from .twitch_miner import get_urls

PLAYER_GATE = "#channel-player-gate > div > div > div.Layout-sc-1xcs6mc-0.iNIiFN > div > button"
DROPS_INVENTORY_URL = "https://www.twitch.tv/drops/inventory"
CDK_TIMEOUT_MS = 600000  # 10 minutes
CDK_CHECK_INTERVAL_MS = 30000  # 30 seconds

CDK_PATTERN = re.compile(r"[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}")


class CDKWorker:
    def __init__(self, account_data: dict, api_client: APIClient):
        self.account = account_data
        self.api = api_client
        self.account_id = account_data.get("id", 0)
        self.username = account_data.get("username", "unknown")
        self.auth_token = account_data.get("auth_token", "")

        self.context = None
        self.stream_page = None
        self.drops_page = None
        self._running = False
        self._drops_found = 0

    async def run(self) -> None:
        self._running = True
        tag = f"[{self.username}]"

        if not self.auth_token and not self.account.get("cookies"):
            logger.error(f"{tag} No auth token or cookies")
            self.api.update_status(self.account_id, "failed")
            return

        try:
            from cloakbrowser import launch_persistent_context_async
        except ImportError:
            logger.error("cloakbrowser not installed")
            self.api.update_status(self.account_id, "failed")
            return

        session_dir = Path("./profiles") / f"cdk_profile_{self.account_id}"
        session_dir.mkdir(parents=True, exist_ok=True)

        try:
            launch_kwargs = {
                "user_data_dir": str(session_dir),
                "headless": True,
                "args": [f"--fingerprint={20000 + self.account_id}"],
                "locale": "zh-CN",
            }
            self.context = await launch_persistent_context_async(**launch_kwargs)
            if not self.context.pages:
                self.stream_page = await self.context.new_page()
            else:
                self.stream_page = self.context.pages[0]

            # Inject cookies
            await self._inject_cookies()

            if not STREAM_URL:
                logger.error(f"{tag} No STREAM_URL configured")
                self.api.update_status(self.account_id, "failed")
                return

            # Open fixed stream
            logger.info(f"{tag} Opening: {STREAM_URL}")
            await self.stream_page.goto(STREAM_URL, wait_until="domcontentloaded", timeout=30000)
            await self.stream_page.wait_for_timeout(3000)

            await self._click_player_gate()
            await self._click_reward_button()

            # Open drops inventory in new tab
            self.drops_page = await self.context.new_page()
            await self.drops_page.goto(DROPS_INVENTORY_URL, wait_until="domcontentloaded", timeout=30000)
            await self.drops_page.wait_for_timeout(3000)

            # Poll for CDK
            cdk = await self._poll_for_cdk()
            if cdk:
                self._drops_found += 1
                self.api.update_status(self.account_id, "success", cdk=cdk)
                self.api.claim_cdk(cdk, "", self.account_id)
                logger.info(f"{tag} CDK claimed: {cdk}")
            else:
                logger.warning(f"{tag} No CDK found in 10 min, marking account failed")
                self.api.update_status(self.account_id, "failed")

        except Exception as e:
            logger.error(f"{tag} Worker error: {e}")
            self.api.update_status(self.account_id, "failed")
        finally:
            await self._cleanup()

    async def _cleanup(self) -> None:
        self._running = False
        if self.context:
            try:
                await self.context.close()
            except Exception:
                pass
        logger.info(f"[{self.username}] Done. Drops: {self._drops_found}")

    async def _inject_cookies(self) -> None:
        tag = f"[{self.username}]"
        cookies_json = self.account.get("cookies", "")
        if cookies_json:
            try:
                cookies_list = json.loads(cookies_json)
                twitch_cookies = [
                    c for c in cookies_list
                    if ".twitch.tv" in c.get("domain", "")
                ]
                if twitch_cookies:
                    await self.context.add_cookies(twitch_cookies)
                    logger.info(f"{tag} Injected {len(twitch_cookies)} cookies")
                    return
            except Exception as e:
                logger.warning(f"{tag} Cookie inject error: {e}")
        if self.auth_token:
            await self.context.add_cookies([{
                "name": "auth-token",
                "value": self.auth_token,
                "domain": ".twitch.tv",
                "path": "/",
            }])

    async def _click_player_gate(self) -> None:
        """Click '#channel-player-gate' button 3 times if visible, to start watching."""
        try:
            gate = self.stream_page.locator(PLAYER_GATE).first
            if await gate.is_visible():
                logger.debug("Clicking player gate...")
                for _ in range(3):
                    await gate.click(timeout=3000)
                    await self.stream_page.wait_for_timeout(200)
        except Exception:
            pass

    async def _click_reward_button(self) -> None:
        """Click bonus/reward button every 1s until it disappears."""
        reward_xpath = "/html/body/div/div[1]/div[1]/div/main/div[1]/div/div[2]/div/div[2]/div/div[4]/div[1]/div/div[4]/section/div/div/div[4]/div/button"
        try:
            for _ in range(30):  # max 30 seconds
                btn = self.stream_page.locator(f"xpath={reward_xpath}").first
                if await btn.is_visible():
                    await btn.click(timeout=3000)
                    logger.debug("Clicked reward button")
                    await self.stream_page.wait_for_timeout(1000)
                else:
                    break
        except Exception:
            pass

    async def _poll_for_cdk(self) -> Optional[str]:
        """Poll drops/inventory for CDK buttons using XPath. Timeout 10 min, check every 30 sec."""
        base_xpath = "/html/body/div/div[1]/div[1]/div/main/div[1]/div/div/div/div/div[2]/div[3]/div"
        modal_input_xpath = "/html/body/div[4]/div/div/div[2]/div/div[2]/div/div[2]/div[3]/div[1]/div/div/input"
        modal_close_xpath = "/html/body/div[4]/div/div/div[2]/div/div[3]/div/button"

        start_time = time.time()
        while self._running and (time.time() - start_time) * 1000 < CDK_TIMEOUT_MS:
            try:
                await self.drops_page.reload(wait_until="domcontentloaded", timeout=30000)
                await self.drops_page.wait_for_timeout(3000)

                # Iterate button indices: div/div[1], div/div[2], ...
                for idx in range(1, 30):
                    btn_xpath = f"{base_xpath}/div[{idx}]/div/div[2]/button"
                    btn = self.drops_page.locator(f"xpath={btn_xpath}").first
                    try:
                        if not await btn.is_visible():
                            break
                    except Exception:
                        break

                    logger.debug(f"Clicking CDK button #{idx}")
                    await btn.click(timeout=3000)
                    await self.drops_page.wait_for_timeout(2000)

                    # Check modal input
                    try:
                        inp = self.drops_page.locator(f"xpath={modal_input_xpath}").first
                        if await inp.is_visible():
                            value = (await inp.input_value()).strip()
                            if CDK_PATTERN.search(value):
                                logger.info(f"CDK found: {value}")
                                return value
                    except Exception:
                        pass

                    # Not a valid CDK, close modal
                    try:
                        close_btn = self.drops_page.locator(f"xpath={modal_close_xpath}").first
                        if await close_btn.is_visible():
                            await close_btn.click(timeout=3000)
                            await self.drops_page.wait_for_timeout(500)
                    except Exception:
                        pass

                logger.debug(f"No CDK yet, waiting {CDK_CHECK_INTERVAL_MS}ms...")
                await asyncio.sleep(CDK_CHECK_INTERVAL_MS / 1000)

            except Exception as e:
                logger.debug(f"CDK poll error: {e}")
                await asyncio.sleep(10)

        return None
