# Browser

# 1.开启无痕模式
# 它的好处就是环境比较干净，不与其他的浏览器示例共享 Cache、Cookies 等内容，
# 其开启方式可以通过 createIncognitoBrowserContext 方法
import asyncio
from pyppeteer import launch

width,height = 1200,768
async def main():
    browser = await launch(headless=False,args=['--disable-infobars',f'--window-size={width},{height}'])
    context = await browser.createIncogniteBrowserContext()
    page = await context.newPage()
    await page.setViewport({'width':width,'height':height})
    await page.goto('https://www.baidu.com')
    await asyncio.sleep(100)
    # 关闭
    await browser.close()
asyncio.get_event_loop().run_until_complete(main())
