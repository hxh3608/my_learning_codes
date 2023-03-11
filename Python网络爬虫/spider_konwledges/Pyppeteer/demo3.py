# launch

# 1.无头模式
import asyncio
from pyppeteer import launch
# async def main():
#     await launch(headless = False) # 无头模式
#     await asyncio.sleep(100)
# asyncio.get_event_loop().run_until_complete(main())

# 2.调试模式
async def main():
    browser = await launch(devtools = True) #调试模式
    page = await browser.newPage()
    await page.goto('https://www.baidu.com')
    await asyncio.sleep(100)
asyncio.get_event_loop().run_until_complete(main())

# 3.禁用提示条
# browser = await launch(headless=False, args=['--disable-infobars'])