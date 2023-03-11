#抓取二进制数据

import requests

r = requests.get('https://github.com/favicon.ico') #github站点图标
print(r.text) # 图片转为字符串，乱码
print(r.content) # 二进制

with open('favicon.ico','wb') as fp:
     fp.write(r.content)