# 平行遍历

import requests
from bs4 import BeautifulSoup

r = requests.get('http://python123.io/ws/demo.html')
demo = r.text
soup = BeautifulSoup(demo,'html.parser')

print(soup)
print(soup.a.next_sibling) #返回按照HTML文本顺序的下一个平行节点,
print(soup.a.next_sibling.next_sibling)
print('=='*20)
print(soup.a.previous_sibling) #上一个
print('=='*20)
for sibling in soup.a.next_siblings: #遍历后续节点
    print(sibling)
print('==='*20)
for sibling in soup.a.previous_siblings:
    print(sibling)