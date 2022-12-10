from selenium.webdriver.common.by import By


class MainPageLocators:
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "[href='/logout']")

    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON_FORM = (By.CSS_SELECTOR, "[class^='authForm-module-button']")


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
