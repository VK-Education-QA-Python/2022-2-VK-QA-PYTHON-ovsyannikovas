import datetime

import pytest


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client

        if self.authorize:
            self.api_client.post_login()

    def create_campaign(self, title=f'Новая кампания {str(datetime.datetime.now())}'):
        return self.api_client.create_campaign(title=title)

    def campaign_in_campaigns(self, campaign_id):
        return self.api_client.campaign_in_campaigns(campaign_id)

    def delete_campaign(self, campaign_id):
        self.api_client.delete_campaign(campaign_id)

    def create_segment(self, title=f'Новый аудиторный сегмент {str(datetime.datetime.now())}',
                       segment_type='remarketing_player'):
        return self.api_client.create_segment(title=title, segment_type=segment_type)

    def segment_in_segments(self, segment_id):
        return self.api_client.segment_in_segments(segment_id)

    def delete_segment(self, segment_id):
        self.api_client.delete_segment(segment_id)
