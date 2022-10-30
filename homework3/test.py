import pytest


class TestLkApi:
    @pytest.fixture(scope='class', autouse=True)
    def setup(self, api_client):
        api_client.post_login()

    @pytest.mark.API
    def test_api_login(self, api_client):
        assert api_client.session.get('https://target-sandbox.my.com/dashboard/').url == \
               'https://target-sandbox.my.com/dashboard/'

    @pytest.mark.API
    def test_api_campaign_creation(self, api_client):
        campaign_id = api_client.create_campaign()
        print(campaign_id)
        assert api_client.campaign_in_campaigns(campaign_id)
        # api_client.delete_campaign(campaign_id)
        # assert api_client.campaign_in_campaigns(campaign_id) is False

    @pytest.mark.API
    def test_api_segment_creation(self, api_client):
        segment_id = api_client.create_segment()
        assert api_client.segment_in_segments(segment_id)
        api_client.delete_segment(segment_id)
        assert api_client.segment_in_segments(segment_id) is False
