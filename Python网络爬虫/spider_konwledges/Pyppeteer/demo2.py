# 实例2
import asyncio
from pyppeteer import launch
width,height = 1366,768
async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width':width,'height':height}) # 设置窗口大小
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    await page.waitForSelector('.item .name')
    await asyncio.sleep(2)
    await page.screenshot(path='./example.png') # 截图
    # 执行 JavaScript 并返回对应数据。
    dimensions = await page.evaluate('''() => {
            return {
            width:document.documentElement.clientWidth,
            height:document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')
    print(dimensions)
    await browser.close()
asyncio.get_event_loop().run_until_complete(main())