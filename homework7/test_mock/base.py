import json

import pytest
import requests

import settings


class TestBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, logger):
        self.url = f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}'
        # self.logger = logger

    def add_user(self, username):
        response = requests.post(f'{self.url}/add_user', json={'name': username})
        # self.logger.info(json.dumps(self.create_log(response=resp, method='POST')))
        return response

    def get_user(self, user_id):
        response = requests.get(f'{self.url}/get_user/{user_id}')
        # self.logger.info(json.dumps(self.create_log(response=resp, method='GET')))
        return response

    def get_users(self):
        response = requests.get(f'{self.url}/')
        # self.logger.info(json.dumps(self.create_log(response=resp, method='GET')))
        return response

    def edit_user(self, user_id, username):
        response = requests.put(f'{self.url}/edit_user/{user_id}', json={'name': username})
        # self.logger.info(json.dumps(self.create_log(response=resp, method='PUT')))
        return response

    def delete_user(self, user_id):
        resp = requests.delete(f'{self.url}/delete_user/{user_id}')
        # self.logger.info(json.dumps(self.create_log(response=resp, method='DELETE')))
        return resp

    def create_log(self, response, method):
        data = {
            'Status code': response.status_code,
            'Method': method,
            # 'Body': response.body
        }
        return data
