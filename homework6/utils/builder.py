from models.models import *
from scripts.script import get_data


class MysqlBuilder:
    def __init__(self, client):
        self.client = client
        self.data = get_data()

    def fill_tables(self):
        self.fill_task1()
        self.fill_task2()
        self.fill_task3()
        self.fill_task4()
        self.fill_task5()
        self.client.session.commit()

    def fill_task1(self):
        self.client.session.add(Task1(amount=self.data[1]['amount']))

    def fill_task2(self):
        for method, num in self.data[2].items():
            self.client.session.add(Task2(method=method, amount=num))

    def fill_task3(self):
        for url, num in self.data[3].items():
            self.client.session.add(Task3(url=url, amount=num))

    def fill_task4(self):
        data = self.data[4]
        head_num = len(data['ip'])
        for i in range(head_num):
            self.client.session.add(Task4(
                ip=data['ip'][i],
                url=data['url'][i],
                status=data['status'][i],
                amount=data['requests_amount'][i],
            ))

    def fill_task5(self):
        for ip, num in self.data[5].items():
            self.client.session.add(Task5(ip=ip, amount=num))
