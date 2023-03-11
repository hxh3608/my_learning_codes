import requests
from bs4 import BeautifulSoup
import bs4
import pymysql
import csv
import xlwt

# 存入数据库
# 建立连接和游标
def get_conn():
    conn = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = 'hxh10030320',
        db = 'pachong_project',
        charset = 'utf8'
    )
    cursor = conn.cursor()
    return conn,cursor

def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()




def get_text(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        text = r.text
        return text
    except:
        return 'error'

def parser_text(text):
    ulist = []
    ulists = []
    soup = BeautifulSoup(text,'html.parser')
    for tr in  soup.find('tbody').children:
        if isinstance(tr,bs4.element.Tag): #判断是否是标签
            tds = tr.find_all('td')
            ulist.append([tds[0].string,tds[1].string,tds[4].string])
            ulists.append({'排名':int(tds[0].string),'大学名称':tds[1].string,'所在省市':tds[2].string,'类型':tds[3].string,'总分':float(tds[4].string)})
    return ulist,ulists

def get_info(ulist,n):
    tplt = '{0:^8}\t{1:{3}^10}\t{2:^10}'
    print(tplt.format('排名','大学名称','总分',chr(12288)))
    for i in range(n):
        u = ulist[i]
        print(tplt.format(u[0],u[1],u[2],chr(12288)))

# def save_data():
#     url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2020.html'
#     text = get_text(url)
#     ulists = parser_text(text)[1]
#     conn, cursor = get_conn()
#     # 插入时要注意插入的数据列数要与表头列数相等，即创建表时不能加id
#     sql = "insert into best_collage values(%s,%s,%s,%s,%s)"
#     for item in ulists:
#         cursor.execute(sql, [item.get('排名'), item.get('大学名称'),
#                              item.get('所在省市'), item.get('类型'), item.get('总分')])
#     conn.commit()
#     close_conn(conn, cursor)

def save_csv(path,title):
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2020.html'
    text = get_text(url)
    ulists = parser_text(text)[1]
    # newline 设置成不隔行
    with open(path,'w',encoding='utf-8',newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(title)
        for item in ulists:
            writer.writerow([item.get('排名'),item.get('大学名称'),item.get('所在省市'),item.get('类型'),item.get('总分')])

def main():
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2020.html'
    path = './Rank.csv'
    title = ['排名','大学名称','所在省市','类型','总分']
    text = get_text(url)
    ulist = parser_text(text)[0]
    get_info(ulist,20)
    ulists = parser_text(text)[1]
    print(ulists)
    #将数据存入数据库
    # save_data()
    save_csv(path,title)


if __name__ == '__main__':
    main()





