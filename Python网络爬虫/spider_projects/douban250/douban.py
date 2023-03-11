import requests
from bs4 import BeautifulSoup
import json
import csv

#获取页面
def get_page():
    try:
        url = 'https://movie.douban.com/cinema/nowplaying/jian/'
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        response = requests.get(url,headers=headers)
        response.raise_for_status() #如果不是200，则会引发HTTPError异常
        response.encoding = response.apparent_encoding
        text = response.text #注意不是text()
        return text
    except:
        return 'error'

movies = []
#解析页面
def parser_page(text):
    soup = BeautifulSoup(text,'html.parser') # 制一锅汤
    li_list = soup.find_all('li',attrs={'data-category':'nowplaying'}) # 找到所有存在属性 data-category 为 nowplaying 的 li 标签
    for li in li_list: # 遍历每个 li 标签
        movie = {}
        name = li['data-title']
        score = li['data-score']
        duration = li['data-duration']
        region = li['data-region']
        director = li['data-director']
        actors = li['data-actors']
        img = li.find('img') # 注意 已经是在每个 li 标签里找 img
        src = img['src']
        movie['name'] = name
        movie['score'] = score
        movie['duration'] = duration
        movie['region'] = region
        movie['director'] = director
        movie['actors'] = actors
        movie['src'] = src
        movies.append(movie)
    return movies

#json数据存储
def save_data1(data):
    with open('douban.json','w',encoding='utf-8') as fp:
        #json.dump是为了将列表、字符串dump成满足json格式的字符串
        json.dump(data,fp,ensure_ascii=False) # ensure_ascii=False 是为了不使用 unicode 编码

#csv数据存储
def save_data2(data):
    with open('douban.csv','w',encoding='utf-8',newline='') as fp:
        fieldnames = ['name','score','duration','region','director','actors','src'] #字段名
        writer = csv.DictWriter(fp,fieldnames=fieldnames) # 创建一个对象，将字典映射到行
        writer.writeheader() # 先写入 字段名
        for item in data:
            writer.writerow(item) # 因为每个 item 是一个字典，写入每一个电影的信息


if __name__=='__main__':
    text = get_page()
    data = parser_page(text)
    save_data1(data)
    save_data2(data)


