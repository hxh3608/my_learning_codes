from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urljoin


# 1.准备工作创建浏览器对象
base_url = 'https://dynamic2.scrape.cuiqingcai.com/page/{page}'
total_pages = 10
time_out = 100
option = ChromeOptions()
option.add_argument('--headless') # 无头模式，即不打开浏览器窗口
browser = webdriver.Chrome(options=option)
wait = WebDriverWait(browser,time_out)

# 2.何时页面加载成功，通用的爬取方法，它可以实现任意 URL 的爬取和状态监听以及异常处理
def get_page(url,condition,locator):
    try:
        browser.get(url)
        wait.until(condition(locator)) # 页面加载成功的条件
    except TimeoutException:
        return 'Time Out Error'

# 3.爬取列表页,每页加载成功的条件
def get_index_page(page):
    url = base_url.format(page = page)
    get_page(url,condition=EC.visibility_of_all_elements_located,locator=(By.CSS_SELECTOR,'#index .item'))


# 4.解析每页（列表页），提取出详情页的url
def parser_page():
    infos = browser.find_elements_by_css_selector('#index .item .name')
    for info in infos:
        href = info.get_attribute('href')
        detail_url = urljoin(base_url,href)
        yield detail_url # 使用生成器，那后面要加上 list 来进行迭代


# 5.详情页加载成功的判定条件
def get_detail_page(url):
    # 我们使用的是 visibility_of_element_located，即判断单个元素出现即可，因为只有一部电影
    get_page(url,condition=EC.visibility_of_element_located,
             locator=(By.TAG_NAME,'h2'))

# 6.解析详情页信息，提取所需信息
def parser_detail_page():
    url = browser.current_url
    # 注意 element 与 elements 的区别
    name = browser.find_element_by_tag_name('h2').text.split('-')[0].strip()
    categories = [element.text for element in browser.find_elements_by_css_selector
    ('.categories button span')]
    cover = browser.find_element_by_css_selector('.cover').get_attribute('src')
    score = browser.find_element_by_class_name('score').text
    drama = browser.find_element_by_css_selector('.drama p').text
    return {
        'url' : url,
        'name' : name,
        'categories' : categories,
        'cover' : cover,
        'score' : score,
        'drama' : drama
    }

# 7.存储数据
import json
from os import makedirs
from os.path import exists

results_dir = 'movies_results'
exists(results_dir) or makedirs(results_dir)
def save_data(data):
    name = data.get('name')
    data_path = f'{results_dir}/{name}.json'
    json.dump(data,open(data_path,'w',encoding='utf-8'),ensure_ascii=False,indent=2)


# 8.将上述方法合并，实现信息获取
def main():
    movie_data = []
    for page in range(1,total_pages + 1):
        get_index_page(page) # 把页面加载出来
        detail_urls = parser_page()
        for url1 in list(detail_urls): # 前面用的是生成器，所以要 list
            get_detail_page(url1)
            data = parser_detail_page()
            movie_data.append(data)
            save_data(data)
    print(movie_data)





if __name__ == '__main__':
    main()







