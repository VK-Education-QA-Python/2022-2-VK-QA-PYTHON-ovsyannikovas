import pytest

from models.models import *
from base import MyTest


class TestMysql(MyTest):
    def test_table_len_task1(self):
        assert self.get_model_len(Task1) == len(self.builder.data[1])

    def test_table_len_task2(self):
        assert self.get_model_len(Task2) == len(self.builder.data[2])

    def test_table_len_task3(self):
        assert self.get_model_len(Task3) == len(self.builder.data[3])

    def test_table_len_task4(self):
        assert self.get_model_len(Task4) == len(self.builder.data[4])

    def test_table_len_task5(self):
        assert self.get_model_len(Task5) == len(self.builder.data[5])
