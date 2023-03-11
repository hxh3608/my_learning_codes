# 超时设置，分连接（connect）和读取（read）

import requests

r = requests.get('https://httpbin.org/get', timeout=1)
print(r.status_code)

# 分别指定，就可以传入一个元组
# r = requests.get('https://httpbin.org/get', timeout=(5, 30))

#永久等待，可以直接将 timeout 设置为 None，或者不设置直接留空
# r = requests.get('https://httpbin.org/get')

