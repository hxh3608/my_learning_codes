from lxml import etree # 实现xpath
import requests
from urllib.parse import urljoin
from os import makedirs
from os.path import exists
import json


BASE_URL = 'https://www.ygdy8.net/'
INDEX_URL = 'https://www.ygdy8.net/html/gndy/dyzz/list_23_{x}.html'
TOTAL_PAGES = 5
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/84.0.4147.89 Safari/537.36'}


def get_page(url):
    '''
    通用的获取文本信息的url
    :param url: 需爬取的url
    :return: 获取的文本
    '''
    try:
        r = requests.get(url,headers = HEADERS)
        r.raise_for_status()
        r.encoding = 'gbk'
        return r.text
    except Exception as e:
        print(e)

def get_detail_url(text):
    '''
    获取每个列表页每部电影详情的 url
    :param text: 每页的文本信息
    :return:
    '''
    html = etree.HTML(text)
    detail_urls = []
    hrefs = html.xpath("//table[@class='tbspan']//a/@href")
    for href in hrefs:
        detail_url = urljoin(BASE_URL,href)
        detail_urls.append(detail_url)
    return detail_urls

def get_pages_detail_urls():
    '''
    获取10页的所有详细信息 url
    :return:
    '''
    detail_all_urls = []
    for page in range(1,TOTAL_PAGES + 1):
        index_url = INDEX_URL.format(x = page)
        index_text = get_page(index_url)
        detail_urls= get_detail_url(index_text)
        detail_all_urls.extend(detail_urls)
    return detail_all_urls

def parser_detail(url):
    '''
    解析每个详情url，获取所需信息
    :return:
    '''
    movie  = {}
    text = get_page(url)
    html = etree.HTML(text)
    title = html.xpath('//*[@id="header"]/div/div[3]/div[3]/div[1]/div[2]/div[1]/h1/font/text()')[0]
    movie['title'] = title
    ZoomE = html.xpath('//div[@id="Zoom"]')[0] # Zoom 包含了电影的所有详细信息
    all_infos = ZoomE.xpath(".//text()")
    for index,info in enumerate(all_infos):
        if info.startswith("◎译　　名"):
            translated_name = info.replace("◎译　　名",'').strip()
            movie['translated_name'] = translated_name
        elif info.startswith("◎片　　名"):
            row_name = info.replace("◎片　　名",'').strip()
            movie['rowd_name'] = row_name
        elif info.startswith("◎年　　代"):
            year = info.replace("◎年　　代",'').strip()
            movie['year'] = year
        elif info.startswith("◎产　　地"):
            country = info.replace("◎产　　地",'').strip()
            movie['country'] = country
        elif info.startswith("◎类　　别"):
            type = info.replace("◎类　　别",'').strip()
            movie['type'] = type
        elif info.startswith("◎上映日期"):
            show_date = info.replace("◎上映日期",'').strip()
            movie['show_date'] = show_date
        elif info.startswith("◎豆瓣评分"):
            score = info.replace("◎豆瓣评分",'').strip()
            movie['score'] = score
        elif info.startswith("◎片　　长"):
            time = info.replace("◎片　　长",'').strip()
            movie['time'] = time
        elif info.startswith("◎导　　演"):
            director = info.replace("◎导　　演",'').strip()
            movie['director'] = director
        elif info.startswith("◎主　　演"):
            info = info.replace("◎主　　演",'').strip()
            actors = [info]
            for x in range(index+1,len(all_infos)):
                actor = all_infos[x].strip()
                if actor.startswith("◎"):
                    break
                actors.append(actor)
            # print(actors)
            movie['actors'] = actors
        elif info.startswith("◎标　　签"):
            tags = info.replace("◎标　　签",'').strip()
            movie['tags'] = tags
        elif info.startswith("◎简　　介"):
            info = info.replace("◎简　　介",'').strip()
            for x in range(index+1,len(all_infos)):
                drama = all_infos[x].strip()
                if drama.startswith('【下载地址】') or drama.startswith('◎') :
                    break
                movie['drama'] = drama
    return movie


def save_data(data):
    results_dir = 'movies_results'
    exists(results_dir) or makedirs(results_dir)
    name = data.get('title')
    data_path = f'{results_dir}/{name}.json'
    if data_path:
        json.dump(data,open(data_path,'w',encoding='utf-8'),ensure_ascii=False,indent=2)


def main():
    movie_infos = []
    detail_urls = get_pages_detail_urls()
    for url in detail_urls:
        movie = parser_detail(url)
        movie_infos.append(movie)
    print(movie_infos)
    for info in movie_infos:
        save_data(info)



if __name__ == '__main__':
    main()


