# 点击
# Pyppeteer 同样可以模拟点击，调用其 click 方法即可
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

async def main():
    browser = await launch(headless = False)
    page = await browser.newPage()
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    await page.waitForSelector('.item .name')
    await page.click('.item .name',options={
        'button':'right', # 鼠标按钮，分为 left、middle、right。
        'clickCount':1, # 点击次数
        'delay':3000 # 毫秒 ，延迟点击
    })
    await asyncio.sleep(20)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

