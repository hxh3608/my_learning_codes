# 切换至Frame

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchAttributeException

browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')
try:
    logo = browser.find_element_by_class_name('logo')
except NoSuchAttributeException:
    print('No Logo')
browser.switch_to.parent_frame() # 重新切换回父级 Frame，然后再次重新获取节点
logo1 = browser.find_element_by_class_name('logo')
print(logo1)
print(logo1.text)
#所以，当页面中包含子 Frame 时，如果想获取子 Frame 中的节点，
#需要先调用 switch_to.frame 方法切换到对应的 Frame，然后再进行操作。

