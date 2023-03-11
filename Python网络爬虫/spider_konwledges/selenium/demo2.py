from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input_first = browser.find_element_by_id('q')
# find_element_by_id 等价于 ind_element(By.ID, id)
input_second = browser.find_element_by_css_selector('#q')
input_third = browser.find_element_by_xpath('//*[@id="q"]')
print(input_first,input_second,input_third)
browser.close()
# 这 3 个节点的类型是一致的，都是 WebElement

# 查找淘宝左侧导航条的所有条目(注意是elements)
#得到的内容变成了列表类型，列表中的每个节点都是 WebElement 类型
# lis = browser.find_elements_by_css_selector('.service-bd li')
# print(lis)

