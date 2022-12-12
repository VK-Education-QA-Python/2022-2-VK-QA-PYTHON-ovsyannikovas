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
    return ApiClient(url=config['url'], username='rootroot', password='0000')


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

    if mysql_builder.client.is_user_exist(data['username']):
        mysql_builder.client.delete_user(data['username'])

