# 无头模式

from selenium import webdriver
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
option.add_argument('--headless') # 无头模式
browser = webdriver.Chrome(options=option)
browser.set_window_size(1366,768) # 在无头模式下，我们最好需要设置下窗口的大小
browser.get('https://www.baidu.com')
browser.get_screenshot_as_file('preview.png') # 输出了页面的截图