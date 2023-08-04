from typing import Optional
from models import RobloxAccount, rand_account
from PyQt5.QtCore import QThread
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .exceptions import InvalidInformation

import undetected_chromedriver as uc
import random as rand


class Roblox:
    TIMEOUT = 30
    BROWSER_WIDTH = 516
    BROWSER_HEIGHT = 653

    def __init__(self, proxy: str = None, headless: bool = False):
        self.proxy = proxy
        self.headless = headless
        self._options = uc.ChromeOptions()
        self._driver: Optional[uc.Chrome] = None

    @property
    def options(self) -> uc.ChromeOptions:
        return self._options

    @property
    def driver(self) -> uc.Chrome:
        if self._driver:
            return self._driver

        self._driver = uc.Chrome(
            user_multi_procs=True,
            headless=self.headless,
            options=self._options
        )

        self._driver.set_window_size(self.BROWSER_WIDTH, self.BROWSER_HEIGHT)

        return self._driver

    def sign_up(self, account: Optional[RobloxAccount] = None):
        if account is None:
            account = rand_account()

        self.driver.get('https://www.roblox.com/')
        QThread.msleep(500)

        signup_container = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="signup-container"]'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(false);", signup_container)

        birthday_selectors = ['select[id="MonthDropdown"]', 'select[id="DayDropdown"]', 'select[id="YearDropdown"]']
        birthday_values = [account.month, account.day, account.year]
        items = list(zip(birthday_selectors, birthday_values))
        for selector, value in items:
            element = WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            Select(element).select_by_value(str(value))
            QThread.msleep(rand.randint(500, 1500))

        username_input = self.driver.find_element(By.CSS_SELECTOR, 'input[id="signup-username"]')
        username_input.send_keys(account.username)
        QThread.msleep(rand.randint(500, 1500))

        password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[id="signup-password"]')
        password_input.send_keys(account.password)
        QThread.msleep(rand.randint(500, 1500))

        gender_selectors = {
            1: 'button[id="FemaleButton"]',
            2: 'button[id="MaleButton"]'
        }
        gender_button = self.driver.find_element(By.CSS_SELECTOR, gender_selectors[account.gender])
        gender_button.click()

        try:
            sign_up_button = WebDriverWait(self.driver, rand.randint(3, 5)).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="signup-button"]'))
            )
            sign_up_button.click()
        except TimeoutException:
            if isinstance(account, RobloxAccount):
                raise InvalidInformation
            return self.sign_up()
