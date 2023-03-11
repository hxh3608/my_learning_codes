import re

# 修饰符，如re.I,re.S,re.M,re.X等
content = '''Hello 1234567 World_This
is a Regex Demo
'''
# 原先匹配的是除换行符之外的任意字符
result = re.match('^He.*?(\d+).*?Demo$', content, re.S) #需加一个修饰符 re.S，匹配包含换行符的所有字符
print(result.group())
print(result.group(1))