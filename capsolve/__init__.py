from roblox import Roblox, CookieNotFound
from models import RobloxAccount
from .exceptions import CaptchaTimeout
from typing import Tuple, Optional
from selenium.webdriver.common.by import By

import time
import undetected_chromedriver as uc


class RobloxCapSolve(Roblox):
    def __init__(self, driver: uc.Chrome):
        super().__init__(driver)

    def sign_up(self) -> Tuple[RobloxAccount, str]:
        account = super().sign_up()

        end_time = time.time() + 30
        while 'home' not in self.driver.current_url:
            captcha_frame = self.driver.find_elements(By.CSS_SELECTOR, 'iframe[id="arkose-iframe"]')
            if not captcha_frame:
                if time.time() > end_time:
                    raise CaptchaTimeout
                time.sleep(.5)
                continue

            end_time = time.time() + 50
            while True:
                if 'home' in self.driver.current_url:
                    break

                if time.time() > end_time:
                    raise CaptchaTimeout

                time.sleep(.5)

        security_cookie = self.get_cookie(20)

        return account, security_cookie
