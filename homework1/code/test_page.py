import pytest
from ui.locators import *
from base import BaseCase


class TestLog(BaseCase):
    @pytest.mark.UI
    def test_login(self):
        self.login()
        assert self.find(USER_NAME_BUTTON)

    @pytest.mark.UI
    def test_logout(self):
        self.login()
        self.find(INSTRUCTION)
        self.click(EMAIL_BUTTON)
        self.click(LOGOUT_BUTTON)
        assert self.find(LOGIN_BUTTON_MENU)


class TestNegativeAutorization(BaseCase):
    @pytest.mark.UI
    def test_wrong_login(self):
        self.login(email_address="test")
        assert self.find(EMAIL_ERROR_MESSAGE)

    @pytest.mark.UI
    def test_wrong_password(self):
        self.login(password="pass")
        assert self.find(LOGIN_ERROR_MESSAGE)


class TestContactInfo(BaseCase):
    @pytest.mark.UI
    def test_contact_info(self):
        self.login()
        self.driver.get("https://target-sandbox.my.com/profile/contacts")
        self.enter(FIO, "Иванов Иван Иванович")
        self.enter(INN, "123456789876")
        self.enter(PHONE, "+79888888888")
        self.click(SUBMIT_BUTTON)
        assert self.find(SUCCESS_MESSAGE)


class TestMenu(BaseCase):
    @pytest.mark.parametrize(
        'locator, locator_expected',
        [(SEGMENTS, SEGMENTS_EXPECTED),
         (STATISTICS, STATISTICS_EXPECTED)]
    )
    @pytest.mark.UI
    def test_menu(self, locator, locator_expected):
        self.login()
        self.click(locator)
        assert self.find(locator_expected)
