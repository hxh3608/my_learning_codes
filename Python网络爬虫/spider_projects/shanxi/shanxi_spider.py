# -*- coding: UTF-8 -*-
"""
Date: 2020-07-19 10:25
Description:
    爬取山西省政府山西要闻
    爬取国务院、政务联播
    爬取山西旅游新闻
    分别存入数据库中
"""

import requests
from bs4 import BeautifulSoup
import pymysql
import time
import re
from urllib import parse

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/77.0.3865.120 Safari/537.36'
}


def get_text(url):
    """
    对网页进行解析
    :param url: 网页url地址
    :return:
    """
    response = requests.get(url, headers=HEADERS, stream=True)
    text = response.content.decode('utf-8')
    soup = BeautifulSoup(text, "html5lib")
    return soup


# ============================== 爬取国务院政务联播 ========================
def get_info_zhenwu(soup):
    """
    获取国务院政务联播
    """
    content = {}

    div = soup.find('div', class_="column3lp_3 fl")
    li_list = div.find_all('li')
    for index1, li in enumerate(li_list):

        a = li.find('a')
        # 获取标题
        content['title'] = a.text

        # 获取url
        content['url'] = a['href']

        # 解析详情页
        soup1 = get_text(content['url'])
        div = soup1.find('div', class_="policyLibraryOverview_header")
        if div:
            trs = div.find_all('tr')
            for index, tr in enumerate(trs):
                if index == 1:
                    td = tr.find_all('td')[1]

                    content['news_title'] = td.text
                if index == 2:
                    td = tr.find_all('td')[3]

                    content['source'] = td.text
                if index == 4:
                    td = tr.find_all('td')[1]
                    # print(td.text.replace('年', '-').replace('月', '-').replace('日', ''))
                    content['news_time'] = td.text.replace('年', '-').replace('月', '-').replace('日', '')
            article = soup1.find('div', class_="pages_content")
            p = article.find_all('p')[1:]
            p_list = []
            for x in p:
                # print(x)
                p_list.append(x)
            content['article_html'] = ("".join('%s' %id for id in p_list))
            content['nowtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # print(content['article_html'])
        else:
            title_div = soup1.find('div', class_="article oneColumn pub_border")
            h1 = title_div.find('h1')
            content['news_title'] = h1.text.replace("\n", "").strip()
            date_div = soup1.find('div', class_="pages-date")
            span = date_div.find('span')
            pattern = re.compile(r'<div.*?class="pages-date">(.*?)<span.*?class="font">', re.S)
            date = re.findall(pattern, str(date_div))[0]
            # print(date)
            content['news_time'] = date.strip()
            # print(span.text.strip().replace("来源： ", ""))
            content['source'] = span.text.strip().replace("来源： ", "")
            article = soup1.find('div', class_="pages_content")
            p = article.find_all('p')[1:]
            p_list = []
            for x in p:
                # print(x)
                p_list.append(x)
            content['article_html'] = ("".join('%s' %id for id in p_list))
            content['nowtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        time.sleep(2)
        print("正在获取第{}条国务院政务联播新闻......".format(index1+1), content['title'], "--", content['nowtime'])
        write_sql_zhenwu(content)


# ============================== 获取国务院新闻 ============================
def get_info_guo(soup):
    """
    获取国务院新闻
    """
    content = {}
    div = soup.find('div', class_="column3lp_1 fl")
    li_list = div.find_all('li')
    for index, li in enumerate(li_list):
        a = li.find('a')

        # 获取标题
        content['title'] = a.text

        # 获取url
        content['url'] = a['href']
        if "http" not in content['url']:
            a = li.find_all('a')[1]
            content['url'] = a['href']
            content['title'] = a.text
        # print(content)

        # 解析详情页
        soup1 = get_text(content['url'])

        title_div = soup1.find('div', class_="article oneColumn pub_border")

        h1 = title_div.find('h1')

        # 获取新闻标题
        content['news_title'] = h1.text.replace("\n", "").strip()
        date_div = soup1.find('div', class_="pages-date")
        span = date_div.find('span')
        pattern = re.compile(r'<div.*?class="pages-date">(.*?)<span.*?class="font">', re.S)
        date = re.findall(pattern, str(date_div))[0]

        # 获取时间
        content['news_time'] = date.strip()

        # 货物来源
        content['source'] = span.text.strip().replace("来源： ", "")
        article = soup1.find('div', class_="pages_content")
        p = article.find_all('p')[1:]
        p_list = []
        for x in p:
            # print(x)
            p_list.append(x)
        # 将HTML连接
        content['article_html'] = ("".join('%s' %id for id in p_list))

        # 获取当前时间
        content['nowtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        time.sleep(2)
        print("正在获取第{}条国务院新闻......".format(index+1), content['title'], "--", content['nowtime'])
        write_sql_guo(content)


# ============================== 获取山西要闻 ==============================
def get_info_shanxi(soup):
    """
    获取山西要闻
    """
    content = {}

    ul = soup.find('ul', class_="common-tab-content-box hide ftsz-16 mgtp-0 common-list-box")
    li_list = ul.find_all('li')[0:6]
    for index, li in enumerate(li_list):

        a = li.find('a')
        # 获取标题
        content['title'] = a.text

        # 获取url
        content['url'] ="http://shanxi.gov.cn/yw/sxyw/" + a['href'].replace("./",'')

        # 解析详情页
        soup1 = get_text(content['url'])
        title_li = soup1.find('li', class_="article-infos-source left")
        span_time = title_li.find_all('span')[0]

        # 获取时间
        content['time'] = span_time.text.replace("时间：", "")

        # 获取来源
        span_source = title_li.find_all('span')[1]
        content['source'] = span_source['alt'].replace("来源：", "")

        # 获取内容

        article_div = soup1.find('div', class_="TRS_Editor")
        article_html = article_div
        img_list = article_div.find_all('img')
        if img_list:
            for img in img_list:
                # 如果有图片
                common_src = img['src']
                src = parse.urljoin(content['url'], img['src'])

                # 替换图片地址
                article_html = str(article_html).replace("{}".format(common_src), "{}".format(src))
            content['article_html'] = article_html
        else:
            content['article_html'] = article_div

        # 获取当前时间
        content['nowtime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        time.sleep(2)
        print("正在获取第{}条山西要闻......".format(index+1), content['title'], "--", content['nowtime'])
        write_sql_shanxi(content)


# ============================== 获取山西旅游新闻 ==============================
def get_info_shanxi_travel(soup):
    """
    获取详细内容
    以字典存储，并获取一条就写入csv
    """
    content = {}
    ul = soup.find('ul', class_="newsul")
    li_list = ul.find_all('li')[0:6]
    for index, li in enumerate(li_list):

        a = li.find('a')

        # 获取链接标题
        content['title'] = a.text
        base_url = "http://wlt.shanxi.gov.cn"

        url = parse.urljoin(base_url, a['href'])

        content['url'] = url

        # 解析详情页
        soup1 = get_text(content['url'])
        div = soup1.find('div', class_="ggj")

        # 获取新闻正文标题
        h1 = div.find('h1')
        content['news_title'] = h1.text

        # 获取发表时间
        p = div.find('p')
        content['news_time'] = p.text.replace("发布日期：", "").strip()

        # 获取下一页标签
        span = div.find('span', class_="ckqx")

        article_html = div
        img_list = div.find_all('img')
        if img_list:
            for img in img_list:
                # 如果有图片
                common_src = img['src']
                src = parse.urljoin(content['url'], img['src'])

                # 替换图片地址
                article_html = str(article_html).replace("{}".format(common_src), "{}".format(src)).replace("{}".format(str(h1)), "").replace("{}".format(str(p)), "").replace("{}".format(str(span)), "")
            content['article_html'] = article_html
        else:
            content['article_html'] = str(div).replace("{}".format(str(h1)), "").replace("{}".format(str(p)), "").replace("{}".format(str(span)), "")

        # 获取当前时间
        content['nowtime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        time.sleep(2)
        print("正在获取第{}条山西旅游新闻......".format(index+1), content['title'], "--", content['nowtime'])
        write_sql_shanxi_travel(content)


# 山西省旅游新闻存放数据库
def write_sql_shanxi_travel(content):
    db = pymysql.connect("39.107.231.30", "root", "Ipbd@mysql123", "shanxi", charset='utf8')
    cursor = db.cursor()

    insertStr = "INSERT INTO travel_news(title, newstime, article_html, nowtime) VALUES ('%s','%s', '%s', '%s')"

    sql = insertStr % (content['title'], content['news_time'], content['article_html'], content['nowtime'])
    cursor.execute(sql)
    db.commit()


# 山西省政府新闻存放数据库
def write_sql_shanxi(content):
    db = pymysql.connect("39.107.231.30", "root", "Ipbd@mysql123", "shanxi", charset='utf8')
    cursor = db.cursor()

    insertStr = "INSERT INTO shanxinews(title, newstime, source, article_html, nowtime) VALUES ('%s','%s', '%s', '%s', '%s')"

    sql = insertStr % (content['title'], content['time'], content['source'], content['article_html'], content['nowtime'])
    cursor.execute(sql)
    db.commit()


# 国务院政务联播存放数据库
def write_sql_zhenwu(content):
    db = pymysql.connect("39.107.231.30", "root", "Ipbd@mysql123", "shanxi", charset='utf8')
    cursor = db.cursor()

    insertStr = "INSERT INTO politics(title, news_title, newstime, source, article_html, nowtime) VALUES ('%s','%s', '%s', '%s', '%s', '%s')"

    sql = insertStr % (content['title'], content['news_title'], content['news_time'], content['source'], content['article_html'], content['nowtime'])
    cursor.execute(sql)
    db.commit()


# 国务院新闻存放数据库
def write_sql_guo(content):
    db = pymysql.connect("39.107.231.30", "root", "Ipbd@mysql123", "shanxi", charset='utf8')
    cursor = db.cursor()

    insertStr = "INSERT INTO guowuyuannews(title, news_title, newstime, source, article_html, nowtime) VALUES ('%s','%s', '%s', '%s', '%s', '%s')"

    sql = insertStr % (content['title'], content['news_title'], content['news_time'], content['source'], content['article_html'], content['nowtime'])
    cursor.execute(sql)
    db.commit()


def main():
    url_guo = "http://www.gov.cn/"    # url地址
    url_shanxi = "http://shanxi.gov.cn/yw/sxyw/"    # url地址
    url_travel = "http://wlt.shanxi.gov.cn/zxw/zh/sourcefiles/html/jqdt/list.shtml"

    soup_guo = get_text(url_guo)
    print("=="*20, "国务院新闻", "=="*20)
    get_info_guo(soup_guo)  # 获取国务院新闻
    time.sleep(10)

    print("=="*20, "政务联播", "=="*20)
    get_info_zhenwu(soup_guo)   # 获取政务联播
    time.sleep(10)

    print("=="*20, "山西要闻", "=="*20)
    soup_shanxi = get_text(url_shanxi)  # 获取山西要闻
    get_info_shanxi(soup_shanxi)
    time.sleep(10)

    print("=="*20, "山西旅游新闻", "=="*20)
    soup_shanxi_travel = get_text(url_travel)  # 获取山西旅游新闻
    get_info_shanxi_travel(soup_shanxi_travel)


if __name__ == '__main__':
    main()

