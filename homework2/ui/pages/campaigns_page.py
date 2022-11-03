import allure
import pytest

from ui.locators import basic_locators
from ui.pages.main_page import MainPage


class CampaignsPage(MainPage):

    locators = basic_locators.CampaignsPageLocators()

    @allure.step("Создание кампании")
    def create_campaign(self, file_path):
        url = "https://vk.com/vkedu"
        # button1 or button2 ?
        self.click(self.locators.CREATE_CAMPAIGN_BUTTON2, timeout=10)
        self.click(self.locators.AIM_BUTTON, timeout=10)
        self.enter_string(self.locators.INPUT_URL, url)
        self.find(self.locators.PRICE_SLIDER, timeout=5)
        self.click(self.locators.BUDGET_SETTING)
        self.click(self.locators.FORMAT_ITEM, timeout=5)
        for i in range(3):
            self.click(self.locators.slide(i))
            self.enter_string(self.locators.UPLOAD_IMG600_BUTTON, file_path)
            self.click(self.locators.SAVE_IMG_BUTTON)
            self.enter_string(self.locators.slide_link(i), url)
            self.enter_string(self.locators.slide_title(i), f"Заголовок {i + 1}")
        self.enter_string(self.locators.UPLOAD_IMG256_BUTTON, file_path)
        self.click(self.locators.SAVE_IMG_BUTTON)
        self.enter_string(self.locators.TITLE_FIELD, "Заголовок")
        self.enter_string(self.locators.TEXT_FIELD, "Текст объявления")
        self.click(self.locators.FINAL_CREATE_CAMPAIGN_BUTTON)
