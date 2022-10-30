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

    # def _request(self, method, location, headers, data, params=None, allow_redirects=False, expected_status=200,
    #              jsonify=True):
    #     # url = urljoin(self.base_url, location)
    #     url = location
    #
    #     response = self.session.request(method=method, url=url, headers=headers, data=data, params=params,
    #                                     allow_redirects=allow_redirects)
    #
    #     if response.status_code != expected_status:
    #         raise ResponseStatusCodeException(f'Expected {expected_status}, but got {response.status_code}')
    #     # if jsonify:
    #     #     json_response: dict = response.json()
    #     #     if json_response.get('bStateError', False):
    #     #         error = json_response['sErrorMsg']
    #     #         raise RespondErrorException(f'Request {url} return error : "{error}"')
    #     #
    #     #     return json_response
    #     return response

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

        headers = {
            'Cookie': f'csrftoken={self.session.cookies["csrftoken"]}; mc={self.session.cookies["mc"]}; sdc={self.session.cookies["sdc"]};',
            'X-CSRFToken': f'{self.session.cookies["csrftoken"]}',
        }

        url = urljoin(self.base_url, 'api/v2/remarketing/segments.json')
        # url = "https://target-sandbox.my.com/segments/segments_list/new"
        return self.session.post(url=url, json=data, headers=headers, allow_redirects=False).json()['id']

    def delete_segment(self, segment_id):
        data = [
            {
                "source_id": segment_id,
                "source_type": "segment"
            }
        ]

        url = "https://target-sandbox.my.com/api/v1/remarketing/mass_action/delete.json"
        # location = "https://target-sandbox.my.com/segments/segments_list"
        headers = {
            'Cookie': f'csrftoken={self.session.cookies["csrftoken"]}; mc={self.session.cookies["mc"]}; sdc={self.session.cookies["sdc"]};',
            'X-CSRFToken': f'{self.session.cookies["csrftoken"]}',
        }
        print(headers)

        return self.session.post(url=url, json=data, headers=headers, allow_redirects=False).json()

    def segment_in_segments(self, segment_id):
        headers = {
            'Cookie': f'csrftoken={self.session.cookies["csrftoken"]}; mc={self.session.cookies["mc"]}; sdc={self.session.cookies["sdc"]};',
            'X-CSRFToken': f'{self.session.cookies["csrftoken"]}',
        }
        url = "https://target-sandbox.my.com/api/v2/remarketing/segments.json"
        segments_list = self.session.get(url=url, headers=headers).json()


c = ApiClient("https://target-sandbox.my.com/", 'minipersik02@gmail.com', 'testpass')
c.post_login()
print(c.session.get('https://target-sandbox.my.com/dashboard/').url == 'https://target-sandbox.my.com/dashboard/')
