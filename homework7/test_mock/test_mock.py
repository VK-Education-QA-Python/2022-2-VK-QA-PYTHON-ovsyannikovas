import requests

import settings
from mock.flask_mock import app_data
from base import BaseTest

url = f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}'


def test_add_get_user(add_user_id):
    resp = requests.get(f'{url}/get_user/{add_user_id}')
    user_id_from_get = resp.json()['id']

    assert add_user_id == user_id_from_get


def test_add_existent_user(add_user_id):
    resp = requests.post(f'{url}/add_user', json={'name': 'Kostya'})

    assert resp.status_code == 400


def test_get_non_existent_user(add_user_id):
    resp = requests.get(f'{url}/12345')

    assert resp.status_code == 404


def test_get_existent_user(add_user_id):
    resp = requests.get(f'{url}/get_user/{add_user_id}')

    assert resp.status_code == 200


def test_delete_existent_user(add_user_id):
    resp = requests.delete(f'{url}/delete_user/{add_user_id}')

    assert resp.status_code == 200


def test_delete_non_existent_user(add_user_id):
    resp = requests.delete(f'{url}/delete_user/12345')

    assert resp.status_code == 404
