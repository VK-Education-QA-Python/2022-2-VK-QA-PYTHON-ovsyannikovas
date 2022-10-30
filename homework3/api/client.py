from urllib.parse import urljoin

import requests


class ApiClientException(Exception):
    ...


class ResponseStatusCodeException(Exception):
    pass


class RespondErrorException(Exception):
    pass


class ApiClient:
    BLOG_ID = 431

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
        self.session.post(url="https://auth-ac.my.com/auth?lang=ru&nosavelogin=0", allow_redirects=False,
                          headers=headers, data=data)

        # getting token for next url
        token = self.session.get(
            url="https://auth-ac.my.com/sdc?from=https%3A%2F%2Faccount.my.com%2Flogin_continue%2F%3Fcontinue%3Dhttps%253A%252F%252Faccount.my.com",
            allow_redirects=False,
            headers=headers).headers['Location'].split('=')[-1]

        # getting sdcs cookie
        self.session.get(url=f"https://account.my.com/sdc?token={token}")

        # getting sdc and csrftoken cookies
        self.session.get(url=f"https://target-sandbox.my.com/csrf/")

        login_request = self.session.post(url='https://target-sandbox.my.com/', headers=headers,
                                          data=data)

        return login_request

    def _request(self, method, location, headers, data, params=None, allow_redirects=False, expected_status=200,
                 jsonify=True):
        url = urljoin(self.base_url, location)

        response = self.session.request(method=method, url=url, headers=headers, data=data, params=params,
                                        allow_redirects=allow_redirects)

        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Expected {expected_status}, but got {response.status_code}')
        if jsonify:
            json_response: dict = response.json()
            if json_response.get('bStateError', False):
                error = json_response['sErrorMsg']
                raise RespondErrorException(f'Request {url} return error : "{error}"')

            return json_response
        return response

    def post_topic_create(self, title, text):
        data = {
            'title': title,
            'text': text,
            'forbid_comment': 'false',
            'is_news': 'false',
            'important': 'false',
            'lessons': '',
            'blog': self.BLOG_ID,
        }

        headers = {
            'Cookie': f'sessionid_gtp={self.session.cookies["sessionid_gtp"]};'
                      f' csrftoken={self.session.cookies["csrftoken"]}',
            'X-CSRFToken': f'{self.session.cookies["csrftoken"]}'
        }

        location = urljoin(self.base_url, 'blog/topic/create/')
        return self._request(method='POST', location=location, data=data, headers=headers)


c = ApiClient("https://target-sandbox.my.com/", 'minipersik02@gmail.com', 'testpass')
c.post_login()
print(c.session.get('https://target-sandbox.my.com/dashboard/').url == 'https://target-sandbox.my.com/dashboard/')
