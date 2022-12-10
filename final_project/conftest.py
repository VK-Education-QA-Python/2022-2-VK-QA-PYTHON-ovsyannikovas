import logging
import os
import shutil
import sys

from mysql.builder import MysqlBuilder
from mysql.client import MysqlClient
from ui.fixtures import *
from api.client import ApiClient


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true")
    parser.addoption("--url", default="http://localhost:8000/")


@pytest.fixture()
def config(request):
    url = request.config.getoption("--url")
    headless = request.config.getoption("--headless")
    return {"url": url, "headless": headless}


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
    return ApiClient(url=config['url'])


@pytest.fixture(scope='session')
def mysql_builder(mysql_client) -> MysqlBuilder:
    return MysqlBuilder(mysql_client)


@pytest.fixture(scope='function')
def create_fake_user(mysql_builder):
    person = mysql_builder.add_fake_user()
    data = {
        'username': person.username,
        'password': person.password,
        'email': person.email
    }

    yield data

    mysql_builder.client.delete_user(data['username'])


# @pytest.fixture(scope='session')
# def repo_root():
#     return os.path.abspath(os.path.join(__file__, os.path.pardir))


# @pytest.fixture(scope='session')
# def base_temp_dir():
#     if sys.platform.startswith('win'):
#         base_dir = 'C:\\tests'
#     else:
#         base_dir = '/tmp/tests'
#     if os.path.exists(base_dir):
#         shutil.rmtree(base_dir)
#     return base_dir
#
#
# @pytest.fixture(scope='function')
# def temp_dir(base_temp_dir, request):
#     # test_dir = '\\'.join((base_temp_dir, request._pyfuncitem.nodeid.replace('::', '\\')))
#     test_dir = os.path.join(base_temp_dir, request._pyfuncitem.nodeid)
#     os.makedirs(test_dir)
#     return test_dir
#
#
# @pytest.fixture
# def file_path(repo_root, filename='userdata.jpg'):
#     return os.path.join(repo_root, 'files', filename)
