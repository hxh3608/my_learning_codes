from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time
import pymysql
import string

def get_baidu_hot():
    option = ChromeOptions()
    option.add_argument('--headless')
    browser = webdriver.Chrome(options=option)
    url = 'https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1'
    browser.get(url)
    # 找到展开按钮
    more_btn = browser.find_element_by_xpath('//*[@id="ptab-0"]/div/div[1]/section/div')
    more_btn.click() # 点击展开
    time.sleep(1)
    # 找到热搜标签
    infos = browser.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[1]/section/a/div/span[2]')
    context = [info.text for info in infos ]
    print(context)
    content_index = {}
    for item in context:
        k = item.rstrip(string.digits) # 移除热搜数字
        hot_index = int(item[len(k):])
        hot_content = item[:len(k)]
        content_index[hot_content] = int(hot_index)
    print(context)
    print(content_index)
    return content_index

def save_data():
    conn = pymysql.connect(
        host='localhost',
        user = 'root',
        password = 'hxh10030320',
        db = 'pachong_project',
        charset = 'utf8'
    )
    cursor = conn.cursor()
    # 注意这里的字段名不用加引号
    sql = "insert into baidu_hot(获取时间,热搜内容,热搜指数) values(%s,%s,%s)"
    ts = time.strftime('%Y-%m-%d %X')
    content_index = get_baidu_hot()
    for k,v in content_index.items():
        cursor.execute(sql,(ts,k,v))
    conn.commit()
    conn.close()
    cursor.close()

if __name__ == '__main__':
    get_baidu_hot()
    save_data()