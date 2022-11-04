import pytest
from base import BaseCase
import allure


class TestCreations(BaseCase):

    @pytest.mark.UI
    @allure.step("Проверка успешного создания рекламной кампании")
    def test_advertising_campaign_creation(self, file_path):
        self.main_page.go_to_campaigns_page()
        self.campaigns_page.create_campaign(file_path)
        allure.step("Проверка наличия успешного сообщения после создания")
        assert self.campaigns_page.find(self.campaigns_page.locators.SUCCESS_MESSAGE, timeout=10)

    @pytest.mark.UI
    @allure.step("Проверка успешного создания аудиторного сегмента")
    def test_segment_creation(self, type_locator=None):
        self.main_page.go_to_segments_page()
        allure.step("Взятие id последнего сегмента")
        segment_id = self.segments_page.find(self.segments_page.locators.ID_DIV, timeout=15).text
        type_locator = self.segments_page.locators.SEGMENT_TYPE_APPS if type_locator is None else type_locator
        self.segments_page.create_segment(type_locator)
        allure.step("Проверка присутствия id созданного сегмента")
        assert self.segments_page.find(self.segments_page.locators.find_segment(segment_id)) is not None

    @pytest.mark.UI
    @allure.step("Проверка успешного создания и последующего удаления аудиторного сегмента с типом 'Группы OK и VK'")
    def test_segment_deletion(self, group):
        self.main_page.go_to_segments_page()
        allure.step("Создание сегмента с проверкой")
        self.test_segment_creation(type_locator=self.segments_page.locators.SEGMENT_TYPE_GROUPS)
        segment_id = self.segments_page.find(self.segments_page.locators.ID_DIV, timeout=15).text
        self.segments_page.delete_segment()
        self.segments_page.find(self.segments_page.locators.SUCCESS_MESSAGE)
        allure.step("Проверка отсутствия наличия id созданного сегмента в списке сегментов")
        assert self.segments_page.find(self.segments_page.locators.find_segment(segment_id)) is None
