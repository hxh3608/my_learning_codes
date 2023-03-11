# 绑定回调

import asyncio
import requests

async def request():
    url = 'https://www.baidu.com'
    status = requests.get(url)
    return status

def callback(task):
    print('Status:',task.result())

coroutine = request()
task = asyncio.ensure_future(coroutine)
task.add_done_callback(callback) # 将 callback 方法传递给了封装好的 task 对象
# 当 task 执行完毕之后就可以调用 callback 方法了，
# 同时 task 对象还会作为参数传递给 callback 方法，调用 task 对象的 result 方法就可以获取返回结果了
print('Task:',task)
loop = asyncio.get_event_loop()
loop.run_until_complete(task)
print('Task:',task)