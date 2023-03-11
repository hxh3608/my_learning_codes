# 代理设置

import requests

proxies = {'https': 'http://user:password@10.10.10.10:1080/',}
requests.get('https://httpbin.org/get', proxies=proxies)

#除了基本的 HTTP 代理外，requests 还支持 SOCKS 协议的代理