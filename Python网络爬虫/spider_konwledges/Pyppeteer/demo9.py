# 常见操作
# 作为一个页面，我们一定要有对应的方法来控制，如加载、前进、后退、关闭、保存等

import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

async def main():
    browser = await launch(headless = False)
    page = await browser.newPage()
    await page.goto('https://dynamic1.scrape.cuiqingcai.com/')
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    # 后退
    await page.goBack()
    # 前进
    await page.goForward()
    # 刷新
    await page.reload()
    # 保存PDF
    await page.pdf()
    # 截图
    await page.screenshot()
    # 设置页面 HTML
    await page.setContent('<h2>Hello World</h2>')
    # 设置 User-Agent
    await page.setUserAgent('Python')
    # 设置 Headers
    await page.setExtraHTTPHeaders(headers={})
    # 关闭
    await page.close()
    await browser.close()
asyncio.get_event_loop().run_until_complete(main())
