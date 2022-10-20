from ui.locators import basic_locators
from ui.pages.main_page import MainPage


class SegmentsPage(MainPage):
    locators = basic_locators.SegmentsPageLocators()

    def create_segment(self, type_locator):
        self.click(self.locators.SEGMENTS_LIST, timeout=10)
        self.click(self.locators.CREATE_SEGMENT_BUTTON2)
        self.click(type_locator, timeout=10)
        self.click(self.locators.CHECKBOX)
        self.click(self.locators.ADD_SEGMENT_BUTTON)
        self.click(self.locators.FINAL_CREATE_SEGMENT_BUTTON)

    def add_group(self, url):
        self.click(self.locators.GROUPS_LIST_BUTTON, timeout=10)
        self.enter(self.locators.INPUT_LINK, url)
        self.click(self.locators.SELECT_ALL_BUTTON)
        self.click(self.locators.ADD_SELECTED_BUTTON)

    def delete_segment(self):
        self.click(self.locators.CREATED_SEGMENT_CHECKBOX)
        self.click(self.locators.ACTIONS_BUTTON)
        self.click(self.locators.REMOVE_BUTTON)

    def delete_group(self):
        self.click(self.locators.GROUPS_LIST_BUTTON)
        self.click(self.locators.REMOVE_GROUP_BUTTON, timeout=15)
        self.click(self.locators.CONFIRM_REMOVE_BUTTON)

