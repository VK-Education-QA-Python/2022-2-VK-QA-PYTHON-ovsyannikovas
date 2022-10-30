import pytest


@pytest.fixture(scope='session')
def credentials():
    user = 'minipersik02@gmail.com'
    password = 'testpass'

    return user, password


class TestLkApi:
    @pytest.fixture(scope='class', autouse=True)
    def setup(self, api_client):
        api_client.post_login()

    @pytest.mark.API
    def test_api_login(self, api_client):
        assert api_client.session.get('https://target-sandbox.my.com/dashboard/').url == \
               'https://target-sandbox.my.com/dashboard/'

    @pytest.mark.API
    def test_api_segment_creation(self, api_client):
        segment_id = api_client.create_segment()
        print(segment_id)
        # assert api_client.segment_in_segments(segment_id)
        response = api_client.delete_segment(segment_id)
        print(response)
