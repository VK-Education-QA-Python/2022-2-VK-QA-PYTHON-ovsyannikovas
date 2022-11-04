import pytest
from selenium.common import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from ui.locators import basic_locators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage(object):
    locators = basic_locators.BasePageLocators()

    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        try:
            return self.wait(timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            return

    def click(self, locator, timeout=None):
        element = self.find(locator, timeout)
        element.click()

    def enter_string(self, locator, text, photo=False):
        element = self.find(locator)
        if not photo:
            element.clear()
        element.send_keys(text)

