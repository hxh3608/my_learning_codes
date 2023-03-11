#post请求

import requests

data = {'name': 'germey', 'age': '25'}
r = requests.post("http://httpbin.org/post", data=data) # 自动提交到form部分
print(r.text)