import pytest
from base import BaseCase
import allure


class TestLogin(BaseCase):
    def test_fields_existence(self, login_page):
        username_field = login_page.find(login_page.locators.USERNAME_FIELD)
        password_field = login_page.find(login_page.locators.PASSWORD_FIELD)
        assert username_field and password_field

    def test_valid_login_valid_pass(self, login_page):
        login_page.authorize(username='gucciman', password='123')
        assert '/'.join(self.driver.current_url.split('/')[3:]) == 'welcome/'  # main_page.url

    def test_valid_login_invalid_pass(self, login_page):
        login_page.authorize(username='gucciman', password='1234')
        import time
        time.sleep(1)
        message_text = login_page.get_text_error_message()
        assert message_text == 'Invalid username or password'

    def test_invalid_login(self, login_page):
        login_page.authorize(username='guccima', password='123')
        import time
        time.sleep(1)
        message_text = login_page.get_text_error_message()
        assert message_text == 'Invalid username or password'

    def test_empty_login_empty_pass(self, login_page):
        login_page.authorize(username='', password='')
        import time
        time.sleep(5)
        assert '/'.join(self.driver.current_url.split('/')[3:]) == login_page.url

    def test_secrecy_password(self, login_page):
        field_type = login_page.get_password_field_type()
        assert field_type == 'password'

    def test_valid_email_login_valid_pass(self, login_page):
        login_page.authorize(username='test@mail.ru', password='test')
        assert '/'.join(self.driver.current_url.split('/')[3:]) == 'welcome/'  # main_page.url

    def test_enter_key(self, login_page):
        login_page.authorize(username='gucciman', password='123', enter=True)
        assert '/'.join(self.driver.current_url.split('/')[3:]) == 'welcome/'  # main_page.url

    def test_valid_login_with_space_invalid_pass(self, login_page):
        login_page.authorize(username='gucciman' + ' ', password='123')
        assert '/'.join(self.driver.current_url.split('/')[3:]) == 'welcome/'  # main_page.url

    def test_create_account_link(self, login_page):
        login_page.go_to_register()
        assert '/'.join(self.driver.current_url.split('/')[3:]) == 'reg'  # register_page.url

    def test_login_password_required_attribute(self,  login_page):
        username_required = login_page.get_required_attribute(login_page.locators.USERNAME_FIELD, 'required')
        password_required = login_page.get_required_attribute(login_page.locators.PASSWORD_FIELD, 'required')
        assert username_required and password_required

    def test_login_field_length(self, login_page):
        minlength = login_page.get_required_attribute(login_page.locators.USERNAME_FIELD, 'minlength')
        maxlength = login_page.get_required_attribute(login_page.locators.USERNAME_FIELD, 'maxlength')
        assert minlength == '6' and maxlength == '16'
