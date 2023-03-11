# requests.request(method, url, **kwargs)
#**kwargs: 控制访问的参数，均为可选项
#各个参数使用说明

import requests

kv = {'key1': 'value1', 'key2': 'value2'}
#params
r = requests.request('GET', 'http://python123.io/ws', params=kv)
print(r.url)
#data
r = requests.request('POST', 'http://python123.io/ws', data=kv)
#json
r = requests.request('POST', 'http://python123.io/ws', json=kv)
#headers
hd = {'user‐agent': 'Chrome/10'}
r = requests.request('POST', 'http://python123.io/ws', headers=hd)
#cookies
#auth 身份认证
#files 字典类型，传输文件
fs = {'file': open('favicon.ico', 'rb')}
r = requests.request('POST', 'http://python123.io/ws', files=fs)
#timeout 超时设置
#proxies 代理设置
pxs = { 'http': 'http://user:pass@10.10.10.1:1234',
'https': 'https://10.10.10.1:4321' }
r = requests.request('GET', 'http://www.baidu.com', proxies=pxs)

#详见ppt