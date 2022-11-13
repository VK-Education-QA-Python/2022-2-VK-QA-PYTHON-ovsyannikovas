import pytest

from models.models import *
from base import MyTest


class TestMysql(MyTest):

    @pytest.mark.parametrize('model, index', [(Task1, 1),
                                              (Task2, 2),
                                              (Task3, 3),
                                              (Task4, 4),
                                              (Task5, 5)])
    def test_table_len(self, model, index):
        assert self.get_model_len(model) == len(self.builder.data[index])
