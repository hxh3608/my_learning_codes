# 实际上不用回调方法，直接在 task 运行完毕之后也可以直接调用 result 方法获取结果

import asyncio
import requests

async def request():
    url = 'https://www.baidu.com'
    status = requests.get(url)
    return status

coroutine = request()
task = asyncio.ensure_future(coroutine)
print('Task:',task)
loop = asyncio.get_event_loop()
loop.run_until_complete(task)
print('Task:',task)
print('Task Result:',task.result())