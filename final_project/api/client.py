import os
from urllib.parse import urljoin

import allure
import pytest
import requests


class ApiClient:

    def __init__(self, url, username=None, password=None):
        self.url = url
        self.vk_id_url = 'http://localhost:9000/'
        self.session = requests.Session()
        self.root_username = username
        self.root_password = password

    @allure.step('Авторизация пользователя через API')
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

    @allure.step('Регистрация пользователя через API')
    def post_register(self, name, surname, username, password, confirm, email, term, middlename=''):
        data = {
            'name': name,
            'surname': surname,
            'middlename': middlename,
            'username': username,
            'email': email,
            'password': password,
            'confirm': confirm,
            'term': term,
            'submit': 'Register'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = self.session.post(f'{self.url}reg', data=data, headers=headers)
        return response

    @allure.step('Добавление пользователя через API')
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

    @allure.step('Удаление пользователя через API')
    def delete_user(self, username, root=True):
        if root:
            self.post_login(self.root_username, self.root_password)
        response = self.session.delete(f'{self.url}api/user/{username}')
        return response

    @allure.step('Редактирование пароля пользователя через API')
    def edit_users_password(self, username, new_password, root=True):
        if root:
            self.post_login(self.root_username, self.root_password)
        body = {
            "password": new_password
        }
        response = self.session.put(f'{self.url}api/user/{username}/change-password', data=body)
        return response

    @allure.step('Блокировка пользователя через API')
    def block_user(self, username, root=True):
        if root:
            self.post_login(self.root_username, self.root_password)
        response = self.session.post(f'{self.url}api/user/{username}/block')
        return response

    @allure.step('Разблокировка пользователя через API')
    def unblock_user(self, username, root=True):
        if root:
            self.post_login(self.root_username, self.root_password)
        response = self.session.post(f'{self.url}api/user/{username}/accept')
        return response

    @allure.step('Получение статуса приложения через API')
    def get_status(self):
        response = requests.get(f'{self.url}status')
        return response

    @allure.step('Получение vk id пользователя через API')
    def get_vk_id_by_username(self, username):
        response = self.session.get(f'{self.vk_id_url}vk_id/{username}')
        return response.json(), response.status_code

    def logout(self):
        response = self.session.get(f'{self.vk_id_url}logout')
        return response
