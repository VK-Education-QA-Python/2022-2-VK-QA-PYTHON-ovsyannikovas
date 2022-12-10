import pytest
from base import BaseCase
import allure
from api.api_base import ApiBase
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
        assert '/'.join(self.driver.current_url.split('/')[3:]) == MainPage.url

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
        assert '/'.join(self.driver.current_url.split('/')[3:]) == MainPage.url

    def test_enter_key(self, login_page, create_fake_user):
        username, password = create_fake_user['username'], create_fake_user['password']
        login_page.authorize(username=username, password=password, enter=True)
        assert '/'.join(self.driver.current_url.split('/')[3:]) == MainPage.url

    def test_valid_login_with_space_invalid_pass(self, login_page, create_fake_user):
        username, password = create_fake_user['username'], create_fake_user['password']
        login_page.authorize(username=username + ' ', password=password)
        import time
        time.sleep(1)
        message_text = login_page.get_text_error_message()
        assert message_text == 'Invalid username or password'

    def test_create_account_link(self, login_page):
        login_page.go_to_register()
        assert '/'.join(self.driver.current_url.split('/')[3:]) == RegisterPage.url

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
        assert '/'.join(self.driver.current_url.split('/')[3:]) == MainPage.url

    def test_valid_all_fields_eithout_middlename(self, register_page, mysql_builder):
        data = mysql_builder.get_fake_user()
        register_page.register(name=data['name'], surname=data['surname'], username=data['username'],
                               email=data['email'], password1=data['password'], password2=data['password'])
        mysql_builder.client.delete_user(data['username'])
        assert '/'.join(self.driver.current_url.split('/')[3:]) == MainPage.url

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
        assert '/'.join(self.driver.current_url.split('/')[3:]) == RegisterPage.url

    def test_small_username(self, register_page, mysql_builder):
        minlength = register_page.get_required_attribute(register_page.locators.USERNAME_FIELD, 'minlength')
        data = mysql_builder.get_fake_user()
        register_page.register(name=data['name'], surname=data['surname'],
                               username=data['username'][0] * (int(minlength) - 1),
                               email=data['email'], password1=data['password'], password2=data['password'],
                               middlename=data['middle_name'])
        assert '/'.join(self.driver.current_url.split('/')[3:]) == RegisterPage.url

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
        assert '/'.join(self.driver.current_url.split('/')[3:]) == MainPage.url

    def test_login_link(self, register_page):
        register_page.go_to_login()
        assert '/'.join(self.driver.current_url.split('/')[3:]) == LoginPage.url


class TestApi(ApiBase):
    def test_add_user(self, create_fake_user):
        username, password = create_fake_user
        self.api_client.post_login(username, password)
        response = self.api_client.add_user(name='testname', surname='testsurname', username='testusername',
                                            password='testpass', email='test@mail.ru')
        # assert response.status_code == 200
        # response = self.api_client.delete_user(username='testusername', password=password)
        # assert response.status_code == 200

    def test_add_existent_username_and_password(self, create_fake_user):
        username, password = create_fake_user
        self.api_client.post_login(username, password)
        response = self.api_client.add_user(name='testname', surname='testsurname', username=username,
                                            password=password, email='test@mail.ru')

    def test_add_existent_username(self, create_fake_user):
        username, password = create_fake_user
        self.api_client.post_login(username, password)
        response = self.api_client.add_user(name='testname', surname='testsurname', username=username,
                                            password='password', email='test@mail.ru')

    # def test_add_existent_email(self, create_fake_user):
    #     username, password = create_fake_user
    #     self.api_client.post_login(username, password)
    #     response = self.api_client.add_user(name='testname', surname='testsurname', username=username,
    #                                         password=password, email='test@mail.ru')

    def test_edit_users_password(self, mysql_builder,
                                 create_fake_user):  # пароль остается старый, но в таблице меняется
        username, password = create_fake_user
        response = self.api_client.edit_users_password(username=username, old_password=password, new_password='12345')
        print(mysql_builder.client.select_by_username(username))
        new_password = mysql_builder.client.select_by_username(username).password
        assert response.status_code == 200  # and new_password == '12345'

    def test_delete_user(self, create_fake_user):
        username, password = create_fake_user
        response = self.api_client.delete_user(username, password)
        assert response.status_code == 204

    def test_delete_non_existent_user(self):  # post login здеся
        response = self.api_client.delete_user('username1', 'password')
        assert response.status_code == 204

    def test_block_user(self, create_fake_user):
        username, password = create_fake_user
        response = self.api_client.block_user(username=username, password=password)
        assert response.status_code == 200

    def test_block_non_existent_user(self, mysql_builder):
        data = mysql_builder.get_fake_user()
        response = self.api_client.block_user(username=data['username'], password=data['password'])
        assert response.status_code == 401

    def test_unblock_user(self):
        ...

    def test_unblock_non_existent_user(self):
        ...
        # data = mysql_builder.get_fake_user()
        # response = self.api_client.block_user(username=data['username'], password=data['password'])

    def test_ubblock_unblocked_user(self):
        ...

    def test_login_user(self, create_fake_user):  # в начале регистрация
        ...
        # response = self.api_client.post_login(data[''], '12345')
        # print(response)

    def test_login_non_existent_user(self):
        ...

    def test_status(self):
        response = self.api_client.get_status()
        assert response.status_code == 200

    # и тд аналогично ui


class TestApiLogin:
    ...


class TestApiRegistration:
    ...
