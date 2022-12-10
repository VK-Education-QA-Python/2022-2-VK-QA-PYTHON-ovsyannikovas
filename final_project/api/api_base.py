import pytest


class ApiBase:
    authorize = False

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client

        if self.authorize:
            self.api_client.post_login()

    def post_login(self, username, password):
        self.api_client.post_login(username=username, password=password)

