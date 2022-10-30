import pytest


@pytest.fixture(scope='session')
def credentials():
    user = 'minipersik02@gmail.com'
    password = 'testpass'

    return user, password


class TestLkApi:
    @pytest.fixture(scope='class', autouse=True)
    def setup(self, api_client):
        api_client.post_login()

    @pytest.mark.API
    def test_api_login(self, api_client):
        assert api_client.session.get('https://target-sandbox.my.com/dashboard/').url == \
               'https://target-sandbox.my.com/dashboard/'

    @pytest.mark.API
    def test_campaign_creation(self, api_client):
        api_client.session.get('https://target-sandbox.my.com/dashboard/')

    def test_browser(self):
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        driver.get("https://target-sandbox.my.com/")
        import time;
        time.sleep(6000)
