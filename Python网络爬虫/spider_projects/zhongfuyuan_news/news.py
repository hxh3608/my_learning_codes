# 需要爬取的内容有：
# 标题、时间、正文html，另外指明来源


import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import re
from urllib.parse import urljoin # url 字符串拼接
import pymysql
import multiprocessing
import datetime
import time

URL = 'http://www.china-nea.cn'
BASE_URL = 'http://www.china-nea.cn/site/term/20.html'
TOTAL_PAGES = 1

def get_text(url):
    '''
    定义一个通用的爬取方法
    :return:
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        text = r.text  # str 类型
        return text
    except:
        return 'error'

def get_each_page_text(page):
    '''
    获取每一页的内容
    :param page: 页码
    :return:
    '''
    index_url = f'{BASE_URL}?page={page}'
    return get_text(index_url)


def get_detail_url(text):
    '''
    获取每篇文章的详情url
    :param text:
    :return:
    '''
    detail_urls = []
    soup = BeautifulSoup(text, 'html.parser')
    lists = soup.find_all('div', class_='news-list')
    for item in lists:
        detail_url = item.find('a')['href']
        detail_url = urljoin(URL, detail_url)
        # print(detail_url)
        detail_urls.append(detail_url)
    return detail_urls

def get_detail_text(url):
    '''
    获取详情页文本
    :param url: 详情页地址
    :return: 文本内容
    '''
    return get_text(url)

def get_detail_info(text):
    '''
    获取正文html内容
    :return:
    '''
    soup = BeautifulSoup(text,'html.parser')
    title = soup.find('div',class_="List-N-Title").text
    doc = pq(text)
    news_time = doc('.List-N-Time span')[0].text
    news_time = news_time.replace("时间：", "")
    news_time = news_time.replace('年', '-')
    news_time = news_time.replace('月', '-')
    news_time = news_time.replace('日', '')
    origin = doc('.List-N-Time span')[1].text
    origin = origin.replace("来源：","")
    content = soup.find('div',class_="text-box text-box-con")
    now_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    # # print(content)
    #
    data = {
        'title':title,
        'time':news_time,
        'origin':origin,
        'content':content,
        'access_time':now_time
    }
    # return title,news_time,origin,content
    return data

# 存入数据库
def save_data(data):
    conn = pymysql.connect(
        host='localhost',
        user = 'root',
        password = 'hxh10030320',
        db = 'zhongfuyuan',
        charset = 'utf8'
    )
    cursor = conn.cursor()
    data['time'] = datetime.datetime.strptime(data['time'],'%Y-%m-%d')
    insert_sql = "INSERT INTO news(title,date_time,origin,content,access_time) values('%s','%s','%s','%s','%s')"
    sql = insert_sql % (data['title'],data['time'],data['origin'],data['content'],data['access_time'])
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def main(page):
    news_infos = []
    index_page_text = get_each_page_text(page)
    detail_urls = get_detail_url(index_page_text)
    for url in detail_urls:
        text = get_detail_text(url)
        data = get_detail_info(text)
        save_data(data)
        news_infos.append(data)
    print(news_infos)


if __name__ == '__main__':
    for page in range(1,TOTAL_PAGES+1):
        main(page)
