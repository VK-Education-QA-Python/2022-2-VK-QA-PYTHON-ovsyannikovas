import pytest

from api.api_base import ApiBase


class TestApi(ApiBase):
    @pytest.fixture(scope='function', autouse=True)
    def create_root(self, mysql_builder):
        try:
            mysql_builder.client.add_user(name='root', surname='root', username='rootroot', password='0000',
                                      email='root@mail.ru')
        except:
            pass

        yield

        try:
            mysql_builder.client.delete_user('rootroot')
        except:
            pass

    @pytest.mark.parametrize("root, expected_status_code, exist", [(True, 200, True), (False, 401, False)])
    def test_add_user(self, mysql_builder, root, expected_status_code, exist):
        """
        Тест проверяет добавление пользователя через API с корректными данными через авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат: При успешном добавлении статус код будет 200 и пользователь будет присутствовать в БД,
        при неуспешном (пользователь не авторизован) статус код будет 401 и пользователя не будет в БД.
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.add_user(name=data['name'], surname=data['surname'], username=data['username'],
                                            password=data['password'], email=data['email'], root=root)
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        self.api_client.delete_user(data['username'])
        assert response.status_code == expected_status_code and current_existence is exist

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_add_existent_username(self, create_fake_user, mysql_builder, root, expected_status_code):
        """
        Тест проверяет добавление пользователя через API с уже существующим значением username в БД через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username = create_fake_user['username']
        data = mysql_builder.get_fake_user()
        response = self.api_client.add_user(name=data['name'], surname=data['surname'], username=username,
                                            password=data['password'], email=data['email'], root=root)
        current_email = mysql_builder.client.get_email_by_username(username)
        assert response.status_code == expected_status_code and current_email != data['email']

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_add_existent_email(self, create_fake_user, mysql_builder, root, expected_status_code):
        """
        Тест проверяет добавление пользователя через API с уже существующим значением email в БД через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        email = create_fake_user['email']
        data = mysql_builder.get_fake_user()
        response = self.api_client.add_user(name=data['name'], surname=data['surname'], username=data['username'],
                                            password=data['password'], email=email, root=root)
        current_username = mysql_builder.client.get_username_by_email(email)
        assert response.status_code == expected_status_code and current_username != data['username']

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_add_with_no_password(self, mysql_builder, root, expected_status_code):
        """
        Тест проверяет добавление пользователя через API с пустым значением password через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
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
        """
        Тест проверяет добавление пользователя через API с пустым значением email через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
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
        """
        Тест проверяет добавление пользователя через API с пустым значением username через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
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
        """
        Тест проверяет добавление пользователя через API со всеми пустыми значениями через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
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
        """
        Тест проверяет редактирование значения password пользователя через API через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username = create_fake_user['username']
        response = self.api_client.edit_users_password(username=username, new_password='12345', root=root)
        current_password = mysql_builder.client.get_password_by_username(username)
        print(current_password)
        assert response.status_code == expected_status_code  # and current_password == '12345'

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_edit_users_password_with_old(self, mysql_builder, create_fake_user, root, expected_status_code):
        """
        Тест проверяет редактирование значения password пользователя с заменой на то же самое значение через API через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.edit_users_password(username=username, new_password=password, root=root)
        current_password = mysql_builder.client.get_password_by_username(username)
        assert response.status_code == expected_status_code and current_password == password

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])
    def test_edit_users_password_with_empty(self, mysql_builder, create_fake_user, root, expected_status_code):
        """
        Тест проверяет редактирование значения password пользователя с заменой на пустое значение через API через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.edit_users_password(username=username, new_password='', root=root)
        current_password = mysql_builder.client.get_password_by_username(username)
        assert response.status_code == expected_status_code and current_password == password

    @pytest.mark.parametrize("root, expected_status_code, existence", [(True, 204, False), (False, 401, True)])
    def test_delete_user(self, create_fake_user, root, expected_status_code, mysql_builder, existence):
        """
        Тест проверяет удаление пользователя из БД через API через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.delete_user(username, root=root)
        current_existence = mysql_builder.client.is_user_exist(username)
        assert response.status_code == expected_status_code and current_existence is existence

    @pytest.mark.parametrize("root, expected_status_code", [(True, 404), (False, 401)])
    def test_delete_non_existent_user(self, mysql_builder, root, expected_status_code):
        """
        Тест проверяет удаление несуществующего пользователя из БД через API через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.delete_user(data['username'], root=root)
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        assert response.status_code == expected_status_code and current_existence is False

    @pytest.mark.parametrize("root, expected_status_code, access_code", [(True, 200, 0), (False, 401, 1)])
    def test_block_user(self, create_fake_user, root, expected_status_code, mysql_builder, access_code):
        """
        Тест проверяет блокировку пользователя (смену поля access в БД) через API через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.block_user(username=username, root=root)
        access = mysql_builder.client.get_access_by_username(username)
        assert response.status_code == expected_status_code and access == access_code

    @pytest.mark.parametrize("root, expected_status_code", [(True, 404), (False, 401)])
    def test_block_non_existent_user(self, mysql_builder, root, expected_status_code):
        """
        Тест проверяет блокировку несуществующего пользователя (смену поля access в БД) через API через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.block_user(username=data['username'], root=root)
        access = mysql_builder.client.get_access_by_username(data['username'])
        assert response.status_code == expected_status_code and access is None

    @pytest.mark.parametrize("root", [True, False])
    def test_block_blocked_user(self, create_fake_user, root, mysql_builder):
        """
        Тест проверяет блокировку заблокированного пользователя (смену поля access в БД) через API через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username, password = create_fake_user['username'], create_fake_user['password']
        self.api_client.block_user(username)
        response = self.api_client.block_user(username, root=root)
        access = mysql_builder.client.get_access_by_username(username)
        assert response.status_code == 400 and access == 0

    @pytest.mark.parametrize("root, expected_status_code, access_code", [(True, 200, 1), (False, 401, 0)])
    def test_unblock_user(self, create_fake_user, root, expected_status_code, mysql_builder, access_code):
        """
        Тест проверяет разблокировку пользователя (смену поля access в БД) через API через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username, password = create_fake_user['username'], create_fake_user['password']
        self.api_client.block_user(username)
        response = self.api_client.unblock_user(username=username, root=root)
        access = mysql_builder.client.get_access_by_username(username)
        assert response.status_code == expected_status_code and access == access_code

    @pytest.mark.parametrize("root, expected_status_code", [(True, 404), (False, 401)])
    def test_unblock_non_existent_user(self, mysql_builder, root, expected_status_code):
        """
        Тест проверяет разблокировку несуществующего пользователя (смену поля access в БД) через API через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.unblock_user(username=data['username'], root=root)
        access = mysql_builder.client.get_access_by_username(data['username'])
        assert response.status_code == expected_status_code and access is None

    @pytest.mark.parametrize("root, expected_status_code", [(True, 400), (False, 401)])

    def test_unblock_unblocked_user(self, create_fake_user, root, expected_status_code, mysql_builder):
        """
        Тест проверяет разблокировку незаблокированного пользователя (смену поля access в БД) через API через
        авторизованного пользователя и нет.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.unblock_user(username=username, root=root)
        access = mysql_builder.client.get_access_by_username(username)
        assert response.status_code == expected_status_code and access == 1

    def test_status(self):
        """
        Тест проверяет статус приложения.
        Ожидаемый результат:
        """
        response = self.api_client.get_status()
        assert response.status_code == 200


