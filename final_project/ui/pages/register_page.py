from faker import Faker

from ui.locators import basic_locators
from ui.pages.base_page import BasePage


class RegisterPage(BasePage):
    url = 'reg'
    locators = basic_locators.RegisterPageLocators()
    fake = Faker(locale="ru_RU")

    def register(self, name, surname, username, email, password1, password2, middlename=False, enter=False):
        self.enter_string(self.locators.NAME_FIELD, name)
        self.enter_string(self.locators.SURNAME_FIELD, surname)
        if middlename:
            self.enter_string(self.locators.MIDDLE_NAME_FIELD, middlename)
        self.enter_string(self.locators.USERNAME_FIELD, username)
        self.enter_string(self.locators.EMAIL_FIELD, email)
        self.enter_string(self.locators.PASSWORD1_FIELD, password1)
        self.enter_string(self.locators.PASSWORD2_FIELD, password2)
        self.click(self.locators.ACCEPT_CHECKBOX)
        if enter:
            self.hit_enter_key(self.locators.PASSWORD2_FIELD)
        else:
            self.click(self.locators.REGISTER_BUTTON)

    def get_password_fields_type(self):
        return self.find(self.locators.PASSWORD2_FIELD).get_attribute('type'), self.find(
            self.locators.PASSWORD1_FIELD).get_attribute('type')

    def go_to_login(self):
        self.click(self.locators.LOGIN_BUTTON)

