# 获取节点信息

from selenium import webdriver
browser = webdriver.Chrome()
url = 'https://dynamic2.scrape.cuiqingcai.com/'
browser.get(url)
logo = browser.find_element_by_class_name('logo-image')
print(logo)
# 1.获取属性
print(logo.get_attribute('src'))
# 2.获取文本值
# 每个 WebElement 节点都有 text 属性，
# 直接调用这个属性就可以得到节点内部的文本信息，这相当于 pyquery 的 text 方法
logo_title = browser.find_element_by_class_name('logo-title')
print(logo_title.text) # 不是text()
# 3.获取 ID、位置、标签名、大小
print(logo_title.id)
print(logo_title.location)
print(logo_title.tag_name)
print(logo_title.size)