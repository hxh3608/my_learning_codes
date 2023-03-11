# 动作链
# 实现一个节点的拖拽操作，将某个节点从一处拖拽到另外一处
from selenium import webdriver
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to_frame('iframeResult') #  先通过id切换到子Frame页面（iframe标签中的属性）
source = browser.find_element_by_css_selector('#draggable') #要移动的位置
target = browser.find_element_by_css_selector('#droppable') #移动到的位置
actions = ActionChains(browser) # 添加至动作链
actions.drag_and_drop(source,target) # 执行
actions.perform() # 演示
