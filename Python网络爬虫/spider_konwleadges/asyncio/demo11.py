# 其他请求类型
# aiohttp 还支持其他的请求类型，如 POST、PUT、DELETE

# 1.post
# 对于 POST 表单提交，其对应的请求头的 Content-type 为 application/x-www-form-urlencoded
import aiohttp
import asyncio

async def main():
    data = {
        'name':'hxh',
        'age':21
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://httpbin.org/post',data=data) as response:
            print(await response.text())

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

# 对于 POST JSON 数据提交，其对应的请求头的 Content-type 为 application/json，
# 我们只需要将 post 方法的 data 参数改成 json 即可