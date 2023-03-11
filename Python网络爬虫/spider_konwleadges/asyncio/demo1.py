# 定义协程

import asyncio  # 引入了 asyncio 这个包，这样我们才可以使用 async 和 await
async def execute(x): # 使用 async 定义了一个 execute 方法
    print('Number:%s'%x)
Coroutine = execute(1) # 这个方法并没有执行，而是返回了一个 coroutine 协程对象
print('coroutine:',Coroutine)
print('After calling execute...')
loop = asyncio.get_event_loop() # 创建了一个事件循环 loop
#  调用了 loop 对象的 run_until_complete 方法将协程注册到事件循环 loop 中，execute方法这才执行
loop.run_until_complete(Coroutine)
print('After calling loop...')

