# 文件上传

import requests

file = {'file':open('favicon.ico','rb')}
r = requests.post('http://httpbin.org/post',files=file)
print(r.text)