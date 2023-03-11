import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from lxml import etree

BASE_URL = 'https://www.tianyancha.com/company/3135480082'
# BASE_URL1 = 'https://www.tianyancha.com/company/2344931370'

# 通用的爬取方法
def get_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        text = r.text  # str 类型
        # print(text)
        return text
    except:
        return 'error'

def get_infos(text):
    doc = pq(text)
    name = doc('.header h1').text().strip() # 公司名称
    print(name)
    html = etree.HTML(text)

    # /****基本信息****/
    # 联系方式
    tel = html.xpath("//*[@id='company_web_top']/div[2]/div[3]/div[3]/div[1]/div[1]/span[2]")[0].text.strip()
    print(tel)
    # 邮箱
    email = html.xpath("//*[@id='company_web_top']/div[2]/div[3]/div[3]/div[1]/div[2]/span[2]")[0].text.strip()
    print(email)
    # 网址
    url = html.xpath("//*[@id='company_web_top']/div[2]/div[3]/div[3]/div[2]/div[1]/span[2]")[0].text.strip()
    print(url)
    # 地址
    address = html.xpath("//*[@id='company_base_info_address']")[0].text.strip()
    print(address)

    #/****法定代表人相关信息****/
    # 法定代表人
    CEO = html.xpath("//*[@id='_container_baseInfo']/table[1]/tbody/tr[1]/td[1]/div/div[1]/div[2]/div[1]/a")[0].text.strip()
    print(CEO)
    # 拥有公司数目
    num_companies = html.xpath(" //*[@id='_container_baseInfo']/table[1]/tbody/tr[1]/td[1]/div/div[1]/div[2]/div[2]/span")[0].text.strip()
    print(num_companies)
    # 公司举例
    company_name_example = html.xpath("//*[@id='_container_baseInfo']/table[1]/tbody/tr[1]/td[1]/div/div[2]/div/div[2]/span[1]")[0].text.strip()
    print(company_name_example)

    # /****工商信息****/
    # 注册资本
    registered_capital = html.xpath("//*[@id='_container_baseInfo']/table[2]/tbody/tr[1]/td[2]/div")[0].text.strip()
    print(registered_capital)
    issued_capital = html.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[4]')[0].text.strip()
    print(issued_capital)
    established_date = html.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[2]/div')[0].text.strip()
    print(established_date)


if __name__ == '__main__':
    text = get_text(BASE_URL)
    get_infos(text)