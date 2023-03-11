# 延时等待


from selenium import webdriver
browser = webdriver.Chrome()
# 1.隐式等待
browser.implicitly_wait(10) #隐式等待 10 秒
browser.get('https://dynamic2.scrape.cuiqingcai.com/')
input = browser.find_element_by_class_name('logo-image')
print(input)
# 隐式等待的效果其实并没有那么好，因为我们只规定了一个固定时间，
# 而页面的加载时间会受到网络条件的影响。

# 2.显示等待
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # 用于指定最长等待时间
from selenium.webdriver.support import expected_conditions as EC
browser = webdriver.Chrome()
browser.get('https://taobao.com/')
wait = WebDriverWait(browser,10) # 显示等待 10 秒
input = wait.until(EC.presence_of_element_located((By.ID,'q')))
button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.btn-search')))
print(input,button)
# 在 10 秒内如果 ID 为 q 的节点（即搜索框）成功加载出来，
# 就返回该节点；如果超过 10 秒还没有加载出来，就抛出异常。

# 如果 10 秒内它是可点击的，也就代表它成功加载出来了，
# 就会返回这个按钮节点；如果超过 10 秒还不可点击，也就是没有加载出来，就抛出异常。