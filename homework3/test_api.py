import pytest

from base import ApiBase


class TestLkApi(ApiBase):
    @pytest.mark.API
    def test_api_login(self):
        assert self.api_client.session.get('https://target-sandbox.my.com/dashboard/').url == \
               'https://target-sandbox.my.com/dashboard/'

    @pytest.mark.API
    def test_api_campaign_creation(self):
        campaign_id = self.create_campaign()
        assert self.campaign_in_campaigns(campaign_id)
        self.delete_campaign(campaign_id)
        assert self.campaign_in_campaigns(campaign_id) is False

    @pytest.mark.API
    def test_api_segment_creation(self):
        segment_id = self.create_segment()
        assert self.segment_in_segments(segment_id)
        self.delete_segment(segment_id)
        assert self.segment_in_segments(segment_id) is False
