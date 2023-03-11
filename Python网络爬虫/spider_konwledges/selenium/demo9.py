# 前进和后退
#  back 方法后退，使用 forward 方法前进
import time
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('https://www.baidu.com/')
browser.get('https://www.taobao.com/')
browser.get('https://www.python.org/')
browser.back()
time.sleep(1)
browser.forward()
browser.close()
# 连续访问 3 个页面，然后调用 back 方法回到第 2 个页面，
# 接下来再调用 forward 方法又可以前进到第 3 个页面。