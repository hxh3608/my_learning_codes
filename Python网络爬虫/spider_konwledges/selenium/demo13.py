# 反屏蔽

from selenium import webdriver
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])
option.add_experimental_option('useAutomationExtension',False)
browser = webdriver.Chrome(options=option)
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',{
    'source':'Object defineProperty(navigator, "webdriver", {get: () => undefined})'
})
browser.get('https://antispider1.scrape.cuiqingcai.com/')
# 对于大多数的情况，以上的方法均可以实现 Selenium 反屏蔽。
# 但对于一些特殊的网站，如果其有更多的 WebDriver 特征检测，可能需要具体排查。