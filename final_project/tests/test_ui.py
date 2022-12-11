import pytest
from base import BaseCase
import allure

from tests.utils import switch_to_new_window
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.register_page import RegisterPage


class TestLogin(BaseCase):
    def test_fields_existence(self, login_page):
        username_field = login_page.find(login_page.locators.USERNAME_FIELD)
        password_field = login_page.find(login_page.locators.PASSWORD_FIELD)
        assert username_field and password_field

    def test_valid_login_valid_pass(self, login_page, create_fake_user):
        username, password = create_fake_user['username'], create_fake_user['password']
        login_page.authorize(username, password)
        assert self.get_url_path() == MainPage.url

    def test_valid_login_invalid_pass(self, login_page, create_fake_user):
        username, password = create_fake_user['username'], create_fake_user['password']
        login_page.authorize(username=username, password=password + 'A')
        import time
        time.sleep(1)
        message_text = login_page.get_text_error_message()
        assert message_text == 'Invalid username or password'

    def test_invalid_login(self, login_page, create_fake_user):
        username, password = create_fake_user['username'], create_fake_user['password']
        login_page.authorize(username=username + 'A', password=password)
        import time
        time.sleep(1)
        message_text = login_page.get_text_error_message()
        assert message_text == 'Invalid username or password'

    def test_secrecy_password(self, login_page):
        field_type = login_page.get_password_field_type()
        assert field_type == 'password'

    def test_valid_email_login_valid_pass(self, login_page):
        login_page.authorize(username='test@mail.ru', password='test')
        assert self.get_url_path() == MainPage.url

    def test_enter_key(self, login_page, create_fake_user):
        username, password = create_fake_user['username'], create_fake_user['password']
        login_page.authorize(username=username, password=password, enter=True)
        assert self.get_url_path() == MainPage.url

    def test_valid_login_with_space_invalid_pass(self, login_page, create_fake_user):
        username, password = create_fake_user['username'], create_fake_user['password']
        login_page.authorize(username=username + ' ', password=password)
        import time
        time.sleep(1)
        message_text = login_page.get_text_error_message()
        assert message_text == 'Invalid username or password'

    def test_create_account_link(self, login_page):
        login_page.go_to_register()
        assert self.get_url_path() == RegisterPage.url

    def test_login_password_required_attribute(self, login_page):
        username_required = login_page.get_required_attribute(login_page.locators.USERNAME_FIELD, 'required')
        password_required = login_page.get_required_attribute(login_page.locators.PASSWORD_FIELD, 'required')
        assert username_required and password_required

    def test_login_field_length(self, login_page):
        minlength = login_page.get_required_attribute(login_page.locators.USERNAME_FIELD, 'minlength')
        maxlength = login_page.get_required_attribute(login_page.locators.USERNAME_FIELD, 'maxlength')
        assert minlength == '6' and maxlength == '16'


class TestRegistration(BaseCase):
    def test_fields_existence(self, register_page):
        name_field = register_page.find(register_page.locators.NAME_FIELD)
        surname_field = register_page.find(register_page.locators.SURNAME_FIELD)
        middlename_field = register_page.find(register_page.locators.MIDDLE_NAME_FIELD)
        username_field = register_page.find(register_page.locators.USERNAME_FIELD)
        email_field = register_page.find(register_page.locators.EMAIL_FIELD)
        password1_field = register_page.find(register_page.locators.PASSWORD1_FIELD)
        password2_field = register_page.find(register_page.locators.PASSWORD2_FIELD)
        term_checkbox = register_page.find(register_page.locators.ACCEPT_CHECKBOX)
        assert name_field and surname_field and middlename_field and username_field and email_field and \
               password1_field and password2_field and term_checkbox

    def test_valid_all_fields(self, register_page, mysql_builder):
        data = mysql_builder.get_fake_user()
        register_page.register(name=data['name'], surname=data['surname'], username=data['username'],
                               email=data['email'], password1=data['password'], password2=data['password'],
                               middlename=data['middle_name'])
        mysql_builder.client.delete_user(data['username'])
        assert self.get_url_path() == MainPage.url

    def test_valid_all_fields_eithout_middlename(self, register_page, mysql_builder):
        data = mysql_builder.get_fake_user()
        register_page.register(name=data['name'], surname=data['surname'], username=data['username'],
                               email=data['email'], password1=data['password'], password2=data['password'])
        mysql_builder.client.delete_user(data['username'])
        assert self.get_url_path() == MainPage.url

    def test_register_existent_username(self, register_page, create_fake_user, mysql_builder):
        username, password = create_fake_user['username'], create_fake_user['password']
        data = mysql_builder.get_fake_user()
        register_page.register(name=data['name'], surname=data['surname'], username=username,
                               email=data['email'], password1=data['password'], password2=data['password'],
                               middlename=data['middle_name'])
        import time
        time.sleep(1)
        message_text = register_page.get_text_error_message()
        assert message_text == 'User already exist'

    def test_register_existent_email(self, register_page, create_fake_user, mysql_builder):
        email = create_fake_user['email']
        data = mysql_builder.get_fake_user()
        register_page.register(name=data['name'], surname=data['surname'], username=data['username'],
                               email=email, password1=data['password'], password2=data['password'],
                               middlename=data['middle_name'])
        import time
        time.sleep(1)
        message_text = register_page.get_text_error_message()
        assert message_text == 'User already exist'

    def test_different_passwords(self, register_page, mysql_builder):
        data = mysql_builder.get_fake_user()
        register_page.register(name=data['name'], surname=data['surname'], username=data['username'],
                               email=data['email'], password1=data['password'], password2=data['password'] + 'A',
                               middlename=data['middle_name'])
        import time
        time.sleep(1)
        message_text = register_page.get_text_error_message()
        assert message_text == 'Passwords must match'

    def test_big_username(self, register_page, mysql_builder):
        maxlength = register_page.get_required_attribute(register_page.locators.USERNAME_FIELD, 'maxlength')
        data = mysql_builder.get_fake_user()
        register_page.register(name=data['name'], surname=data['surname'],
                               username=data['username'][0] * (int(maxlength) + 1),
                               email=data['email'], password1=data['password'], password2=data['password'],
                               middlename=data['middle_name'])
        assert self.get_url_path() == RegisterPage.url

    def test_small_username(self, register_page, mysql_builder):
        minlength = register_page.get_required_attribute(register_page.locators.USERNAME_FIELD, 'minlength')
        data = mysql_builder.get_fake_user()
        register_page.register(name=data['name'], surname=data['surname'],
                               username=data['username'][0] * (int(minlength) - 1),
                               email=data['email'], password1=data['password'], password2=data['password'],
                               middlename=data['middle_name'])
        assert self.get_url_path() == RegisterPage.url

    def test_email_without_dog(self, register_page, mysql_builder):
        data = mysql_builder.get_fake_user()
        register_page.register(name=data['name'], surname=data['surname'], username=data['username'],
                               email=data['username'], password1=data['password'], password2=data['password'],
                               middlename=data['middle_name'])
        import time
        time.sleep(1)
        message_text = register_page.get_text_error_message()
        assert message_text == 'Invalid email address'

    def test_secrecy_password(self, register_page):
        field1_type, field2_type = register_page.get_password_fields_type()
        assert field1_type == field2_type == 'password'

    def test_valid_all_fields_enter_key(self, register_page, mysql_builder):
        data = mysql_builder.get_fake_user()
        register_page.register(name=data['name'], surname=data['surname'], username=data['username'],
                               email=data['email'], password1=data['password'], password2=data['password'],
                               middlename=data['middle_name'], enter=True)
        mysql_builder.client.delete_user(data['username'])
        assert self.get_url_path() == MainPage.url

    def test_login_link(self, register_page):
        register_page.go_to_login()
        assert self.get_url_path() == LoginPage.url


