import allure

from ui.locators import basic_locators
from ui.pages.base_page import BasePage


class MainPage(BasePage):

    locators = basic_locators.MainPageLocators()

    def authorize(self, email_address="minipersik02@gmail.com", password="testpass"):
        self.click(self.locators.LOGIN_BUTTON_MENU, timeout=15)
        self.enter_string(self.locators.EMAIL_FIELD, email_address)
        self.enter_string(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.LOGIN_BUTTON_FORM)

    @allure.step("Переход на страницу кампаний")
    def go_to_campaigns_page(self):
        self.click(self.locators.CAMPAIGNS)

    @allure.step("Переход на страницу аудиторий")
    def go_to_segments_page(self):
        self.click(self.locators.SEGMENTS)



