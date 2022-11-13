import pytest
from mysql.client import MysqlClient
from utils.builder import MysqlBuilder


class MyTest:
    @pytest.fixture(scope='session')
    def prepare(self, mysql_client):
        MysqlBuilder(mysql_client).fill_tables()

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, prepare):
        self.client: MysqlClient = mysql_client
        self.builder: MysqlBuilder = MysqlBuilder(self.client)

    def get_model_len(self, model):
        return len(self.client.session.query(model).all())
