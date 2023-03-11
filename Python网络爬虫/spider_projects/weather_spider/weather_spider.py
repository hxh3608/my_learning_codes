import requests
from bs4 import BeautifulSoup
import pymysql
All_data = []



def get_page(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    response = requests.get(url,headers=headers)
    response.encoding = response.apparent_encoding
    text = response.text
    # text = response.content.decode('utf-8') #注意.content返回的是二进制内容，所以要解码
    return text

def parser_page(text):
    soup = BeautifulSoup(text,'html5lib')
    conMidtab = soup.find('div',class_ = 'conMidtab')
    tables = conMidtab.find_all('table')
    #每个省市用一个table
    for table in tables:
        trs = table.find_all('tr')[2:]
        #enumetate是获取下标值
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]
            # stripped_strings原先是生成器，所以要转换成列表
            city = list(city_td.stripped_strings)[0]  #[0]是为了取出值，而不是一个列表
            temp_td = tds[-2]
            temp = list(temp_td.stripped_strings)[0]
            All_data.append({"city":city,'day_high_temp':temp})
            # print({"city":city,'night_min_temp':int(temp)})


def main():
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
    ]
    for url in urls:
        text = get_page(url)
        parser_page(text)

    All_data.sort(key=lambda data: data['day_high_temp'],reverse=True)
    data = All_data[0:10]
    print(data)

#存入数据库
#建立连接和游标
# def get_conn():
#     conn = pymysql.connect(
#         host = 'localhost',
#         user = 'root',
#         password = 'hxh10030320',
#         db = 'pachong_project',
#         charset = 'utf8'
#     )
#     cursor = conn.cursor()
#     return conn,cursor
#
# def close_conn(conn, cursor):
#     if cursor:
#         cursor.close()
#     if conn:
#         conn.close()
#
# def insert_data():
#     conn = None
#     cursor = None
#     conn,cursor = get_conn()
#     sql = "insert into wether_spider(city,temp) values (%s,%s)"
#     for item in All_data:
#         # item格式：{"city":'北京','temp':18}
#         cursor.execute(sql,[item['city'],item['temp']])
#     conn.commit()
#     close_conn()


if __name__ == '__main__':
    main()
    # insert_data()
    # All_data = [
    #     {"city":'北京','night_min_temp':18},
    #     {"city":'上海','night_min_temp':22},
    #     {"city":'广州','night_min_temp':26}
    # ]

    #定义一个匿名函数，规定按哪个值来排序
    # '''def sort_key(data):
    #     min_temp = - data['night_min_temp']
    #     return min_temp
    #
    # All_data.sort(key=sort_key)'''
    #或者使用lambda表达式
    # All_data.sort(key=lambda data: - data['night_min_temp'])

