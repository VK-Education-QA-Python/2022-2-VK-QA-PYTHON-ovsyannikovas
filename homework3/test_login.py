import time

import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.common.by import By

from ui.fixtures import get_driver
from ui.pages.base_page import BasePage


class BaseCase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.login_page = LoginPage(driver)
        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                print(cookie)
                self.driver.add_cookie(cookie)

            self.driver.refresh()
            self.main_page = MainPage(driver)


@pytest.fixture(scope='session')
def credentials():
    user = 'minipersik02@gmail.com'
    password = 'testpass'

    return user, password


@pytest.fixture(scope='session')
def cookies(credentials, config, api_client):
    api_client.post_login()
    cookies = []
    for cookie in api_client.session.cookies:
        cookies.append({
            'name': cookie.name,
            'domain': cookie.domain,
            'path': cookie.path,
            'value': cookie.value
        })
    return cookies


class LoginPage(BasePage):
    url = 'https://target-sandbox.my.com/'

    def login(self, user, password):
        self.click((By.XPATH, '/html/body/header/div/nav/button'))
        self.find((By.NAME, 'login')).send_keys(user)
        self.find((By.NAME, 'password')).send_keys(password)

        self.click((By.XPATH, '//html/body/div[4]/div/div[1]/form/button'))

        time.sleep(5)
        return MainPage(self.driver)


class MainPage(BasePage):
    url = 'https://target-sandbox.my.com/'


# class TestLogin(BaseCase):
#     authorize = False
#
#     @pytest.mark.skip("SKIP")
#     def test_login(self, credentials):
#         login_page = LoginPage(self.driver)
#         login_page.login(*credentials)
#
#         time.sleep(5)


class TestLK(BaseCase):

    def test_lk1(self):
        time.sleep(5)


# class TestLkApi:
#     @pytest.fixture(scope='class', autouse=True)
#     def setup(self, api_client):
#         api_client.post_login()
#
#     def test_api_login(self, api_client):
#         assert api_client.session.get('https://target-sandbox.my.com/dashboard/').url == \
#                'https://target-sandbox.my.com/dashboard/'