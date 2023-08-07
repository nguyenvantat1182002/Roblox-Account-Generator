from . import extension
from tinproxy import TinProxy, ProxyError

import os
import shutil
import secrets
import time


class ChromeProxyGenerator:
    def __init__(self, tinproxy: TinProxy):
        self.tinproxy = tinproxy
        self._extension_folder_path = None

    @property
    def extension_folder_path(self) -> str:
        return self._extension_folder_path

    def create_extension(self) -> None:
        try:
            next_request, proxy = self.tinproxy.get_current_proxy()
        except ProxyError:
            end_time = time.time() + next_request
            while True:
                if time.time() < end_time:
                    print('Lay lai proxy sau:', round(end_time - time.time(), 1))
                if time.time() > end_time:
                    break
            self.tinproxy.get_proxy()
            return self.create_extension()

        proxy = proxy if next_request > 1 else self.tinproxy.get_proxy()

        self._extension_folder_path = f'{os.getcwd()}\\extensions\\chrome_proxy_{secrets.token_hex(8)}'

        os.mkdir(self.extension_folder_path)

        with open(f'{self.extension_folder_path}\\manifest.json', 'w', encoding='utf-8') as file:
            file.write(extension.MANIFEST)

        with open(f'{self.extension_folder_path}\\background.js', 'w', encoding='utf-8') as file:
            account, address = proxy.split('@')
            username, password = account.split(':')
            host, port = address.split(':')

            file.write(extension.background % (host, port, username, password))

    def remove(self) -> None:
        if not os.path.exists(self.extension_folder_path):
            return
        shutil.rmtree(self.extension_folder_path)
