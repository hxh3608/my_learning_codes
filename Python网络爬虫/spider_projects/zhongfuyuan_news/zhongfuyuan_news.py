# 需要爬取的内容有：
# 标题、时间、来源、正文内容


import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import re
from urllib.parse import urljoin # url 字符串拼接
import pymysql
import multiprocessing
import time

URL = 'http://www.china-nea.cn/site/term/20.html'

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
    time = doc('.List-N-Time span')[0].text
    origin = doc('.List-N-Time span')[1].text
    content = soup.find('div',class_="text-box text-box-con")
    # print(content)
    data = {
        'title':title,
        'time':time,
        'origin':origin,
        'content':content
    }
    return data