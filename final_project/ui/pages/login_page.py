# import allure
import pytest

from ui.locators import basic_locators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    url = 'login'
    locators = basic_locators.LoginPageLocators()

    def authorize(self, username, password, enter=False):
        self.enter_string(self.locators.USERNAME_FIELD, username)
        self.enter_string(self.locators.PASSWORD_FIELD, password)
        if enter:
            self.hit_enter_key(self.locators.PASSWORD_FIELD)
        else:
            self.click(self.locators.LOGIN_BUTTON)

    def get_text_error_message(self):
        element = self.find(self.locators.LOGIN_ERROR_MESSAGE)
        return element.text

    def get_password_field_type(self):
        return self.find(self.locators.PASSWORD_FIELD).get_attribute('type')

    def go_to_register(self):
        self.click(self.locators.CREATE_ACC_BUTTON)

    # def get_required_attribute(self, locator, attribute):
    #     return self.find(locator).get_attribute(attribute)