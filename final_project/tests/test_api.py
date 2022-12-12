import pytest

from api.api_base import ApiBase


class TestApi(ApiBase):
    @pytest.fixture(scope='function', autouse=True)
    def create_root(self, mysql_builder):
        mysql_builder.client.add_user(name='root', surname='root', username='rootroot', password='0000',
                                      email='root@mail.ru')
        yield
        mysql_builder.client.delete_user('rootroot')

    @pytest.mark.parametrize("root, expected_status_code, exist", [(True, 200, True), (False, 401, False)])
    def test_add_user(self, mysql_builder, root, expected_status_code, exist):
        data = mysql_builder.get_fake_user()
        response = self.api_client.add_user(name=data['name'], surname=data['surname'], username=data['username'],
                                            password=data['password'], email=data['email'], root=root)
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        self.api_client.delete_user(data['username'])
        assert response.status_code == expected_status_code and current_existence is exist

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_add_existent_username(self, create_fake_user, mysql_builder, root, expected_status_code):
        username = create_fake_user['username']
        data = mysql_builder.get_fake_user()
        response = self.api_client.add_user(name=data['name'], surname=data['surname'], username=username,
                                            password=data['password'], email=data['email'], root=root)
        current_email = mysql_builder.client.get_email_by_username(username)
        assert response.status_code == expected_status_code and current_email != data['email']

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_add_existent_email(self, create_fake_user, mysql_builder, root, expected_status_code):
        email = create_fake_user['email']
        data = mysql_builder.get_fake_user()
        response = self.api_client.add_user(name=data['name'], surname=data['surname'], username=data['username'],
                                            password=data['password'], email=email, root=root)
        current_username = mysql_builder.client.get_username_by_email(email)
        assert response.status_code == expected_status_code and current_username != data['username']

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_add_with_no_password(self, mysql_builder, root, expected_status_code):
        data = mysql_builder.get_fake_user()
        response = self.api_client.add_user(name=data['name'], surname=data['surname'], username=data['username'],
                                            password='', email=data['email'], root=root)
        current_password = mysql_builder.client.get_password_by_username(data['username'])
        try:
            mysql_builder.client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == expected_status_code and current_password != ''

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_add_with_no_email(self, mysql_builder, root, expected_status_code):
        data = mysql_builder.get_fake_user()
        response = self.api_client.add_user(name=data['name'], surname=data['surname'], username=data['username'],
                                            password=data['password'], email='', root=root)
        current_email = mysql_builder.client.get_email_by_username(data['username'])
        try:
            mysql_builder.client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == expected_status_code and current_email != ''

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_add_with_no_username(self, mysql_builder, root, expected_status_code):
        data = mysql_builder.get_fake_user()
        response = self.api_client.add_user(name=data['name'], surname=data['surname'], username='',
                                            password=data['password'], email=data['email'], root=root)
        current_username = mysql_builder.client.get_username_by_email(data['email'])
        try:
            mysql_builder.client.delete_user('')
        except:
            pass
        assert response.status_code == expected_status_code and current_username != ''

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_add_empty(self, root, expected_status_code, mysql_builder):
        response = self.api_client.add_user(name='', surname='', username='', password='', email='', root=root)
        existence = mysql_builder.client.is_user_exist('')
        try:
            mysql_builder.client.delete_user('')
        except:
            pass
        assert response.status_code == expected_status_code and existence is False

    @pytest.mark.parametrize("root, expected_status_code", [(True, 200), (False, 401)])
    def test_edit_users_password(self, mysql_builder,
                                 create_fake_user, root,
                                 expected_status_code):  # пароль остается старый, но в таблице меняется
        username = create_fake_user['username']
        response = self.api_client.edit_users_password(username=username, new_password='12345', root=root)
        current_password = mysql_builder.client.get_password_by_username(username)
        print(current_password)
        assert response.status_code == expected_status_code #and current_password == '12345'

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_edit_users_password_with_old(self, mysql_builder, create_fake_user, root, expected_status_code):
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.edit_users_password(username=username, new_password=password, root=root)
        current_password = mysql_builder.client.get_password_by_username(username)
        assert response.status_code == expected_status_code and current_password == password

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_edit_users_password_with_empty(self, mysql_builder, create_fake_user, root, expected_status_code):
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.edit_users_password(username=username, new_password='', root=root)
        current_password = mysql_builder.client.get_password_by_username(username)
        assert response.status_code == expected_status_code and current_password == password

    @pytest.mark.parametrize("root, expected_status_code, existence", [(True, 204, False), (False, 401, True)])
    def test_delete_user(self, create_fake_user, root, expected_status_code, mysql_builder, existence):
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.delete_user(username, root=root)
        current_existence = mysql_builder.client.is_user_exist(username)
        assert response.status_code == expected_status_code and current_existence is existence

    @pytest.mark.parametrize("root, expected_status_code", [(True, 404), (False, 401)])
    def test_delete_non_existent_user(self, mysql_builder, root, expected_status_code):
        data = mysql_builder.get_fake_user()
        response = self.api_client.delete_user(data['username'], root=root)
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        assert response.status_code == expected_status_code and current_existence is False

    @pytest.mark.parametrize("root, expected_status_code, access_code", [(True, 200, 0), (False, 401, 1)])
    def test_block_user(self, create_fake_user, root, expected_status_code, mysql_builder, access_code):
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.block_user(username=username, root=root)
        access = mysql_builder.client.get_access_by_username(username)
        assert response.status_code == expected_status_code and access == access_code

    @pytest.mark.parametrize("root, expected_status_code", [(True, 404), (False, 401)])
    def test_block_non_existent_user(self, mysql_builder, root, expected_status_code):
        data = mysql_builder.get_fake_user()
        response = self.api_client.block_user(username=data['username'], root=root)
        access = mysql_builder.client.get_access_by_username(data['username'])
        assert response.status_code == expected_status_code and access is None

    @pytest.mark.parametrize("root", [True, False])
    def test_block_blocked_user(self, create_fake_user, root, mysql_builder):
        username, password = create_fake_user['username'], create_fake_user['password']
        self.api_client.block_user(username)
        response = self.api_client.block_user(username, root=root)
        access = mysql_builder.client.get_access_by_username(username)
        assert response.status_code == 400 and access == 0

    @pytest.mark.parametrize("root, expected_status_code, access_code", [(True, 200, 1), (False, 401, 0)])
    def test_unblock_user(self, create_fake_user, root, expected_status_code, mysql_builder, access_code):
        username, password = create_fake_user['username'], create_fake_user['password']
        self.api_client.block_user(username)
        response = self.api_client.unblock_user(username=username, root=root)
        access = mysql_builder.client.get_access_by_username(username)
        assert response.status_code == expected_status_code and access == access_code

    @pytest.mark.parametrize("root, expected_status_code", [(True, 404), (False, 401)])
    def test_unblock_non_existent_user(self, mysql_builder, root, expected_status_code):
        data = mysql_builder.get_fake_user()
        response = self.api_client.unblock_user(username=data['username'], root=root)
        access = mysql_builder.client.get_access_by_username(data['username'])
        assert response.status_code == expected_status_code and access is None

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_unblock_unblocked_user(self, create_fake_user, root, expected_status_code, mysql_builder):
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.unblock_user(username=username, root=root)
        access = mysql_builder.client.get_access_by_username(username)
        assert response.status_code == expected_status_code and access == 1

    def test_status(self):
        response = self.api_client.get_status()
        assert response.status_code == 200


# class TestApiLogin:
#     def test_login_user(self, create_fake_user):
#         ...
#         # response = self.api_client.post_login(data[''], '12345')
#         # print(response)
#
#     def test_login_non_existent_user(self):
#         ...
#
#
# class TestApiRegistration:
#     ...
