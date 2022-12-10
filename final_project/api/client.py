import os
from urllib.parse import urljoin

import pytest
import requests


class ApiClient:

    def __init__(self, url):
        self.url = url  # f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}'
        self.session = requests.Session()

    def post_login(self, username, password):
        data = {
            'username': username,
            'password': password,
            'submit': 'Login'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = self.session.post(f'{self.url}login', data=data, headers=headers)
        print('post_login', response.status_code)
        return response

    def add_user(self, name, surname, username, password, email, middle_name=None):
        body = {
            "name": name,
            "surname": surname,
            "username": username,
            "password": password,
            "email": email
        }
        if username:
            body['middle_name'] = middle_name
        response = self.session.post(f'{self.url}api/user', json=body)
        print('add_user', response.status_code)
        return response

    def delete_user(self, username, password):
        self.post_login(username, password)
        response = self.session.delete(f'{self.url}api/user/{username}')
        print('delete_user', response.status_code)
        return response

    def edit_users_password(self, username, old_password, new_password):
        self.post_login(username, old_password)
        body = {
            "password": new_password
        }
        response = self.session.put(f'{self.url}api/user/{username}/change-password', data=body)
        print(response.status_code)
        return response

    def block_user(self, username, password):
        self.post_login(username, password)
        response = requests.post(f'{self.url}api/user/{username}/block')
        print('block_user', response.status_code)
        return response

    def unblock_user(self, username, password):
        self.post_login(username, password)
        response = requests.post(f'{self.url}api/user/{username}/accept')
        return response

    def get_status(self):
        response = requests.get(f'{self.url}status')
        return response
