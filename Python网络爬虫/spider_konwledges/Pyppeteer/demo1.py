# 实例1
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq
async def main():
    browser = await launch() # launch 方法会新建一个 Browser 对象,这一步就相当于启动了浏览器
    # 相当于浏览器中新建了一个选项卡，同时新建了一个 Page 对象，
    # 这时候新启动了一个选项卡，但是还未访问任何页面，浏览器依然是空白
    page = await browser.newPage()
    # 相当于在浏览器中输入了这个 URL，浏览器跳转到了对应的页面进行加载。
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    await page.waitForSelector('.item .name') # 传入选择器，那么页面就会等待选择器所对应的节点信息加载出来
    doc = pq(await page.content()) # 获得当前浏览器页面的源代码，这就是 JavaScript 渲染后的结果。
    names = [item.text() for item in doc('.item .name').items()]
    print('Names:',names)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
