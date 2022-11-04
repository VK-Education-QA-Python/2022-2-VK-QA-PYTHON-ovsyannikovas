import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
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
def main_page(driver):
    main_page = MainPage(driver=driver)
    main_page.authorize()
    return main_page


@pytest.fixture
def campaigns_page(driver, main_page):
    main_page.go_to_campaigns_page()
    return CampaignsPage(driver=driver)


@pytest.fixture
def segments_page(driver, main_page):
    main_page.go_to_segments_page()
    return SegmentsPage(driver=driver)


@pytest.fixture(scope='function')
def group(main_page, segments_page):
    main_page.go_to_segments_page()
    segments_page.add_group(url="https://vk.com/vkedu")
    yield
    segments_page.delete_group()
