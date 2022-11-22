import os
from urllib.parse import urljoin

import requests


class ApiClient:

    def __init__(self, base_url: str, login: str, password: str, repo_root: str):
        self.base_url = base_url
        self.login = login
        self.password = password
        self.repo_toot = repo_root
        self.session = requests.Session()

    def post_login(self):
        data = {
            'email': self.login,
            'password': self.password,
            "continue": "https://target-sandbox.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email",
            "failure": "https://account.my.com/login/"
        }
        headers = {
            'Referer': 'https://account.my.com/',
        }
        # getting mc and ssdc cookies
        self.session.post(url='https://auth-ac.my.com/auth', allow_redirects=False,
                          headers=headers, data=data)

        # getting sdc and csrftoken cookies
        self.session.get(url=f'https://target-sandbox.my.com/csrf/')

        login_request = self.session.post(url=self.base_url, headers=headers,
                                          data=data)

        return login_request

    def get_post_headers(self):
        return {
            'Cookie': f"csrftoken={self.session.cookies.get('csrftoken')}; mc={self.session.cookies.get('mc')}; "
                      f"sdc={self.session.cookies.get('sdc')};",
            'X-CSRFToken': f"{self.session.cookies.get('csrftoken')}",
        }

    def create_segment(self, title, segment_type='remarketing_player'):
        data = {
            'name': title,
            'pass_condition': 1,
            'relations': [
                {
                    'object_type': segment_type,
                    'params': {
                        'type': 'positive',
                        'left': 365,
                        'right': 0
                    }
                }
            ],
            'logicType': 'or'
        }

        url = urljoin(self.base_url, 'api/v2/remarketing/segments.json')

        return self.session.post(url=url, json=data, headers=self.get_post_headers(), allow_redirects=False).json()[
            'id']

    def delete_segment(self, segment_id):
        data = [
            {
                'source_id': segment_id,
                'source_type': 'segment'
            }
        ]

        url = urljoin(self.base_url, 'api/v1/remarketing/mass_action/delete.json')

        return self.session.post(url=url, json=data, headers=self.get_post_headers(), allow_redirects=False).json()

    def segment_in_segments(self, segment_id):
        url = urljoin(self.base_url, f'api/v2/remarketing/segments/{segment_id}.json')
        response = self.session.get(url=url, headers=self.get_post_headers()).json()
        return response.get('id') == segment_id

    def get_img_id(self, path):
        files = {'file': (path, open(path, 'rb'), 'multipart/form-data')}
        url = urljoin(self.base_url, 'api/v2/content/static.json')
        response = self.session.post(url=url, files=files, headers=self.get_post_headers(),
                                     allow_redirects=False).json()
        return response['id']

    def create_campaign(self, title):
        path_256 = os.path.join(self.repo_toot, 'files/256.png')
        path_600 = os.path.join(self.repo_toot, 'files/600.jpg')

        # loading 256x256 picture
        img_id_256 = self.get_img_id(path_256)

        # loading 600x600 picture
        img_id_600 = self.get_img_id(path_600)

        # loading url
        url = urljoin(self.base_url, 'api/v1/urls/?url=vk.com')
        response = self.session.get(url=url, headers=self.get_post_headers(),
                                    allow_redirects=False).json()
        url_id = response['id']

        data = {
            'name': title,
            'objective': 'traffic',
            'package_id': 814,
            'banners': [
                {
                    'urls': {
                        'url_slide_1': {
                            'id': url_id
                        },
                        'url_slide_2': {
                            'id': url_id
                        },
                        'url_slide_3': {
                            'id': url_id
                        },
                        'header_click': {
                            'id': url_id
                        }
                    },
                    'textblocks': {
                        'title_25_slide_1': {
                            'text': 'Заголовок 1'
                        },
                        'title_25_slide_2': {
                            'text': 'Заголовок 2'
                        },
                        'title_25_slide_3': {
                            'text': 'Заголовок 3'
                        },
                        'title_25': {
                            'text': 'Текст 25'
                        },
                        'text_50': {
                            'text': 'Текст 50'
                        },
                        'cta_sites_full': {
                            'text': 'visitSite'
                        }
                    },
                    'content': {
                        'image_600x600_slide_1': {
                            'id': img_id_600
                        },
                        'image_600x600_slide_2': {
                            'id': img_id_600
                        },
                        'image_600x600_slide_3': {
                            'id': img_id_600
                        },
                        'icon_256x256': {
                            'id': img_id_256
                        }
                    },
                    'name': ''
                }
            ]
        }

        url = urljoin(self.base_url, 'api/v2/campaigns.json')
        response = self.session.post(url=url, json=data, headers=self.get_post_headers(),
                                     allow_redirects=False)
        return response.json()['id']

    def delete_campaign(self, campaign_id):
        data = [
            {
                'id': campaign_id,
                'status': 'deleted'
            }
        ]
        url = urljoin(self.base_url, 'api/v2/campaigns/mass_action.json')
        self.session.post(url=url, json=data, headers=self.get_post_headers(), allow_redirects=False)

    def campaign_in_campaigns(self, campaign_id):
        url = urljoin(self.base_url, f'api/v2/campaigns/{campaign_id}.json?fields=id,name,status')
        status = self.session.get(url=url, headers=self.get_post_headers()).json()['status']
        return status == 'active'
