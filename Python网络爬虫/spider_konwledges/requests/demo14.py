# requests.put()方法，联系demo4

import requests

payload = {
    'name':'scvsd',
    'age':20
}

r = requests.put('http://httpbin.org/put',data=payload) #也是提交到form中
print(r.text)