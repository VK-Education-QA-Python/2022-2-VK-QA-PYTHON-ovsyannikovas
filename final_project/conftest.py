import logging
import os
import shutil
import sys

import allure

from mysql.builder import MysqlBuilder
from mysql.client import MysqlClient
from ui.fixtures import *
from api.client import ApiClient


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true")
    parser.addoption("--url", default="http://localhost:8000/")
    parser.addoption('--debug_log', action='store_true')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')


@pytest.fixture()
def config(request):
    url = request.config.getoption("--url")
    headless = request.config.getoption("--headless")
    debug_log = request.config.getoption('--debug_log')
    if request.config.getoption('--selenoid'):
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
        selenoid = "http://127.0.0.1:4444/wd/hub"
    else:
        selenoid = None
        vnc = False

    return {
        'url': url,
        "headless": headless,
        'debug_log': debug_log,
        'selenoid': selenoid,
        'vnc': vnc,
    }


def pytest_configure(config):
    mysql_client = MysqlClient()
    mysql_client.connect(db_created=True)

    config.mysql_client = mysql_client


@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.connection.close()


@pytest.fixture()
def api_client(config):
    return ApiClient(url=config['url'], username='rootroot', password='0000')


@pytest.fixture(scope='session')
def mysql_builder(mysql_client) -> MysqlBuilder:
    return MysqlBuilder(mysql_client)


@allure.step('Создание пользователя в БД')
@pytest.fixture(scope='function')
def create_fake_user(mysql_builder):
    person = mysql_builder.add_fake_user()
    data = {
        'username': person.username,
        'password': person.password,
        'email': person.email
    }
    allure.step(f'Создан пользователь с username: {data["username"]}, email: {data["email"]}, password: {data["password"]}')

    yield data

    if mysql_builder.client.is_user_exist(data['username']):
        mysql_builder.client.delete_user(data['username'])


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def temp_dir(request, repo_root):
    test_dir = '\\'.join(('\\'.join((repo_root, 'logs')), request._pyfuncitem.nodeid.replace('::', '\\')))
    # test_dir = os.path.join(os.path.join(repo_root, 'logs'), request._pyfuncitem.nodeid)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    return test_dir
