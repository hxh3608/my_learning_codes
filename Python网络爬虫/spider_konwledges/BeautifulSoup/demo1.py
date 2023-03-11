import requests
from bs4 import BeautifulSoup

r = requests.get('http://python123.io/ws/demo.html')
demo = r.text
soup = BeautifulSoup(demo,'html.parser')
#格式化输出html
# print(soup.prettify())

#Tag标签
print(soup.title) #title标签
print(soup.a) #a标签
print(type(soup.a))
print('=='*20)
#Tag名字
print(soup.title.name)
print(soup.title.parent.name)
print(soup.title.parent.parent.name)
print('=='*20)
#Tag的属性(attrs)
print(soup.a.attrs)
print(soup.a.attrs['class'])
print(type(soup.a.attrs))
print('=='*20)
#Tag的NavigableString
print(soup.a.string)
print(soup.p)
print(soup.p.string)
print(type(soup.p.string))
print('=='*20)
#Tag的Comment(标签内的注释部分)