class TestMainPage(BaseCase):
    def test_logout_button(self, main_page):
        main_page.click(main_page.locators.LOGOUT_BUTTON)
        assert self.get_url_path() == LoginPage.url

    def test_quote(self, main_page):
        assert main_page.find(main_page.locators.QUOTE)

    def test_api_button(self, main_page):
        main_page.click(main_page.locators.API_IMG)
        current_url = switch_to_new_window(main_page.driver)
        assert current_url == 'https://en.wikipedia.org/wiki/API'

    def test_future_button(self, main_page):
        main_page.click(main_page.locators.FUTURE_IMG)
        current_url = switch_to_new_window(main_page.driver)
        assert current_url == 'https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/'

    def test_smtp_button(self, main_page):
        main_page.click(main_page.locators.SMTP_IMG)
        current_url = switch_to_new_window(main_page.driver)
        assert current_url == 'https://ru.wikipedia.org/wiki/SMTP'

    def test_logo_clickability(self, main_page):
        main_page.click(main_page.locators.LOGO_BUTTON)
        assert self.get_url_path() == MainPage.url

    def test_home_button(self, main_page):
        main_page.click(main_page.locators.HOME_BUTTON)
        assert self.get_url_path() == MainPage.url

    def test_python_history_link(self, main_page):
        main_page.click(main_page.locators.PYTHON_BUTTON)
        main_page.click(main_page.locators.PYTHON_HISTORY_BUTTON)
        current_url = switch_to_new_window(main_page.driver)
        assert current_url == 'https://en.wikipedia.org/wiki/History_of_Python'

    def test_about_flask_link(self, main_page):
        main_page.click(main_page.locators.PYTHON_BUTTON)
        main_page.click(main_page.locators.ABOUT_FLASK_BUTTON)
        current_url = switch_to_new_window(main_page.driver)
        assert current_url == 'https://en.wikipedia.org/wiki/History_of_Python'

    def test_download_centos7(self, main_page):
        main_page.click(main_page.locators.LINUX_BUTTON)
        main_page.click(main_page.locators.DOWNLOAD_CENTOS7_BUTTON)
        current_url = switch_to_new_window(main_page.driver)
        assert current_url == 'https://www.centos.org/download/'

    def test_wireshark_news(self, main_page):
        main_page.click(main_page.locators.NETWORK_BUTTON)
        main_page.click(main_page.locators.WIRESHARK_NEWS_BUTTON)
        current_url = switch_to_new_window(main_page.driver)
        assert current_url == 'https://www.wireshark.org/news/'

    def test_wireshark_download(self, main_page):
        main_page.click(main_page.locators.NETWORK_BUTTON)
        main_page.click(main_page.locators.WIRESHARK_DOWNLOAD_BUTTON)
        current_url = switch_to_new_window(main_page.driver)
        assert current_url == 'https://www.wireshark.org/#download'

    def test_tcp_dump_examples(self, main_page):
        main_page.click(main_page.locators.NETWORK_BUTTON)
        main_page.click(main_page.locators.TCP_DUMP_EXAMPLES)
        current_url = switch_to_new_window(main_page.driver)
        assert current_url == 'https://hackertarget.com/tcpdump-examples/'