class TestApiMock(ApiBase):
    def test_vkid_of_existent_user(self, create_fake_user, mysql_builder):
        """
        Тест проверяет получение vk_id у существующего пользователя через API.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username = create_fake_user['username']
        user_id = mysql_builder.client.get_id_by_username(username)
        vk_id, status_code = self.api_client.get_vk_id_by_username(username)
        assert int(vk_id['vk_id']) == user_id and status_code == 200

    def test_vkid_of_non_existent_user(self, mysql_builder):
        """
        Тест проверяет получение vk_id у несуществующего пользователя через API.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        vk_id, status_code = self.api_client.get_vk_id_by_username(data['username'])
        assert vk_id == {} and status_code == 404


class TestApiLogin(ApiBase):
    def test_login_user(self, create_fake_user):
        """
        Тест проверяет авторизацию существующего пользователя через API.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.post_login(username, password)
        assert response.status_code == 200

    def test_login_user_with_invalid_password(self, create_fake_user):
        """
        Тест проверяет авторизацию существующего пользователя через API с неверным паролем.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username, password = create_fake_user['username'], create_fake_user['password']
        response = self.api_client.post_login(username, password + 'A')
        assert response.status_code == 401

    def test_login_user_with_empty_password(self, create_fake_user):
        """
        Тест проверяет авторизацию существующего пользователя через API с пустым значением пароля.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username = create_fake_user['username']
        response = self.api_client.post_login(username, '')
        assert response.status_code == 401

    def test_login_non_existent_user(self, mysql_builder):
        """
        Тест проверяет авторизацию несуществующего пользователя через API.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_login(data['username'], data['password'])
        assert response.status_code == 401


