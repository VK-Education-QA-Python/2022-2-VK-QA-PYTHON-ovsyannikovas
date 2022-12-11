from selenium.webdriver.common.by import By


class MainPageLocators:
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "[href='/logout']")

    LOGO_BUTTON = (By.CSS_SELECTOR, '[class*="uk-navbar-brand"]')
    HOME_BUTTON = (By.CSS_SELECTOR, "[href='/']")

    PYTHON_BUTTON = (By.XPATH, "//a[.='Python']")
    PYTHON_HISTORY_BUTTON = (By.XPATH, '//a[.="Python"]/following::div/ul/li/a[.="Python history"]')
    ABOUT_FLASK_BUTTON = (By.XPATH, '//a[.="Python"]/following::div/ul/li/a[.="About Flask"]')

    LINUX_BUTTON = (By.XPATH, "//a[.='Linux']")
    DOWNLOAD_CENTOS7_BUTTON = (By.XPATH, '//a[.="Linux"]/following::div/ul/li/a')

    NETWORK_BUTTON = (By.XPATH, "//a[.='Network']")
    WIRESHARK_NEWS_BUTTON = (By.XPATH, '//a[.="Network"]/following::div/ul/li[1]/ul/li/a[.="News"]')
    WIRESHARK_DOWNLOAD_BUTTON = (By.XPATH, '//a[.="Network"]/following::div/ul/li[1]/ul/li/a[.="Download"]')
    TCP_DUMP_EXAMPLES = (By.XPATH, '//a[.="Network"]/following::div/ul/li/ul/li/a[.="Examples "]')

    API_IMG = (By.CSS_SELECTOR, "[href*='Application_programming_interface']")
    FUTURE_IMG = (By.CSS_SELECTOR, "[href*='future-of-the-internet/']")
    SMTP_IMG = (By.CSS_SELECTOR, "[href*='SMTP']")

    QUOTE = (By.CSS_SELECTOR, 'footer div p:first-child')


class RegisterPageLocators:
    NAME_FIELD = (By.ID, 'user_name')
    SURNAME_FIELD = (By.ID, 'user_surname')
    MIDDLE_NAME_FIELD = (By.ID, 'user_middle_name')
    USERNAME_FIELD = (By.ID, 'username')
    EMAIL_FIELD = (By.ID, 'email')
    PASSWORD1_FIELD = (By.ID, 'password')
    PASSWORD2_FIELD = (By.ID, 'confirm')
    ACCEPT_CHECKBOX = (By.ID, 'term')
    REGISTER_BUTTON = (By.ID, 'submit')
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[href='/login']")
    REGISTER_ERROR_MESSAGE = (By.ID, 'flash')


class LoginPageLocators:
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "submit")
    CREATE_ACC_BUTTON = (By.CSS_SELECTOR, "[href='/reg']")
    LOGIN_ERROR_MESSAGE = (By.ID, 'flash')
