import pytest
from base import BaseCase
import allure


class TestCreations(BaseCase):
    @staticmethod
    @pytest.mark.UI
    @allure.step("Проверка успешного создания рекламной кампании")
    def test_advertising_campaign_creation(file_path, campaigns_page):
        campaigns_page.create_campaign(file_path)
        allure.step("Проверка наличия успешного сообщения после создания")
        assert campaigns_page.find(campaigns_page.locators.SUCCESS_MESSAGE, timeout=10)

    @staticmethod
    @pytest.mark.UI
    @allure.step("Проверка успешного создания аудиторного сегмента")
    def test_segment_creation(segments_page, type_locator=None):
        allure.step("Взятие id последнего сегмента")
        segment_id = segments_page.find(segments_page.locators.ID_DIV, timeout=15).text
        type_locator = segments_page.locators.SEGMENT_TYPE_APPS if type_locator is None else type_locator
        segments_page.create_segment(type_locator)
        allure.step("Проверка присутствия id созданного сегмента")
        assert segments_page.find(segments_page.locators.find_segment(segment_id)) is not None

    @pytest.mark.UI
    @allure.step("Проверка успешного создания и последующего удаления аудиторного сегмента с типом 'Группы OK и VK'")
    def test_segment_deletion(self, group, segments_page):
        segments_page.go_to_segments_page()
        allure.step("Создание сегмента с проверкой")
        self.test_segment_creation(segments_page, type_locator=segments_page.locators.SEGMENT_TYPE_GROUPS)
        segment_id = segments_page.find(segments_page.locators.ID_DIV, timeout=15).text
        segments_page.delete_segment()
        segments_page.find(segments_page.locators.SUCCESS_MESSAGE)
        allure.step("Проверка отсутствия наличия id созданного сегмента в списке сегментов")
        assert segments_page.find(segments_page.locators.find_segment(segment_id)) is None
