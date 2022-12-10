import pytest

from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage


class BaseCase:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config):
        self.driver = driver
        self.config = config
        # self.login_page = LoginPage(self.driver)
        # self.register_page = RegisterPage(self.driver)
        # self.main_page = MainPage(self.driver)

    def get_url_path(self):
        return '/'.join(self.driver.current_url.split('/')[3:])
