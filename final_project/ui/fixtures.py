import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.register_page import RegisterPage


@pytest.fixture()
def driver(config):
    # version = "105.0.5195.19"
    url = config["url"]
    headless = config["headless"]
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                              options=chrome_options)
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def main_page(driver, config, login_page, create_fake_user):
    main_page = MainPage(driver=driver)
    driver.get(config['url'])
    username, password = create_fake_user['username'], create_fake_user['password']
    login_page.authorize(username, password)
    return main_page


@pytest.fixture
def login_page(driver, config):
    login_page = LoginPage(driver=driver)
    driver.get(''.join((config['url'], login_page.url)))
    return login_page


@pytest.fixture
def register_page(driver, config):
    register_page = RegisterPage(driver=driver)
    driver.get(''.join((config['url'], register_page.url)))
    return register_page