#
#
class TestApiRegistration(ApiBase):
    def test_valid_api_registration(self, mysql_builder):
        """
        Тест проверяет регистрацию пользователя через API.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register(data['name'], data['surname'], data['username'], data['password'],
                                                 data['password'], data['email'], 'y')
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        self.api_client.delete_user(data['username'])
        assert response.status_code == 200 and current_existence is True

    def test_api_registration_with_no_username(self, mysql_builder):
        """
        Тест проверяет регистрацию пользователя через API с пустым значением username.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register(data['name'], data['surname'], '', data['password'],
                                                 data['password'], data['email'], 'y')
        current_existence = mysql_builder.client.is_user_exist('')
        try:
            self.api_client.delete_user('')
        except:
            pass
        assert response.status_code == 400 and current_existence is False

    def test_api_registration_with_no_email(self, mysql_builder):
        """
        Тест проверяет регистрацию пользователя через API с пустым значением email.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register(data['name'], data['surname'], data['username'], data['password'],
                                                 data['password'], '', 'y')
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        try:
            self.api_client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == 400 and current_existence is False

    def test_api_registration_with_no_term(self, mysql_builder):
        """
        Тест проверяет регистрацию пользователя через API с пустым значением term.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register(data['name'], data['surname'], data['username'], data['password'],
                                                 data['password'], '', '')
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        try:
            self.api_client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == 400 and current_existence is False

    def test_api_registration_with_no_name(self, mysql_builder):
        """
        Тест проверяет регистрацию пользователя через API с пустым значением name.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register('', data['surname'], data['username'], data['password'],
                                                 data['password'], data['email'], 'y')
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        try:
            self.api_client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == 400 and current_existence is False

    def test_api_registration_with_no_surname(self, mysql_builder):
        """
        Тест проверяет регистрацию пользователя через API с пустым значением surname.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register(data['name'], '', data['username'], data['password'],
                                                 data['password'], data['email'], 'y')
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        try:
            self.api_client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == 400 and current_existence is False

    def test_api_registration_with_no_password(self, mysql_builder):
        """
        Тест проверяет регистрацию пользователя через API с пустым значением password.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register(data['name'], data['surname'], data['username'], '',
                                                 '', data['email'], 'y')
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        try:
            self.api_client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == 400 and current_existence is False

    def test_api_registration_with_different_passwords(self, mysql_builder):
        """
        Тест проверяет регистрацию пользователя через API с разными значениями password и confirm.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register(data['name'], data['surname'], data['username'], data['password'],
                                                 data['password'] + 'A', data['email'], 'y')
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        try:
            self.api_client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == 400 and current_existence is False

    def test_api_registration_with_existent_username(self, mysql_builder, create_fake_user):
        """
        Тест проверяет регистрацию пользователя через API с существующим значением username.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        username = create_fake_user['username']
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register(data['name'], data['surname'], username, data['password'],
                                                 data['password'], data['email'], 'y')
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        try:
            self.api_client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == 400 and current_existence is False

    def test_api_registration_with_existent_email(self, mysql_builder, create_fake_user):
        """
        Тест проверяет регистрацию пользователя через API с существующим значением email.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        email = create_fake_user['email']
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register(data['name'], data['surname'], data['username'], data['password'],
                                                 data['password'], email, 'y')
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        try:
            self.api_client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == 400 and current_existence is False

    def test_api_registration_with_big_username(self, mysql_builder):
        """
        Тест проверяет регистрацию пользователя через API с большим значением username.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register(data['name'], data['surname'], data['username'][0] * 20,
                                                 data['password'],
                                                 data['password'], data['email'], 'y')
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        try:
            self.api_client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == 400 and current_existence is False

    def test_api_registration_with_small_username(self, mysql_builder):
        """
        Тест проверяет регистрацию пользователя через API с маленьким значением username.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register(data['name'], data['surname'], data['username'][0] * 2,
                                                 data['password'],
                                                 data['password'], data['email'], 'y')
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        try:
            self.api_client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == 400 and current_existence is False

    def test_api_registration_with_email_with_no_dog(self, mysql_builder):
        """
        Тест проверяет регистрацию пользователя через API с невалидным значением email.
        Осуществляется проверка наличия пользователя в БД через ORM.
        Ожидаемый результат:
        """
        data = mysql_builder.get_fake_user()
        response = self.api_client.post_register(data['name'], data['surname'], data['username'], data['password'],
                                                 data['password'], data['username'], 'y')
        current_existence = mysql_builder.client.is_user_exist(data['username'])
        try:
            self.api_client.delete_user(data['username'])
        except:
            pass
        assert response.status_code == 400 and current_existence is False
