#如果用 Selenium 来驱动浏览器加载网页的话，就可以直接拿到 JavaScript 渲染的结果了，
#不用担心使用的是什么加密系统。

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome() # 声明谷歌浏览器对象
try:
    browser.get('http://www.baidu.com') # 访问页面
    input = browser.find_element_by_id('kw')
    input.send_keys('python')
    input.send_keys(Keys.ENTER) # 模拟回车键搜索
    wait = WebDriverWait(browser,5) #模拟浏览器等待
    # 验证页面是否出现
    wait.until(EC.presence_of_all_elements_located((By.ID,'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)
except Exception as e:
    print(e)
finally:
    browser.close()