# 使用aiohttp

import aiohttp
import asyncio
import time

start = time.time()

# 将请求库由 requests 改成了 aiohttp
async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    await response.text()
    await  session.close()
    return response

async def request():
    url = 'https://static4.scrape.cuiqingcai.com/'
    print('Waiting for',url)
    response = await get(url)
    print('Get response from',url,'response',response)

tasks = [asyncio.ensure_future(request()) for _ in  range(10)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()

print('Cost time:',end-start)