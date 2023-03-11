# 并发限制
# 我们可以借助于 asyncio 的 Semaphore 来控制并发量

import asyncio
import aiohttp
CONCURRENCY = 5
URL = 'https://www.baidu.com'
semaphore = asyncio.Semaphore(CONCURRENCY) # 创建一个信号量对象
session = None
async def scrape_api():
    async with semaphore:
        print('scraping',URL)
        async with session.get(URL) as response:
            await asyncio.sleep(1)
            return await response.text()

async def main():
    global session
    session = aiohttp.ClientSession()
    scrape_index_tasks = [asyncio.ensure_future(scrape_api()) for _ in range(10000)]
    await asyncio.gather(*scrape_index_tasks)
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())