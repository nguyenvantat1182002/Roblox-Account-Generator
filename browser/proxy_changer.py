import secrets
import os
import shutil


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    }
}
"""

background_js = """
var config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
);
"""


class ProxyChangerExtension:
    def __init__(self, host: str, port: str, username: str, password: str):
        self.host = host.strip()
        self.port = port.strip()
        self.username = username.strip()
        self.password = password.strip()
        self._plugin_folder_path = None

    @property
    def plugin_folder_path(self) -> str:
        return self._plugin_folder_path

    def create_extension(self) -> None:
        extensions_folder = 'extensions'

        if not os.path.exists(extensions_folder):
            os.mkdir(extensions_folder)

        folder_path = f'{extensions_folder}\\proxy_auth_plugin_{secrets.token_hex(8)}'

        os.mkdir(folder_path)

        with open(f'{folder_path}\\manifest.json', 'w', encoding='utf-8') as file:
            file.write(manifest_json)

        with open(f'{folder_path}\\background.js', 'w', encoding='utf-8') as file:
            file.write(background_js % (self.host, self.port, self.username, self.password))

        self._plugin_folder_path = f'{os.getcwd()}\\{folder_path}'

    def remove(self) -> None:
        if not os.path.exists(self.plugin_folder_path):
            return
        shutil.rmtree(self.plugin_folder_path)
