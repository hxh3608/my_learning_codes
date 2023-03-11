'''
使用 PyQuery + 正则表达式爬取 豆瓣250 电影信息
'''

import requests
from pyquery import PyQuery as pq
import re
import pymysql
import json
import csv

BASE_URL = 'https://movie.douban.com/top250'


# 定义一个通用的爬虫方法
def get_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers)
        text = r.text  # str 类型
        return text
    except:
        return 'error'


# 获取每部电影的详情url
def get_detail_url(url):
    text = get_text(url)
    doc = pq(text)
    detail_url_href = doc('.pic a')
    detail_urls = []
    for item in detail_url_href.items():
        detail_urls.append(item.attr.href)  # 获取这一页的所有电影详情url
    return detail_urls


# 根据详情url获取电影信息
def get_infos(url):
    movie_infos = {}
    text = get_text(url)
    doc = pq(text)
    # 对于有标签的信息采用pyquery，没有标签的信息采用正则表达式
    rank = doc('.top250 span:first-child')
    rank = rank.text().replace("No.", "").strip()
    movie_infos['rank'] = rank
    name = doc('#content h1 span:first-child').text()
    movie_infos['name'] = name
    director = doc('#info span:first-child span a').text()
    movie_infos['director'] = director
    director = doc('#info span:first-child span a').text()
    movie_infos['director'] = director
    # 有些电影没有 编剧和演员 ，则采用异常处理
    try:
        screenwriter = doc('#info > span:nth-child(3) > span.attrs > a').text()
        screenwriter = screenwriter.replace(" ", "/")
        movie_infos['screenwriter'] = screenwriter
        actors = doc('#info > span.actor > span.attrs  > a').text()
        movie_infos['actors'] = actors
    except:
        movie_infos['screenwriter'] = ''
        movie_infos['actors'] = ''
    type = doc("#info span[property='v:genre']").text()
    type = type.replace(" ", "/")
    movie_infos['type'] = type
    country_pattern = re.compile(r"制片国家/地区:</span> (.*?)<br/>")
    country = re.findall(country_pattern, text)[0]
    movie_infos['country'] = country
    language_pattern = re.compile(r"语言:</span> (.*?)<br/>")
    language = re.findall(language_pattern, text)[0]
    movie_infos['language'] = language
    publish_date = doc("#info span[property='v:initialReleaseDate']").text()
    publish_date = publish_date.replace(" ", "/")
    movie_infos['publish_date'] = publish_date
    last_time = doc("#info span[property='v:runtime']").text()
    movie_infos['last_time'] = last_time
    # 有些电影没有别名，所以采用异常处理
    try:
        other_names_pattern = re.compile(r"又名:</span> (.*?)<br/>")
        other_names = re.findall(other_names_pattern, text)[0]
        movie_infos['other_names'] = other_names
    except:
        movie_infos['other_names'] = ''
    score = doc('.rating_self strong ').text()
    movie_infos['score'] = score
    # MOVIES.append(movie_infos)
    # return MOVIES
    return movie_infos


# 存储数据
# 存为json
def save_data1(data):
    with open('douban_250.json', 'w', encoding='utf-8') as fp:
        # json.dump是为了将列表、字符串dump成满足json格式的字符串
        json.dump(data, fp, ensure_ascii=False)  # ensure_ascii=False 是为了不使用 unicode 编码


# 存为csv
def save_data2(data):
    with open('douban_250.csv', 'w', encoding='utf-8', newline='') as fp:
        fieldnames = ['rank', 'name', 'director', 'screenwriter', 'actors', 'type', 'country', 'language',
                      'publish_date', 'last_time', 'other_names', 'score']  # 字段名
        writer = csv.DictWriter(fp, fieldnames=fieldnames)  # 创建一个对象，将字典映射到行
        writer.writeheader()  # 先写入 字段名
        writer.writerow(data)  # 因为每个 item 是一个字典，写入每一个电影的信息


# 存入数据库
def save_data3(data):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='hxh10030320',
        db='pachong_project',
        charset='utf8'
    )
    cursor = conn.cursor()
    insert_sql = 'INSERT INTO douban_250 values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
    sql = insert_sql % (
        data['rank'], data['name'], data['director'], data['screenwriter'], data['actors'], data['type'],
        data['country'], data['language'], data['publish_date'], data['last_time'], data['other_names'],
        data['score'])
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


# 定义主函数，执行上述函数
def main():
    for i in range(0, 226, 25):
        index_url = f"{BASE_URL}?start={i}&filter="
        index_detail_urls = get_detail_url(index_url)
        for url in index_detail_urls:
            movies = get_infos(url)
            print(movies)
            print('scraping %s...', url)
            save_data1(movies)
            save_data2(movies)
            save_data3(movies)


if __name__ == '__main__':
    main()
