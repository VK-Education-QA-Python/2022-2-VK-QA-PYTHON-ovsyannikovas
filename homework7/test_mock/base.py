import json

import pytest
import requests

import settings


class TestBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, logger):
        self.url = f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}'
        self.logger = logger

    def add_user(self, username):
        body = {'name': username}
        response = requests.post(f'{self.url}/add_user', json=body)
        self.logger.info(json.dumps(self.create_log(response=response, method='POST', body=body)))
        return response

    def get_user(self, user_id):
        response = requests.get(f'{self.url}/get_user/{user_id}')
        self.logger.info(json.dumps(self.create_log(response=response, method='GET')))
        return response

    def get_users(self):
        response = requests.get(f'{self.url}/')
        self.logger.info(json.dumps(self.create_log(response=response, method='GET')))
        return response

    def edit_user(self, user_id, username):
        body = {'name': username}
        response = requests.put(f'{self.url}/edit_user/{user_id}', json=body)
        self.logger.info(json.dumps(self.create_log(response=response, method='PUT', body=body)))
        return response

    def delete_user(self, user_id):
        response = requests.delete(f'{self.url}/delete_user/{user_id}')
        self.logger.info(json.dumps(self.create_log(response=response, method='DELETE')))
        return response

    @staticmethod
    def create_log(response, method, body=None):
        if body is None:
            body = {}
        data = {
            'Status code': response.status_code,
            'Method': method,
            'JSON Response': response.json(),
            'Body': body
        }
        return data
