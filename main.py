from capsolve import RobloxCapSolve, CaptchaTimeout, CookieNotFound
from roblox.exceptions import InvalidInformation
from proxy_generator import ChromeProxyGenerator
from tinproxy import TinProxy, ProxyError, CannotFetchProxyDataError
from queue import Queue
from typing import List
from proxy_generator import ChromeProxyGenerator
from selenium.common.exceptions import TimeoutException, WebDriverException

import os
import json
import threading
import time
import undetected_chromedriver as uc


num_accounts_created = 0


def get_list_extensions() -> list:
    folder_name = 'extensions'
    extension_names = os.listdir(folder_name)
    extension_names = list(filter(lambda name: not name.startswith('chrome_proxy'), extension_names))
    return [f'{os.getcwd()}\\{folder_name}\\{extension_name}' for extension_name in extension_names]


def get_tinproxy_instances(list_api_keys: list, user_agent: str) -> 'Queue[TinProxy]':
    q = Queue()
    for key in list_api_keys:
        tin = TinProxy(key, user_agent)
        q.put(tin)
    return q


def worker(quantity: int, tin: TinProxy, lock: threading.Lock, chrome_pos: tuple) -> None:
    global num_accounts_created

    while num_accounts_created < quantity:
        chrome_proxy = ChromeProxyGenerator()

        try:
            next_request, proxy = tin.get_current_proxy()
            print('Current proxy:', proxy)

            if next_request < 1:
                proxy = tin.get_proxy()
                print('New proxy:', proxy)

            address = proxy[proxy.index('@') + 1:]

            if len(address) < 5:
                end_time = time.time() + next_request
                while True:
                    if time.time() > end_time:
                        break
                    time.sleep(1.5)

                tin.get_proxy()

                continue

            chrome_proxy.proxy_auth = proxy
        except ProxyError as e:
            print(e)
        except CannotFetchProxyDataError as e:
            print(e)
            break

        chrome_proxy.create_extension()

        list_extensions = get_list_extensions()
        list_extensions.append(chrome_proxy.extension_folder_path)

        with lock:
            options = uc.ChromeOptions()
            options.add_argument(f'--load-extension={",".join(list_extensions)}')

            driver = uc.Chrome(user_multi_procs=True, options=options, driver_executable_path='chromedriver.exe')
            r = RobloxCapSolve(driver)

        driver.set_window_size(RobloxCapSolve.BROWSER_WIDTH, RobloxCapSolve.BROWSER_HEIGHT)
        driver.set_window_position(*chrome_pos)

        try:
            driver.get('https://api.ipify.org?format=json')
            time.sleep(2.5)

            items = r.sign_up()
            print(items)

            account, security_cookie = items

            with lock:
                with open('Done.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{account.username}|{account.password}/{security_cookie}\n')
                num_accounts_created += 1
                print('Tong so tai khoan da tao:', str(num_accounts_created))
        except InvalidInformation:
            print('Sai thong tin, dang thu lai....')
        except CookieNotFound:
            print('Khong tim thay cookie, dang thu lai...')
        except CaptchaTimeout:
            print('Khong giai duoc captcha, dang thu lai...')
        except (TimeoutException, WebDriverException):
            print('Loi, dang thu lai...')

        driver.quit()
        chrome_proxy.remove()


# load config
with open('config.json', encoding='utf-8') as file:
    config = json.load(file)
tinproxy_api_keys = config['TinProxyAPIKeys']
user_agent = config['UserAgent']
max_rows = config['Rows']
max_cols = config['Cols']
quantity = config['Quantity']

# create instances
list_tinproxy_instances = get_tinproxy_instances(tinproxy_api_keys, user_agent)
list_threads: List[threading.Thread] = []
lock = threading.Lock()
x, y = 0, 0

for _ in range(max_rows):
    for _ in range(max_cols):
        if list_tinproxy_instances.empty():
            break
        tin = list_tinproxy_instances.get()
        list_tinproxy_instances.task_done()

        t = threading.Thread(target=worker, args=(quantity, tin, lock, (x, y)), daemon=True)
        list_threads.append(t)

        x += RobloxCapSolve.BROWSER_WIDTH
    x = 0
    y += RobloxCapSolve.BROWSER_HEIGHT

for t in list_threads:
    t.start()
    time.sleep(.5)

for t in list_threads:
    t.join()
