import os
import time

import pytest
import requests

import settings

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))


# @pytest.fixture(scope='session')
# def repo_root():
#     return os.path.abspath(os.path.join(__file__, os.path.pardir))

@pytest.fixture(scope='function')
def add_user_id():
    url = f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}'
    resp = requests.post(f'{url}/add_user', json={'name': 'Kostya'})
    user_id = resp.json()['id']
    yield user_id
    try:
        requests.delete(f'{url}/delete_user/{user_id}')
    except:
        pass


def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError('App did not started in 5s!')


# @pytest.fixture(scope='session')
# def configure(config):
#     if not hasattr(config, 'workerinput'):
#         from mock import flask_mock
#         flask_mock.run_mock()
#         wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)
#
#         yield
#
#         requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        from mock import flask_mock
        flask_mock.run_mock()
        wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)


def pytest_unconfigure(config):
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')
