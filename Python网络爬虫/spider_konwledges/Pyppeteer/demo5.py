# launch-用户数据持久化

import asyncio
from pyppeteer import launch
async def main():
    # 启动的时候设置 userDataDir,用于恢复一些历史记录甚至一些登录状态信息
    browser = await launch(headless = False,args=['--disable-infobars'],userDataDir = './userdata') # 无头模式
    page = await browser.newPage()
    await page.goto('https://www.taobao.com')
    await asyncio.sleep(100)
asyncio.get_event_loop().run_until_complete(main())