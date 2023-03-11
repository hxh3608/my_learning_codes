# 文本输入

import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq
async def main():
    browser = await launch(headless = False)
    page = await browser.newPage()
    await page.goto('https://www.taobao.com')
    # 后退
    await page.type('#q','iPad') # id=q
    # 关闭
    await page.click('#J_TSearchForm > div.search-button > button',options={
        'button':'left', # 鼠标按钮，分为 left、middle、right。
        'clickCount':1, # 点击次数
        'delay':3000 # 毫秒 ，延迟点击
    })
    await asyncio.sleep(100)
    await browser.close()
asyncio.get_event_loop().run_until_complete(main())
