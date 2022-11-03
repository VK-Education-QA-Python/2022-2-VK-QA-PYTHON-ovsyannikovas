import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.campaigns_page import CampaignsPage
from ui.pages.segments_page import SegmentsPage

CLICK_RETRY = 3


class BaseCase:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.main_page: MainPage = (request.getfixturevalue('main_page'))
        self.campaigns_page: CampaignsPage = (request.getfixturevalue('campaigns_page'))
        self.segments_page: SegmentsPage = (request.getfixturevalue('segments_page'))

        # page = self.__new__(self.__class__)
        # page.authorize()
