# 在demo1中，当我们将 coroutine 对象传递给 run_until_complete 方法的时候，
# 实际上它进行了一个操作就是将 coroutine 封装成了 task 对象，我们也可以显式地进行声明，

import asyncio
async def execute(x):
    print("Number:",x)
    return x
Coroutine = execute(1)
print('Coroutine:',Coroutine)
print('After calling execute...')
loop = asyncio.get_event_loop() # 创建事件循环
task = loop.create_task(Coroutine) # 将Coroutine封装成task对象
print('Task:',task) #  pending 状态
loop.run_until_complete(task) # 将 task 对象添加到事件循环中得到执行
print('Task:',task)  # finished状态,result变为1
print('After calling loop...')

