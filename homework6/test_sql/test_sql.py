from models.models import *
from base import BaseTest
from scripts.script import get_task1_dict, get_task2_dict, get_task3_dict, get_task4_dict, get_task5_dict


class TestMysql(BaseTest):
    def test_table_len_task1(self):
        self.prepare_table1()
        assert self.get_model_len(Task1) == len(get_task1_dict(self.path))

    def test_table_len_task2(self):
        self.prepare_table2()
        assert self.get_model_len(Task2) == len(get_task2_dict(self.path))

    def test_table_len_task3(self):
        self.prepare_table3()
        assert self.get_model_len(Task3) == len(get_task3_dict(self.path))

    def test_table_len_task4(self):
        self.prepare_table4()
        assert self.get_model_len(Task4) == len(get_task4_dict(self.path))

    def test_table_len_task5(self):
        self.prepare_table5()
        assert self.get_model_len(Task5) == len(get_task5_dict(self.path))
