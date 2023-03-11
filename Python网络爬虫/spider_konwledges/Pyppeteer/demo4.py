# launch-页面设置大小，防止检测

import asyncio
from pyppeteer import launch
width,height = 1366,768

async def main():
    browser = await launch(headless = False,args=['--disable-infobars'])
    page = await browser.newPage()
    await page.setViewport({'width':width,'height':height})
    # 防止检测
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
    await page.goto('https://antispider1.scrape.cuiqingcai.com/')
    await asyncio.sleep(100)
asyncio.get_event_loop().run_until_complete(main())
