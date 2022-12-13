# import allure

from ui.locators import basic_locators
from ui.pages.base_page import BasePage


class MainPage(BasePage):

    url = 'welcome/'
    locators = basic_locators.MainPageLocators()

    def get_vk_id(self):
        info = self.find(self.locators.USER_VK_ID)
        vk_id = int(info.text.split(':')[-1])
        return vk_id






