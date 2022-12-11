# import allure

from ui.locators import basic_locators
from ui.pages.base_page import BasePage


class MainPage(BasePage):

    url = 'welcome/'
    locators = basic_locators.MainPageLocators()






