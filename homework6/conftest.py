import pytest
from mysql.client import MysqlClient

tables = (
    'Task1',
    'Task2',
    'Task3',
    'Task4',
    'Task5',
)


def pytest_configure(config):
    mysql_client = MysqlClient()
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)
    if not hasattr(config, 'workerinput'):
        mysql_client.create_tables(tables)

    config.mysql_client = mysql_client


@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.connection.close()
