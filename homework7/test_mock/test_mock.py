from base import TestBase


class TestUserGet(TestBase):

    def test_get_users(self):
        resp = self.get_users()

        assert resp.status_code == 200

    def test_get_non_existent_user(self):
        resp = self.get_user(user_id=12345)

        assert resp.status_code == 404

    def test_get_existent_user(self, add_user_id):
        resp = self.get_user(add_user_id)

        assert resp.status_code == 200


class TestUserAdd(TestBase):
    def test_add_get_user(self, add_user_id):
        resp = self.get_user(add_user_id)
        user_id_from_get = resp.json()['id']

        assert add_user_id == user_id_from_get

    def test_add_existent_user(self):
        resp = self.add_user('Kostya')

        assert resp.status_code == 400


class TestUserDelete(TestBase):
    def test_delete_existent_user(self, add_user_id):
        resp = self.delete_user(user_id=add_user_id)

        assert resp.status_code == 200

    def test_delete_non_existent_user(self):
        resp = self.delete_user(user_id=12345)

        assert resp.status_code == 404


class TestUserPut(TestBase):

    def test_edit_existent_user(self, add_user_id):
        new_name = 'Sveta'
        resp = self.edit_user(add_user_id, username=new_name)

        assert resp.json()['name'] == new_name

    def test_edit_non_existent_user(self, add_user_id):
        new_name = 'Sveta'
        resp = self.edit_user(user_id=12345, username=new_name)

        assert resp.status_code == 404
