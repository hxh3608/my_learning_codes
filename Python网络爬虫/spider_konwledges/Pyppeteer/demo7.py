# Page-选择器

# 1.选择器
# Page 对象内置了一些用于选取节点的选择器方法，如 J 方法传入一个选择器 Selector，则能返回对应匹配的第一个节点，
# 等价于 querySelector。如 JJ 方法则是返回符合 Selector 的列表，类似于 querySelectorAll。
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    await page.waitForSelector('.item .name')
    j_result1 = await page.J('.item .name')
    j_result2 = await page.querySelector('.item .name') # J、querySelector 一样，返回了单个匹配到的节点
    jj_result1 = await page.JJ('.item .name')
    jj_result2 = await page.querySelectorAll('.item .name') # JJ、querySelectorAll 则返回了节点列表，是 ElementHandle 的列表
    print('j_result1',j_result1)
    print('j_result2',j_result2)
    print('jj_result1',jj_result1)
    print('jj_result2',jj_result2)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
