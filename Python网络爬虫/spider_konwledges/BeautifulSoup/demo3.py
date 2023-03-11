# 上行遍历

import requests
from bs4 import BeautifulSoup

r = requests.get('http://python123.io/ws/demo.html')
demo = r.text
soup = BeautifulSoup(demo,'html.parser')

print(soup.title.parent)
print(soup.html.parent) #就是整个html
print(soup.parent) #无
print('=='*20)
for parent in soup.a.parents: #遍历所有先辈节点，包括soup本身，所以要区别判断
    if parent ==  None:
        print(parent)
    else:
        print(parent.name)