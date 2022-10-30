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

    def create_campaign(self, title="Новая кампания test"):
        files = {'file': ('files/256.png', open('files/256.png', 'rb'), 'multipart/form-data')}

        url = "https://target-sandbox.my.com/api/v2/content/static.json"
        response = self.session.post(url=url, files=files, headers=self.get_post_headers(),
                                     allow_redirects=False).json()
        print(response)
        img_id_256 = response['id']

        files = {'file': ('files/600.jpg', open('files/600.jpg', 'rb'), 'multipart/form-data')}

        url = "https://target-sandbox.my.com/api/v2/content/static.json"
        response = self.session.post(url=url, files=files, headers=self.get_post_headers(),
                                     allow_redirects=False).json()
        img_id_600 = response['id']

        url = "https://target-sandbox.my.com/api/v1/urls/?url=vk.com"
        response = self.session.get(url=url, headers=self.get_post_headers(),
                                    allow_redirects=False).json()
        url_id = response['id']

        data = {
            "name": title,
            "read_only": False,
            "conversion_funnel_id": None,
            "objective": "traffic",
            "enable_offline_goals": False,
            "targetings": {
                "split_audience": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10
                ],
                "sex": [
                    "male",
                    "female"
                ],
                "age": {
                    "age_list": [
                        0,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                        26,
                        27,
                        28,
                        29,
                        30,
                        31,
                        32,
                        33,
                        34,
                        35,
                        36,
                        37,
                        38,
                        39,
                        40,
                        41,
                        42,
                        43,
                        44,
                        45,
                        46,
                        47,
                        48,
                        49,
                        50,
                        51,
                        52,
                        53,
                        54,
                        55,
                        56,
                        57,
                        58,
                        59,
                        60,
                        61,
                        62,
                        63,
                        64,
                        65,
                        66,
                        67,
                        68,
                        69,
                        70,
                        71,
                        72,
                        73,
                        74,
                        75
                    ],
                    "expand": True
                },
                "geo": {
                    "regions": [
                        188
                    ]
                },
                "interests_soc_dem": [],
                "segments": [],
                "interests": [],
                "fulltime": {
                    "flags": [
                        "use_holidays_moving",
                        "cross_timezone"
                    ],
                    "mon": [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23
                    ],
                    "tue": [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23
                    ],
                    "wed": [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23
                    ],
                    "thu": [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23
                    ],
                    "fri": [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23
                    ],
                    "sat": [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23
                    ],
                    "sun": [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23
                    ]
                },
                "pads": [
                    102634,
                    102643
                ],
                "mobile_types": [
                    "tablets",
                    "smartphones"
                ],
                "mobile_vendors": [],
                "mobile_operators": []
            },
            "age_restrictions": None,
            "date_start": None,
            "date_end": None,
            "autobidding_mode": "second_price_mean",
            "budget_limit_day": None,
            "budget_limit": None,
            "mixing": "fastest",
            "utm": None,
            "enable_utm": True,
            "price": "1.64",
            "max_price": "0",
            "package_id": 814,
            "banners": [
                {
                    "urls": {
                        "url_slide_1": {
                            "id": url_id
                        },
                        "url_slide_2": {
                            "id": url_id
                        },
                        "url_slide_3": {
                            "id": url_id
                        },
                        "header_click": {
                            "id": url_id
                        }
                    },
                    "textblocks": {
                        "title_25_slide_1": {
                            "text": "Еуывмы"
                        },
                        "title_25_slide_2": {
                            "text": "Аапвап"
                        },
                        "title_25_slide_3": {
                            "text": "ВАыпв"
                        },
                        "title_25": {
                            "text": "чап"
                        },
                        "text_50": {
                            "text": "вап"
                        },
                        "cta_sites_full": {
                            "text": "visitSite"
                        }
                    },
                    "content": {
                        "image_600x600_slide_1": {
                            "id": img_id_600
                        },
                        "image_600x600_slide_2": {
                            "id": img_id_600
                        },
                        "image_600x600_slide_3": {
                            "id": img_id_600
                        },
                        "icon_256x256": {
                            "id": img_id_256
                        }
                    },
                    "name": ""
                }
            ]
        }

        url = "https://target-sandbox.my.com/api/v2/campaigns.json"
        response = self.session.post(url=url, json=data, headers=self.get_post_headers(),
                                     allow_redirects=False)

        return response.json()['id']

    def delete_campaign(self, campaign_id):
        data = [...]

        url = ...

        return self.session.post(url=url, json=data, headers=self.get_post_headers(), allow_redirects=False).json()

    def campaign_in_campaigns(self, campaign_id):
        url = "https://target-sandbox.my.com/api/v2/banners.json"
        campaings_list = self.session.get(url=url, headers=self.get_post_headers()).json()
        campaigns = campaings_list["items"]
        print(campaigns)
        for campaign in campaigns:
            if campaign["campaign_id"] == campaign_id:
                return True
        return False
