# 身份认证

import requests
from requests.auth import HTTPBasicAuth

# r = requests.get('https://static3.scrape.cuiqingcai.com/',auth = HTTPBasicAuth('admin','admin'))
# print(r.status_code)

#如果用户名和密码正确的话，请求时会自动认证成功，
#返回 200 状态码；如果认证失败，则返回 401 状态码。

#直接传一个元组，它会默认使用 HTTPBasicAuth 这个类来认证

r = requests.get('https://static3.scrape.cuiqingcai.com/', auth=('admin', 'admin'))
print(r.status_code)