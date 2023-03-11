import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import time
import pymysql
import datetime

BASE_URL = 'https://www.cnnpn.cn/channel/1.html'
TOTAL_PAGES = 1

# 通用的爬取方法
def get_text(url):
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

# 获取每一页的内容
def get_each_text(page):
    index_url = f'{BASE_URL}?&page={page}'
    return get_text(index_url)

def get_detail_url(text):
    detail_urls = []
    soup = BeautifulSoup(text,'html.parser')
    li_lists = soup.find_all('li')[:15]
    # print(li_lists)
    for item in li_lists:
        detail_url = item.find('a')['href']
        detail_urls.append(detail_url)
    # print(detail_urls)
    return detail_urls

# 获取详情页文本
def get_detail_text(url):
    return get_text(url)

# 获取所需要的信息
def get_infos(text):
    doc = pq(text)
    title = doc('.title').text().strip()
    time_origin = doc('p.info').text().strip()
    news_time = time_origin[:16]
    time_origin = time_origin.split() # 按空格分隔，生成列表如：['2020-10-02', '15:07', '来源：中国铀业有限公司', '中国铀业']
    origin = time_origin[2]
    origin = origin.replace("来源：","").strip()
    content = doc('.content')
    # print(content)
    now_time = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
    data = {
        'title': title,
        'time': news_time,
        'origin': origin,
        'content': content,
        'access_time': now_time
    }
    return data

# 存入数据库
def save_data(data):
    conn = pymysql.connect(
        host='39.107.231.30',
        user = 'root',
        password = 'Ipbd@mysql123',
        db = 'zhongfuyuan',
        charset = 'utf8'
    )
    cursor = conn.cursor()
    data['time'] = datetime.datetime.strptime(data['time'],'%Y-%m-%d %H:%M')
    insert_sql = "INSERT INTO news(title,date_time,origin,content,access_time) values('%s','%s','%s','%s','%s')"
    sql = insert_sql % (data['title'],data['time'],data['origin'],data['content'],data['access_time'])
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def main(page):
    news_infos = []
    index_page_text = get_each_text(page)
    detail_urls = get_detail_url(index_page_text)
    for url in detail_urls:
        text = get_detail_text(url)
        data = get_infos(text)
        save_data(data)
        news_infos.append(data)
    print(news_infos)


if __name__ == '__main__':
    for page in range(1,TOTAL_PAGES+1):
        main(page)