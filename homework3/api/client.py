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
            'password': self.password
        }
        headers = {
            'Referer': 'https://account.my.com/',
        }
        # getting mc and ssdc cookies
        self.session.post(url='https://auth-ac.my.com/auth', allow_redirects=False,
                          headers=headers, data=data)

        # getting token for next url
        token = self.session.get(
            url='https://auth-ac.my.com/sdc',
            allow_redirects=False,
            headers=headers).headers['Location'].split('=')[-1]

        # getting sdcs cookie
        self.session.get(url=f'https://account.my.com/sdc?token={token}')

        # getting sdc and csrftoken cookies
        self.session.get(url=f'https://target-sandbox.my.com/csrf/')

        login_request = self.session.post(url=self.base_url, headers=headers,
                                          data=data)

        return login_request

    def get_post_headers(self):
        return {
            'Cookie': f"csrftoken={self.session.cookies['csrftoken']}; mc={self.session.cookies['mc']}; "
                      f"sdc={self.session.cookies['sdc']};",
            'X-CSRFToken': f"{self.session.cookies['csrftoken']}",
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
        print(segment_id)
        url = urljoin(self.base_url, 'api/v2/remarketing/segments.json')
        segments_list = self.session.get(url=url, headers=self.get_post_headers()).json()
        print(segments_list)
        segments = segments_list['items']

        for segment in segments:
            if segment['id'] == segment_id:
                return True
        return False

    def create_campaign(self, title):
        path_256 = os.path.join(self.repo_toot, 'files/256.png')
        path_600 = os.path.join(self.repo_toot, 'files/600.jpg')

        # loading 256x256 picture
        files = {'file': (path_256, open(path_256, 'rb'), 'multipart/form-data')}
        url = urljoin(self.base_url, 'api/v2/content/static.json')
        response = self.session.post(url=url, files=files, headers=self.get_post_headers(),
                                     allow_redirects=False).json()
        img_id_256 = response['id']

        # loading 600x600 picture
        files = {'file': (path_600, open(path_600, 'rb'), 'multipart/form-data')}
        response = self.session.post(url=url, files=files, headers=self.get_post_headers(),
                                     allow_redirects=False).json()
        img_id_600 = response['id']

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
