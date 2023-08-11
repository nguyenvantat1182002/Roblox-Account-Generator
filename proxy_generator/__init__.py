from . import extension
from tinproxy import TinProxy, ProxyError
from typing import Optional

import os
import shutil
import secrets
import time


class ChromeProxyGenerator:
    def __init__(self, proxy_auth: str = None):
        self._proxy_auth: Optional[str] = proxy_auth
        self._extension_folder_path = None

    @property
    def proxy_auth(self) -> Optional[str]:
        return self._proxy_auth

    @proxy_auth.setter
    def proxy_auth(self, value: str) -> None:
        self._proxy_auth = value

    @property
    def extension_folder_path(self) -> str:
        return self._extension_folder_path

    def create_extension(self) -> None:
        self._extension_folder_path = f'{os.getcwd()}\\extensions\\chrome_proxy_{secrets.token_hex(8)}'

        os.mkdir(self.extension_folder_path)

        with open(f'{self.extension_folder_path}\\manifest.json', 'w', encoding='utf-8') as file:
            file.write(extension.MANIFEST)

        with open(f'{self.extension_folder_path}\\background.js', 'w', encoding='utf-8') as file:
            account, address = self.proxy_auth.split('@')
            username, password = account.split(':')
            host, port = address.split(':')

            file.write(extension.background % (host, port, username, password))

    def remove(self) -> None:
        if not os.path.exists(self.extension_folder_path):
            return
        shutil.rmtree(self.extension_folder_path)
