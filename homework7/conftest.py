import logging
import os
import time

import pytest
import requests

import settings


@pytest.fixture(scope='function', autouse=True)
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


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        from mock import flask_mock
        flask_mock.run_mock()
        wait_ready(settings.MOCK_HOST, settings.MOCK_PORT)


def pytest_unconfigure(config):
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def temp_dir(request, repo_root):
    test_dir = os.path.join(os.path.join(repo_root, 'logs'), request._pyfuncitem.nodeid)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='session')
def logger(temp_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()
