# 获取信息
# Page 获取源代码用 content 方法即可，Cookies 则可以用 cookies 方法获取

import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq
async def main():
    browser = await launch(headless = True)
    page = await browser.newPage()
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    print('HTML:',await page.content())
    print('Cookies:',await page.cookies())
    # await asyncio.sleep(20)
    await page.close()
    await browser.close()
asyncio.get_event_loop().run_until_complete(main())
