# Page - 选项卡操作

# 新建之后的获取和切换
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(headless = False)
    page = await browser.newPage() # 第一个选项卡
    await page.goto('https://www.baidu.com')
    page = await browser.newPage() # 第二个选项卡
    await page.goto('https://www.bing.com')
    pages = await browser.pages() # 调用 pages 方法即可获取所有的页面
    print('Pages',pages)
    page1 = pages[1]
    # 然后选一个页面调用其 bringToFront 方法即可切换到该页面对应的选项卡。
    await page1.bringToFront()
    await asyncio.sleep(100)