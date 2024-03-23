from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import time
import random
import logging
import asyncio

logging.basicConfig(filemode = 'w', format='%(asctime)s - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

class ShopeeCaptchaSolver():
    def __init__(self) -> None:
        #login url
        self.url = "https://shopee.ph/seller/login"


    async def goto_link(self, url):
        attempts = 10
        for i in range(attempts):
            try:
                await self.page.goto(url)
                logging.info('Navigating to login page...')
                # wait for the whole page to load up
                await self.page.wait_for_load_state(timeout=40000)
                logging.info("Successfully loaded")
                time.sleep(2)

            except (TimeoutError, Exception) as e:
                if i < attempts - 1:
                    logging.info(f"{self.color_text['blue']}Connection or Page problem, page will retry please wait: {e}{self.color_text['reset']}")
                    await self.page.reload()
                    await self.countdown(random.randint(1,4), "team navigation")
                    continue
                else:
                    logging.info(f"Used all {attempts} Attempts")
                    raise Exception("Page nav Needs Fixes.....")
            break

    async def wait_time(self, min_num, max_num) -> int: 
        rand_num = random.uniform(min_num,max_num)
        return rand_num
    
    async def countdown(self, secs, retry_message):
        for i in range(secs, 0, -1):
            logging.info(f"{self.color_text['cyan']}Retrying {retry_message} {str(i)} sec(s){self.color_text['reset']}")
            time.sleep(1)          

    async def main(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(slow_mo=50, headless=False)
            logging.info("Browser instance created")
            self.page = await browser.new_page()
            await stealth_async(self.page)
            logging.info("Page stealth")
            await self.goto_link(self.url)
            logging.info(f"Navigated to {self.url}")

            await browser.close()


if __name__ == '__main__':
    solver = ShopeeCaptchaSolver()
    asyncio.run(solver.main())
