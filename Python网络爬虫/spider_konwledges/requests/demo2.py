import requests

r = requests.get('http://httpbin.org/get')
print(type(r.text)) #json格式的字符串
print(r.json()) #将字符串转为json数据
print(type(r.json())) #dict类型