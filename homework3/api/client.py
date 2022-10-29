import requests


class ApiClientException(Exception):
    ...


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
            'Cookie': ''
        }
        # getting mc and ssdc cookies
        self.session.post(url="https://auth-ac.my.com/auth?lang=ru&nosavelogin=0", allow_redirects=False,
                          headers=headers, data=data)
        cookies_dict = dict(self.session.cookies)
        headers['Cookie'] += f'mc={cookies_dict["mc"]}; ssdc={cookies_dict["ssdc"]}; '

        # getting token for next url
        token = self.session.get(
            url="https://auth-ac.my.com/sdc?from=https%3A%2F%2Faccount.my.com%2Flogin_continue%2F%3Fcontinue%3Dhttps%253A%252F%252Faccount.my.com",
            allow_redirects=False,
            headers=headers).headers['Location'].split('=')[-1]

        # getting sdcs cookie
        self.session.get(url=f"https://account.my.com/sdc?token={token}")
        cookies_dict = dict(self.session.cookies)
        headers['Cookie'] += f'sdcs={cookies_dict["sdcs"]}; '

        # getting sdc and csrftoken cookies
        self.session.get(url=f"https://target-sandbox.my.com/csrf/")
        cookies_dict = dict(self.session.cookies)
        headers['Cookie'] += f'sdc={cookies_dict["sdc"]}; csrftoken={cookies_dict["csrftoken"]}; '

        login_request = self.session.post(url='https://target-sandbox.my.com/', headers=headers,
                                          data=data)

        return login_request


c = ApiClient("https://target-sandbox.my.com/", 'minipersik02@gmail.com', 'testpass')
c.post_login()
print(c.session.get('https://target-sandbox.my.com/dashboard/').url == 'https://target-sandbox.my.com/dashboard/')
