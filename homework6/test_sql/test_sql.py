from models.models import *
from base import BaseTest
from scripts.script import get_task1_dict, get_task2_dict, get_task3_dict, get_task4_dict, get_task5_dict


class TestMysql(BaseTest):
    def test_table_len_task1(self):
        self.prepare_table1()
        data_dict = get_task1_dict(self.path)
        assert self.get_model_len(Task1) == len(data_dict) and \
               self.get_model_first_row(Task1).amount == data_dict['amount']

    def test_table_len_task2(self):
        self.prepare_table2()
        data_dict = get_task2_dict(self.path)
        assert self.get_model_len(Task2) == len(data_dict) and \
               self.get_model_first_row(Task2).amount == data_dict['GET']

    def test_table_len_task3(self):
        self.prepare_table3()
        data_dict = get_task3_dict(self.path)
        assert self.get_model_len(Task3) == len(data_dict) and \
               self.get_model_first_row(Task3).amount == data_dict['/administrator/index.php']

    def test_table_len_task4(self):
        self.prepare_table4()
        data_dict = get_task4_dict(self.path)
        assert self.get_model_len(Task4) == len(data_dict) and \
               self.get_model_first_row(Task4).ip == data_dict['ip'][0] and \
               self.get_model_first_row(Task4).url == data_dict['url'][0] and \
               str(self.get_model_first_row(Task4).status) == data_dict['status'][0]

    def test_table_len_task5(self):
        self.prepare_table5()
        data_dict = get_task5_dict(self.path)
        assert self.get_model_len(Task5) == len(data_dict) and \
               self.get_model_first_row(Task5).amount == data_dict['189.217.45.73']
