import pytest
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement
from ui.locators import basic_locators
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage(object):

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

    def enter_string(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def hit_enter_key(self, locator):
        element = self.find(locator)
        element.send_keys(Keys.ENTER)

    def get_required_attribute(self, locator, attribute):
        return self.find(locator).get_attribute(attribute)

    def get_text_error_message(self, locator):
        attempt = 30
        element = self.find(locator, 5)
        while element.text == '' and attempt > 0:
            element = self.find(locator, 5)
            attempt -= 1

        # while element.text == '' and attempt > 0:
        #     element = self.find(locator)
        #     attempt -= 1
        return element.text

    def switch_to_second_tab(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
            return self.driver.current_url
        except IndexError:
            raise
