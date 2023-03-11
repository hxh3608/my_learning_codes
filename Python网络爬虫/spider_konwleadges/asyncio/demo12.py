# 响应字段
# 对于响应来说，我们可以用如下的方法分别获取
# 响应的状态码、响应头、响应体、响应体二进制内容、响应体 JSON 结果
import aiohttp
import asyncio

async def main():
    data = {
        'name':'hxh',
        'age':21
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://httpbin.org/post',data=data) as response:
            print('status:',response.status)
            print('headers:',response.headers)
            print('body:',await response.text()) #  coroutine 对象（如 async 修饰的方法），那么前面就要加 await
            print('bytes:',await response.read())
            print('json:',await response.json())

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
