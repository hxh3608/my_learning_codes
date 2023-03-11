# search 它在匹配时会扫描整个字符串，然后返回第一个成功匹配的结果。

import re

content =  'Extra stings Hello 1234567 World_This is a Regex Demo Extra stings'
result = re.search(r'Hello.*?(\d+).*?Demo',content) #不能用match,开头不匹配
print(result)
print(result.group(1))