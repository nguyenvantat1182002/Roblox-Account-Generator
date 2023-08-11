from typing import Optional
from models import RobloxAccount, rand_account
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .exceptions import CookieNotFound, InvalidInformation

import undetected_chromedriver as uc
import random as rand
import time


class Roblox:
    TIMEOUT = 30
    BROWSER_WIDTH = 516
    BROWSER_HEIGHT = 653

    def __init__(self, driver: uc.Chrome):
        self.driver = driver

    def get_cookie(self, timeout: int = 10) -> str:
        end_time = time.time() + timeout

        while True:
            cookie = self.driver.get_cookie('.ROBLOSECURITY')
            if cookie:
                return cookie['value']

            if time.time() > end_time:
                break

            time.sleep(.5)

        raise CookieNotFound

    def sign_up(self) -> RobloxAccount:
        account = rand_account()

        self.driver.get('https://www.roblox.com/')
        time.sleep(.5)

        signup_container = WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="signup-container"]'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(false);", signup_container)
        time.sleep(1.5)

        birthday_selectors = ['select[id="MonthDropdown"]', 'select[id="DayDropdown"]', 'select[id="YearDropdown"]']
        birthday_values = [account.month, account.day, account.year]
        items = list(zip(birthday_selectors, birthday_values))
        for selector, value in items:
            element = WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            Select(element).select_by_value(str(value))
            time.sleep(rand.uniform(.5, 1.5))

        username_input = self.driver.find_element(By.CSS_SELECTOR, 'input[id="signup-username"]')
        username_input.send_keys(account.username)
        time.sleep(rand.uniform(.5, 1.5))

        password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[id="signup-password"]')
        password_input.send_keys(account.password)
        time.sleep(rand.uniform(.5, 1.5))

        gender_selectors = {
            1: 'button[id="FemaleButton"]',
            2: 'button[id="MaleButton"]'
        }
        gender_button = self.driver.find_element(By.CSS_SELECTOR, gender_selectors[account.gender])
        gender_button.click()
        time.sleep(rand.uniform(.5, 1.5))

        try:
            sign_up_button = WebDriverWait(self.driver, rand.randint(3, 5)).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="signup-button"]'))
            )
            sign_up_button.click()
        except TimeoutException:
            raise InvalidInformation

        return account
