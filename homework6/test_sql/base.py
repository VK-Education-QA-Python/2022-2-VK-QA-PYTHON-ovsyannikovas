import pytest
from mysql.client import MysqlClient
from models.models import *
from scripts.script import get_task1_dict, get_task2_dict, get_task3_dict, get_task4_dict, get_task5_dict


class BaseTest:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, file_path):
        self.client: MysqlClient = mysql_client
        self.path = file_path

    def get_model_len(self, model):
        return len(self.client.session.query(model).all())

    def get_model_first_row(self, model):
        return self.client.session.query(model).get(1)

    def create_table(self, table_model):
        self.client.create_table(table_model)

    @pytest.fixture()
    def prepare_table1(self):
        self.create_table('Task1')
        self.client.session.add(Task1(amount=get_task1_dict(self.path)['amount']))
        self.client.session.commit()

    @pytest.fixture()
    def prepare_table2(self):
        self.create_table('Task2')
        data = get_task2_dict(self.path)
        for method, num in data.items():
            self.client.session.add(Task2(method=method, amount=num))
        self.client.session.commit()

    @pytest.fixture()
    def prepare_table3(self):
        self.create_table('Task3')
        data = get_task3_dict(self.path)
        for url, num in data.items():
            self.client.session.add(Task3(url=url, amount=num))
        self.client.session.commit()

    @pytest.fixture()
    def prepare_table4(self):
        self.create_table('Task4')
        data = get_task4_dict(self.path)
        head_num = len(data['ip'])
        for i in range(head_num):
            self.client.session.add(Task4(
                ip=data['ip'][i],
                url=data['url'][i],
                status=data['status'][i],
                amount=data['requests_amount'][i],
            ))
        self.client.session.commit()

    @pytest.fixture()
    def prepare_table5(self):
        self.create_table('Task5')
        data = get_task5_dict(self.path)
        for ip, num in data.items():
            self.client.session.add(Task5(ip=ip, amount=num))
        self.client.session.commit()
