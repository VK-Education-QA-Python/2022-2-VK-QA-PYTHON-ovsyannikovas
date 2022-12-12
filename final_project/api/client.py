import os
from urllib.parse import urljoin

import pytest
import requests


class ApiClient:

    def __init__(self, url, username=None, password=None):
        self.url = url
        self.session = requests.Session()
        self.root_username = username
        self.root_password = password

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
        return response

    def add_user(self, name, surname, username, password, email, middle_name=None, root=True):
        if root:
            self.post_login(self.root_username, self.root_password)
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
        return response

    def delete_user(self, username, root=True):
        if root:
            self.post_login(self.root_username, self.root_password)
        response = self.session.delete(f'{self.url}api/user/{username}')
        return response

    def edit_users_password(self, username, new_password, root=True):
        if root:
            self.post_login(self.root_username, self.root_password)
        body = {
            "password": new_password
        }
        response = self.session.put(f'{self.url}api/user/{username}/change-password', data=body)
        return response

    def block_user(self, username, root=True):
        if root:
            self.post_login(self.root_username, self.root_password)
        response = self.session.post(f'{self.url}api/user/{username}/block')
        return response

    def unblock_user(self, username, root=True):
        if root:
            self.post_login(self.root_username, self.root_password)
        response = self.session.post(f'{self.url}api/user/{username}/accept')
        return response

    def get_status(self):
        response = requests.get(f'{self.url}status')
        return response
