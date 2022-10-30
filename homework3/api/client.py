from urllib.parse import urljoin

import requests


class ApiClientException(Exception):
    ...


class ResponseStatusCodeException(Exception):
    pass


class RespondErrorException(Exception):
    pass


class ApiClient:

    def __init__(self, base_url: str, login: str, password: str):
        self.base_url = base_url
        self.login = login
        self.password = password
        self.session = requests.Session()

    def post_login(self):
        data = {
            'email': self.login,
            'password': self.password
        }
        headers = {
            'Referer': 'https://account.my.com/',
        }
        # getting mc and ssdc cookies
        self.session.post(url="https://auth-ac.my.com/auth", allow_redirects=False,
                          headers=headers, data=data)

        # getting token for next url
        token = self.session.get(
            url="https://auth-ac.my.com/sdc",
            allow_redirects=False,
            headers=headers).headers['Location'].split('=')[-1]

        # getting sdcs cookie
        self.session.get(url=f"https://account.my.com/sdc?token={token}")

        # getting sdc and csrftoken cookies
        self.session.get(url=f"https://target-sandbox.my.com/csrf/")

        login_request = self.session.post(url='https://target-sandbox.my.com/', headers=headers,
                                          data=data)

        return login_request

    def get_post_headers(self):
        return {
            'Cookie': f'csrftoken={self.session.cookies["csrftoken"]}; mc={self.session.cookies["mc"]}; sdc={self.session.cookies["sdc"]};',
            'X-CSRFToken': f'{self.session.cookies["csrftoken"]}',
        }

    def create_segment(self, title="Новый аудиторный сегмент test"):
        data = {
            "name": title,
            "pass_condition": 1,
            "relations": [
                {
                    "object_type": "remarketing_player",
                    "params": {
                        "type": "positive",
                        "left": 365,
                        "right": 0
                    }
                }
            ],
            "logicType": "or"
        }

        url = urljoin(self.base_url, 'api/v2/remarketing/segments.json')

        return self.session.post(url=url, json=data, headers=self.get_post_headers(), allow_redirects=False).json()[
            'id']

    def delete_segment(self, segment_id):
        data = [
            {
                "source_id": segment_id,
                "source_type": "segment"
            }
        ]

        url = urljoin(self.base_url, 'api/v1/remarketing/mass_action/delete.json')

        return self.session.post(url=url, json=data, headers=self.get_post_headers(), allow_redirects=False).json()

    def segment_in_segments(self, segment_id):
        url = urljoin(self.base_url, 'api/v2/remarketing/segments.json')
        segments_list = dict(self.session.get(url=url, headers=self.get_post_headers()).json())
        segments = segments_list["items"]

        for segment in segments:
            if segment["id"] == segment_id:
                return True
        return False

    def create_campaign(self, title="Новый аудиторный сегмент test"):
        data = {...}

        url = ...

        return self.session.post(url=url, json=data, headers=self.get_post_headers(), allow_redirects=False).json()[
            'id']

    def delete_campaign(self, segment_id):
        data = [...]

        url = ...

        return self.session.post(url=url, json=data, headers=self.get_post_headers(), allow_redirects=False).json()

    def campaign_in_campaigns(self, segment_id):
        url = ...
        segments_list = dict(self.session.get(url=url, headers=self.get_post_headers()).json())
        segments = segments_list["items"]
        for segment in segments:
            if segment["id"] == segment_id:
                return True
        return False
