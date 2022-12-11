import pytest

from api.api_base import ApiBase


class TestApi(ApiBase):
    @pytest.mark.parametrize("root, expected_status_code", [(True, 200), (False, 401)])
    def test_add_user(self, mysql_builder, root, expected_status_code):
        data = mysql_builder.get_fake_user()
        response = self.api_client.add_user(name=data['name'], surname=data['surname'], username=data['username'],
                                            password=data['password'], email=data['email'], root=root)
        self.api_client.delete_user(data['username'])
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_add_existent_username(self, create_fake_user, mysql_builder, root, expected_status_code):
        username = create_fake_user['username']
        data = mysql_builder.get_fake_user()
        response = self.api_client.add_user(name=data['name'], surname=data['surname'], username=username,
                                            password=data['password'], email=data['email'], root=root)
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_add_existent_email(self, create_fake_user, mysql_builder, root, expected_status_code):
        email = create_fake_user['email']
        data = mysql_builder.get_fake_user()
        response = self.api_client.add_user(name=data['name'], surname=data['surname'], username=data['username'],
                                            password=data['password'], email=email, root=root)
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize("root, expected_status_code", [(True, 200), (False, 401)])
    def test_edit_users_password(self, mysql_builder,
                                 create_fake_user, root, expected_status_code):  # пароль остается старый, но в таблице меняется
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.edit_users_password(username=username, new_password='12345', root=root)
        print(mysql_builder.client.select_by_username(username))
        new_password = mysql_builder.client.select_by_username(username).password
        assert response.status_code == expected_status_code  # and new_password == '12345'

    @pytest.mark.parametrize("root, expected_status_code", [(True, 204), (False, 401)])
    def test_delete_user(self, create_fake_user, root, expected_status_code):
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.delete_user(username, root=root)
        # проверить в бд
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize("root, expected_status_code", [(True, 404), (False, 401)])
    def test_delete_non_existent_user(self, mysql_builder, root, expected_status_code):
        data = mysql_builder.get_fake_user()
        response = self.api_client.delete_user(data['username'], root=root)
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize("root, expected_status_code", [(True, 200), (False, 401)])
    def test_block_user(self, create_fake_user, root, expected_status_code):
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.block_user(username=username, root=root)
        # проверить в бд
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize("root, expected_status_code", [(True, 404), (False, 401)])
    def test_block_non_existent_user(self, mysql_builder, root, expected_status_code):
        data = mysql_builder.get_fake_user()
        response = self.api_client.block_user(username=data['username'], root=root)
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize("root", [True, False])
    def test_block_blocked_user(self, create_fake_user, root):
        username, password = create_fake_user['username'], create_fake_user['password']
        self.api_client.block_user(username)
        response = self.api_client.block_user(username, root=root)
        # проверить в бд
        assert response.status_code == 400

    @pytest.mark.parametrize("root, expected_status_code", [(True, 200), (False, 401)])
    def test_unblock_user(self, create_fake_user, root, expected_status_code):
        username, password = create_fake_user['username'], create_fake_user['password']
        self.api_client.block_user(username)
        response = self.api_client.unblock_user(username=username, root=root)
        # проверить в бд
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize("root, expected_status_code", [(True, 404), (False, 401)])
    def test_unblock_non_existent_user(self, mysql_builder, root, expected_status_code):
        data = mysql_builder.get_fake_user()
        response = self.api_client.unblock_user(username=data['username'], root=root)
        assert response.status_code == expected_status_code

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_unblock_unblocked_user(self, create_fake_user, root, expected_status_code):
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.unblock_user(username=username, root=root)
        # проверить в бд
        assert response.status_code == expected_status_code

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
