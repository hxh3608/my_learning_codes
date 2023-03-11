#标签树的下行遍历

import requests
from bs4 import BeautifulSoup

r = requests.get('http://python123.io/ws/demo.html')
demo = r.text
soup = BeautifulSoup(demo,'html.parser')

#下行遍历
print(soup.head)
print(soup.head.contents) #.contents:子节点的列表，将<tag>所有儿子节点存入列表
print(soup.body)
print(soup.body.contents)
print(len(soup.body.contents))
print(soup.body.contents[1])
print('=='*20)
for child in soup.body.children: # 子节点的迭代类型，与.contents类似，用于循环遍历儿子节点
    print(child)
print('=='*20)
for child in soup.body.descendants: # 子孙节点的迭代类型，包含所有子孙节点，用于循环遍历
    print(child)

