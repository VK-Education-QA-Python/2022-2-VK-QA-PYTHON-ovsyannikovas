import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.campaigns_page import CampaignsPage
from ui.pages.segments_page import SegmentsPage


@pytest.fixture()
def driver(config):
    version = "105.0.5195.19"
    url = config["url"]
    headless = config["headless"]
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=ChromeDriverManager(version=version).install(),
                              options=chrome_options)
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    main_page = MainPage(driver=driver)
    main_page.authorize()
    return main_page


@pytest.fixture
def campaigns_page(driver):
    return CampaignsPage(driver=driver)


@pytest.fixture
def segments_page(driver):
    return SegmentsPage(driver=driver)
