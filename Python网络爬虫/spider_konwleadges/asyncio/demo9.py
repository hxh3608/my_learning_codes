# aiohttp 客户端部分的基本使用

# 基本实例

import aiohttp
import asyncio
async def fetch(session,url):
    # 支持异步的上下文管理器
    async with session.get(url) as response:
        return await response.text(),response.status
async def main():
    async with aiohttp.ClientSession() as session:
        html,status = await fetch(session,'https://cuiqingcai.com')
        print(f'html:{html[:100]}...')
        print(f'status:{status}')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())