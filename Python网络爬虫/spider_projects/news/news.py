import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from urllib.parse import urljoin # url 字符串拼接
BASE_URL = 'http://www2017.tyut.edu.cn/xyxw/lgyw.htm'
# http://www2017.tyut.edu.cn/xyxw/lgyw/369.htm

# 定义一个通用的爬虫方法
def get_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding # 防止乱码
        text = r.text  # str 类型
        return text
    except:
        return 'error'

# 获取新闻详情url
def get_detail_url(url):
    text = get_text(url)
    detail_urls = []
    soup = BeautifulSoup(text, 'html.parser')
    div_lists = soup.find_all('div',class_='tit')
    for div in div_lists:
        detail_url = div.find('a')['href']
        detail_url = urljoin(BASE_URL, detail_url)
        # print(detail_url)
        detail_urls.append(detail_url)
    return detail_urls

# 获取详情页文本
def get_detail_text(url):
    return get_detail_text(url)

# 获取新闻信息
def get_infos(text):
    doc = pq(text)
    title = doc('.contenttop h2').text()
    time = doc('.xxxx span:first-child').text()
    time = time.replace("发布时间：","").strip()
    origin = doc('.xxxx span:nth-child(2)').text()
    origin = origin.replace("来源：","").strip()
    author = doc('.xxxx span:nth-child(3)').text()
    author = author.replace("作者：","").strip()
    click_times = doc('.xxxx span:nth-child(4) span').text() # 因为次数是js渲染的
    content = doc('.v_news_content:first-child').html()
    data = {
        'title':title,
        'time':time,
        'origin':origin,
        'author':author,
        'click_times':click_times,
        'content':content
    }
    print(data)
    return data

# 定义主函数，执行上述函数
def main():
    for i in range(369, 365, -1):
        index_url = f"{BASE_URL}?start={i}&filter="
        detail_urls = get_detail_url(index_url)
        for url in detail_urls:
            # 爬取点击次数
            option = ChromeOptions()
            option.add_argument('--headless')
            browser = webdriver.Chrome(options=option)
            browser.get(url)
            text = browser.page_source
            get_infos(text)

if __name__ == '__main__':
    main()

