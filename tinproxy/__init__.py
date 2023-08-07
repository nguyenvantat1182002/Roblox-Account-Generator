import requests


class TinProxy:
    def __init__(self, api_key: str, user_agent: str):
        self.params = {
            'api_key': api_key
        }

        self.session = requests.Session()
        self.session.headers['User-Agent'] = user_agent

    def get_current_proxy(self) -> tuple:
        pass