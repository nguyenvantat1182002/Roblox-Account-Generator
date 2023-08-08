from capsolve import RobloxCapSolve, CaptchaTimeout, CookieNotFound
from proxy_generator import ChromeProxyGenerator
from tinproxy import TinProxy, ProxyError, CannotFetchProxyDataError
from queue import Queue
from typing import List
from proxy_generator import ChromeProxyGenerator

import os
import json
import threading
import time


num_accounts_created = 0


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


def worker(quantity: int, tin: TinProxy, lock: threading.Lock) -> None:
    global num_accounts_created

    while num_accounts_created < quantity:
        try:
            next_request, proxy = tin.get_current_proxy()
            print('Current proxy:', proxy)

            if next_request < 1:
                proxy = tin.get_proxy()
                print('New proxy:', proxy)

            chrome_proxy = ChromeProxyGenerator(proxy)
            chrome_proxy.create_extension()

            list_extensions = get_list_extensions()
            r = RobloxCapSolve(list_extensions)

            account, security_cookie = r.sign_up()

            with lock:
                with open('Done.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{account.username}|{account.password}/{security_cookie}\n')
                num_accounts_created += 1
                print('Tong so tai khoan da tao:', str(num_accounts_created))
        except CookieNotFound:
            print('Khong tim thay cookie, dang thu lai...')
        except CaptchaTimeout:
            print('Khong giai duoc captcha, dang thu lai...')
        except ProxyError as e:
            print(e)

            end_time = time.time() + 45
            while True:
                if time.time() > end_time:
                    break
                else:
                    print('Se lay lai proxy sau:', end_time - time.time())
        except CannotFetchProxyDataError as e:
            print(e)
            break


# load config
with open('config.json', encoding='utf-8') as file:
    config = json.load(file)
tinproxy_api_keys = config['TinProxyAPIKeys']
user_agent = config['UserAgent'],
max_rows = config['Rows']
max_cols = config['Cols']
quantity = config['Quantity']

# create instances
list_tinproxy_instances = get_tinproxy_instances(tinproxy_api_keys, user_agent)
list_threads: List[threading.Thread] = []
lock = threading.Lock()

for _ in range(max_rows):
    for _ in range(max_cols):
        if list_tinproxy_instances.empty():
            break
        tin = list_tinproxy_instances.get()
        list_tinproxy_instances.task_done()

        t = threading.Thread(target=worker, args=(quantity, tin, lock), daemon=True)
        list_threads.append(t)

for t in list_threads:
    t.start()
    time.sleep(.5)

for t in list_threads:
    t.join()
