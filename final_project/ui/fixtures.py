import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.register_page import RegisterPage


@pytest.fixture()
def driver(config):
    url = config["url"]
    headless = config["headless"]
    selenoid = config['selenoid']
    vnc = config['vnc']
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument('--headless')
    if selenoid:
        capabilities = {
            "browserName": "chrome",
            "browserVersion": "107.0",
            "selenoid:options": {
                "enableVideo": False,
                # "AdditionalNetworks": ["selenoid"],
                # "enableVNC": vnc
            },
        }
        driver = webdriver.Remote(
            'http://localhost:4444/wd/hub/',
            desired_capabilities=capabilities,
            options=chrome_options)
    else:
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
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
