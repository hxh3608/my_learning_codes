# SSL证书认证

import requests

#抛出 SSLError 错误
# response = requests.get('https://static2.scrape.cuiqingcai.com/')
# print(response.status_code)

#会给出警告，建议我们给它指定证书
# response = requests.get('https://static2.scrape.cuiqingcai.com/', verify=False)
# print(response.status_code)

#通过捕获警告到日志的方式忽略警告
import logging
logging.captureWarnings(True)
response = requests.get('https://static2.scrape.cuiqingcai.com/', verify=False)
print(response.status_code)

#当然，我们也可以指定一个本地证书用作客户端证书，
#这可以是单个文件（包含密钥和证书）或一个包含两个文件路径的元组：
#注意：我们需要有 crt 和 key 文件，并且指定它们的路径。
#另外注意，本地私有证书的 key 必须是解密状态，加密状态的 key 是不支持的。

# response = requests.get('https://static2.scrape.cuiqingcai.com/', cert=('/path/server.crt', '/path/server.key'))
# print(response.status_code)