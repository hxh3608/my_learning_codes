# URL 参数设置

import asyncio
import aiohttp

async def main():
    params = {'name':'hxh','age':21}
    async with aiohttp.ClientSession() as session:
        async with session.get('https://httpbin.org/get',params=params) as response:
            print(await response.text())
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

