# 超时设置

import aiohttp
import asyncio

async def main():
    timeout = aiohttp.ClientTimeout(total=10) # 设置5秒钟的超时
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get('https://httpbin.org/get') as response:
            print('status:',response.status)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

# 如果在 10 秒之内成功获取响应的话,返回200
# 如果超时的话，会抛出 TimeoutError 异常