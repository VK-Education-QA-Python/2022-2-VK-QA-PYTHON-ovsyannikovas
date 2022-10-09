import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui.locators import LOGIN_BUTTON_MENU, EMAIL_FIELD, PASSWORD_FIELD, LOGIN_BUTTON_FORM
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException

CLICK_RETRY = 3


class BaseCase:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    def find(self, locator):
        element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(locator)
        )
        return element

    def click(self, locator):
        for i in range(CLICK_RETRY):
            try:
                elem = self.find(locator)
                elem.click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                if i == CLICK_RETRY - 1:
                    raise

    def login(self, email_address="minipersik02@gmail.com", password="testpass"):
        self.click(LOGIN_BUTTON_MENU)
        email = self.find(EMAIL_FIELD)
        email.send_keys(email_address)
        password_field = self.find(PASSWORD_FIELD)
        password_field.send_keys(password)
        self.click(LOGIN_BUTTON_FORM)

    def enter(self, locator, message):
        field = self.find(locator)
        field.clear()
        field.send_keys(message)
