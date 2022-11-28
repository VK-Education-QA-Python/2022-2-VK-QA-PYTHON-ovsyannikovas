import os

import pytest
from mysql.client import MysqlClient


def pytest_configure(config):
    mysql_client = MysqlClient()
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)

    config.mysql_client = mysql_client


@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.connection.close()


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def file_path(repo_root, filename='access.log'):
    return os.path.join(repo_root, 'scripts', filename)
