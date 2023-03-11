# match ，match 方法在使用时需要考虑到开头的内容

import re

content = 'Hello 123 4567 World_This is a Regex Demo'
print(len(content))
result = re.match(r'^Hello\s\d\d\d\s\d{4}\s\w{10}',content)
print(result)
print(result.group())
print(result.group(0)) #整个字符串
print(result.span()) #匹配的开始与结束位置
print('=='*20)
#group(1)
content1 = 'Hello 1234567 World_This is a Regex Demo'
result1 = re.match(r'^Hello\s(\d+)\sWorld',content1) #注意这里将1234567视为一个整体，所以能用group
print(result1.group())
print(result1.group(1)) # 会输出第一个被 () 包围的匹配结果

print('=='*20)
#通用匹配
content2 = 'Hello 123 4567 World_This is a Regex Demo'
result2 = re.match(r'^He.*Demo$',content2)
print(result2.group())
print(result2.span())
print('=='*20)
#贪婪与非贪婪
content3 = 'Hello 1234567 World_This is a Regex Demo'
result3 = re.match(r'^He.*(\d+).*Demo$',content3) #贪婪
print(result3.group())
print(result3.group(1)) #只输出了7
result4 = re.match(r'^He.*?(\d+).*Demo$',content3) #非贪婪
print(result4.group(1))
#但需要注意的是，如果匹配的结果在字符串结尾，
# .*? 就有可能匹配不到任何内容了，因为它会匹配尽可能少的字符。
#如：
# content = 'http://weibo.com/comment/kEraCN'
# result1 = re.match('http.*?comment/(.*?)', content) #结果:无
# result2 = re.match('http.*?comment/(.*)', content) #结果:kEraCN
