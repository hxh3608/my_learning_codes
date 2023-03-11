# 内置的状态码查询对象 requests.codes

import requests

r = requests.get('https://static1.scrape.cuiqingcai.com/')

exit() if not r.status_code == requests.codes.ok else print('Request Successfully')