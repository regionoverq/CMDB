# -*-encoding:utf-8-*-
import os

# 远程接收数据的服务器
Params = {
    "server": "192.168.1.28",
    "port": 8888,
    'url': '/assets/report/',
    'request_timeout': 30,
}
# 日志文件配置
PATH = os.path.join(os.path.dirname(os.getcwd()), 'log', 'cmdb.log')

