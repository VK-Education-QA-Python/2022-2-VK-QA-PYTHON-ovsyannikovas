import os

import pytest

from api.client import ApiClient


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default='https://target-sandbox.my.com/')


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')

    return {
        'browser': browser,
        'url': url,
    }


@pytest.fixture(scope='session')
def credentials():
    user = 'minipersik02@gmail.com'
    password = 'testpass'

    return user, password


# @pytest.fixture(scope='session')
# def api_client(credentials, config, repo_root):
#     return ApiClient(base_url=config['url'], login=credentials[0], password=credentials[1], repo_root=repo_root)
