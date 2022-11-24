import requests

import settings
from mock.flask_mock import app_data
from base import TestBase

url = f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}'


class TestMock:

    def test_get_users(self, add_user_id):
        resp = requests.get(f'{url}/')

        assert resp.status_code == 200

    def test_add_get_user(self, add_user_id):
        resp = requests.get(f'{url}/get_user/{add_user_id}')
        user_id_from_get = resp.json()['id']

        assert add_user_id == user_id_from_get

    def test_add_existent_user(self, add_user_id):
        resp = requests.post(f'{url}/add_user', json={'name': 'Kostya'})

        assert resp.status_code == 400

    def test_get_non_existent_user(self, add_user_id):
        resp = requests.get(f'{url}/12345')

        assert resp.status_code == 404

    def test_get_existent_user(self, add_user_id):
        resp = requests.get(f'{url}/get_user/{add_user_id}')

        assert resp.status_code == 200

    def test_delete_existent_user(self, add_user_id):
        resp = requests.delete(f'{url}/delete_user/{add_user_id}')

        assert resp.status_code == 200

    def test_delete_non_existent_user(self, add_user_id):
        resp = requests.delete(f'{url}/delete_user/12345')

        assert resp.status_code == 404

    def test_edit_existent_user(self, add_user_id):
        new_name = 'Sveta'
        resp = requests.put(f'{url}/edit_user/{add_user_id}', json={'name': new_name})

        assert resp.json()['name'] == new_name

    def test_edit_non_existent_user(self, add_user_id):
        new_name = 'Sveta'
        resp = requests.put(f'{url}/edit_user/12345', json={'name': new_name})

        assert resp.status_code == 404
