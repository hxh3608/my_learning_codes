# 重点是 javascript 字符串写法和 await 的使用

from pyppeteer import launch
import json
from os import makedirs
from os.path import exists
import asyncio

BASE_URL = 'https://dynamic2.scrape.cuiqingcai.com/'
INDEX_URL = 'https://dynamic2.scrape.cuiqingcai.com/page/{page}'
TIMEOUT = 100 # 超时
TOTAL_PAGES = 10 # 需爬取的总页数
RESULTS_DIR = 'movie_results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

# 1.定义一个初始化 Pyppeteer 的方法，包括启动 Pyppeteer，新建一个页面选项卡
async def init():
    global browser
    global page
    browser = await launch(headless=True,args=['--disable-infobars'])
    page = await browser.newPage()

# 2.定义一个通用的爬取方法(列表 页面加载)
async def get_page(url,selector):
    try:
        await page.goto(url)
        await page.waitForSelector(selector,options={
            'timeout':TIMEOUT * 1000
        })
    except Exception as e:
        print(e)

# 3.定义一个爬取列表页的方法
async def get_index(page):
    url = INDEX_URL.format(page=page)
    await get_page(url,'.item .name')

# 4.定义一个爬取列表页详情url的方法
async def get_detail_url():
    # 第一个参数是选择器，表示要选择哪个节点，第二个使用一段 JavaScript 字符串提取href，最终返回一个列表
    return await page.querySelectorAllEval('.item .name','nodes => nodes.map(node => node.href)')

# 5.定义一个爬取详情页的方法(加载详情页)
async def get_detail(url):
    await get_page(url,'h2')

# 6.爬取所有详细信息
async def get_detail_infos():
    url = page.url # 获取当前页面的url
    name = await page.querySelectorEval('h2','node => node.innerText')
    categories = await page.querySelectorAllEval('.categories button span','nodes => nodes.map(node => node.innerText)')
    cover = await page.querySelectorEval('.cover','node => node.src')
    score = await page.querySelectorEval('.score','node => node.innerText')
    drama = await page.querySelectorEval('.drama p','node => node.innerText')
    return {
        'url': url,
        'name': name,
        'categories': categories,
        'cover': cover,
        'score': score,
        'drama': drama
    }

# 7.存储信息
async def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# 8.将上述方法串起来
async def main():
   await init()
   try:
       for page in range(1,TOTAL_PAGES + 1):
           await get_index(page)
           detail_urls = await get_detail_url()
           for detail_url in detail_urls:
               await get_detail(detail_url)
               detail_data = await get_detail_infos()
               print(detail_data)
               await save_data(detail_data)
   except  Exception as e:
       print(e)
   finally:
       await browser.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
