# 多任务协程

import asyncio
import requests

async def request():
    url = 'https://www.baidu.com'
    status = requests.get(url)
    return status
coroutine = request()
tasks = [asyncio.ensure_future(coroutine) for _ in range(5)]
print('Tasks:',tasks)
loop = asyncio.get_event_loop()
# 列表首先传递给了 asyncio 的 wait() 方法，然后再将其注册到时间循环中
loop.run_until_complete(asyncio.wait(tasks))
for task in tasks:
    print('Task Result:',task.result())

