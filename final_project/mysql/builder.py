import allure
import faker

from mysql.client import MysqlClient

fake = faker.Faker('ru_RU')


class MysqlBuilder:

    def __init__(self, mysql_client: MysqlClient):
        self.client = mysql_client

    def add_fake_user(self):
        return self.client.add_user(
            name=fake.first_name(),
            surname=fake.last_name(),
            username=''.join(fake.random_letters(6)),
            password=fake.password(),
            email=fake.email(),
        )

    @staticmethod
    @allure.step('Генерация данных для пользователя')
    def get_fake_user():
        return {
            'name': fake.first_name(),
            'surname': fake.last_name(),
            'middle_name': fake.middle_name(),
            'username': ''.join(fake.random_letters(6)),
            'password': fake.password(),
            'email': fake.email(),
        }
