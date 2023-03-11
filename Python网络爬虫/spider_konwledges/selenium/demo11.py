# 选项卡管理

import time
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
browser.execute_script('window open()') # 开启一个选项卡,然后切换到该选项卡
print(browser.window_handles) # 调用 window_handles 属性获取当前开启的所有选项卡
browser.switch_to_window(browser.window_handles[1]) # 第2个选项卡
browser.get('https://www.taobao.com')
time.sleep(1)
browser.switch_to_window(browser.window_handles[0])
browser.get('https://python.org')
