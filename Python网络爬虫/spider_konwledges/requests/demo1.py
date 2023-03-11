import requests
#利用 params 参数就传递参数
#我们把 URL 参数通过字典的形式传给 get 方法的 params 参数
data = {
    'name':'germey',
    'age':25
}
r = requests.get('http://httpbin.org/get',params=data)
#等同于：
# r = requests.request('GET','http://httpbin.org/get',params=data)
print(r.text)
print(type(r.text))