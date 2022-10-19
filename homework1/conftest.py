import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true")
    parser.addoption("--url", default="https://target-sandbox.my.com/")


@pytest.fixture()
def config(request):
    url = request.config.getoption("--url")
    headless = request.config.getoption("--headless")
    return {"url": url, "headless": headless}


@pytest.fixture(scope='function')
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
