from api.api_base import ApiBase


class TestApi(ApiBase):
    def test_add_user(self, create_fake_user):
        username, password = create_fake_user['username'], create_fake_user['password']
        self.api_client.post_login(username, password)
        response = self.api_client.add_user(name='testname', surname='testsurname', username='testusername',
                                            password='testpass', email='test@mail.ru')
        # assert response.status_code == 200
        # response = self.api_client.delete_user(username='testusername', password=password)
        # assert response.status_code == 200

    def test_add_existent_username_and_password(self, create_fake_user):
        username, password = create_fake_user['username'], create_fake_user['password']
        self.api_client.post_login(username, password)
        response = self.api_client.add_user(name='testname', surname='testsurname', username=username,
                                            password=password, email='test@mail.ru')

    def test_add_existent_username(self, create_fake_user):
        username, password = create_fake_user['username'], create_fake_user['password']
        self.api_client.post_login(username, password)
        response = self.api_client.add_user(name='testname', surname='testsurname', username=username,
                                            password='password', email='test@mail.ru')

    # def test_add_existent_email(self, create_fake_user):
    #     username, password = create_fake_user
    #     self.api_client.post_login(username, password)
    #     response = self.api_client.add_user(name='testname', surname='testsurname', username=username,
    #                                         password=password, email='test@mail.ru')

    def test_edit_users_password(self, mysql_builder,
                                 create_fake_user):  # пароль остается старый, но в таблице меняется
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.edit_users_password(username=username, old_password=password, new_password='12345')
        print(mysql_builder.client.select_by_username(username))
        new_password = mysql_builder.client.select_by_username(username).password
        assert response.status_code == 200  # and new_password == '12345'

    def test_delete_user(self, create_fake_user):
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.delete_user(username, password)
        assert response.status_code == 204

    def test_delete_non_existent_user(self):  # post login здеся
        response = self.api_client.delete_user('username1', 'password')
        assert response.status_code == 204

    def test_block_user(self, create_fake_user):
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.block_user(username=username, password=password)
        assert response.status_code == 200

    def test_block_non_existent_user(self, mysql_builder):
        data = mysql_builder.get_fake_user()
        response = self.api_client.block_user(username=data['username'], password=data['password'])
        assert response.status_code == 401

    def test_unblock_user(self):
        ...

    def test_unblock_non_existent_user(self):
        ...
        # data = mysql_builder.get_fake_user()
        # response = self.api_client.block_user(username=data['username'], password=data['password'])

    def test_ubblock_unblocked_user(self):
        ...

    def test_status(self):
        response = self.api_client.get_status()
        assert response.status_code == 200


class TestApiLogin:
    def test_login_user(self, create_fake_user):  # в начале регистрация
        ...
        # response = self.api_client.post_login(data[''], '12345')
        # print(response)

    def test_login_non_existent_user(self):
        ...


class TestApiRegistration:
    ...
