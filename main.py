from capsolve import RobloxCapSolve
from proxy_generator import  ChromeProxyGenerator
from tinproxy import TinProxy
from queue import Queue

import os
import json
import threading


def get_list_extensions() -> list:
    folder_name = 'extensions'
    extension_names = os.listdir(folder_name)
    return [f'{os.getcwd()}\\{folder_name}\\{extension_name}' for extension_name in extension_names]


def get_tinproxy_instances(list_api_keys: list, user_agent: str) -> 'Queue[TinProxy]':
    q = Queue()
    for key in list_api_keys:
        tin = TinProxy(key, user_agent)
        q.put(tin)
    return q


# list_extensions = get_list_extensions()
# r = RobloxCapSolve(list_extensions)
#
# account, cookie = r.sign_up()
#
# print(account.username, account.password)
# print(cookie)

# load config
with open('config.json', encoding='utf-8') as file:
    config = json.load(file)
tinproxy_api_keys = config['TinProxyAPIKeys']
user_agent = config['UserAgent'],
max_rows = config['Rows']
max_cols = config['Cols']


# create instances
list_threads = []


for _ in range(max_rows):
    for _ in range(max_cols):
        pass