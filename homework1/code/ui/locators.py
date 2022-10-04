from selenium.webdriver.common.by import By

LOGIN_BUTTON_MENU = (By.CSS_SELECTOR, "[class^='responseHead-module-rightSide'] [class^='responseHead-module-button']")
EMAIL_FIELD = (By.NAME, "email")
PASSWORD_FIELD = (By.NAME, "password")
LOGIN_BUTTON_FORM = (By.CSS_SELECTOR, "[class^='authForm-module-button']")

USER_NAME_BUTTON = (By.CSS_SELECTOR, "[class^='right-module-userNameWrap']")
EMAIL_BUTTON = (By.CSS_SELECTOR, "[class^='right-module-rightWrap']")
INSTRUCTION = (By.CSS_SELECTOR, "[class*='instruction-module']")
LOGOUT_BUTTON = (By.CSS_SELECTOR, "[class*='rightMenu-module-rightMenu'] a[href='/logout']")

EMAIL_ERROR_MESSAGE = (By.CSS_SELECTOR, "[class*='undefined notify-module-error']")
LOGIN_ERROR_MESSAGE = (By.CSS_SELECTOR, "[class*='formMsg_text']")

FIO = (By.CSS_SELECTOR, ".input[data-name='fio'] input")
INN = (By.CSS_SELECTOR, ".input[data-name='ordInn'] input")
PHONE = (By.CSS_SELECTOR, ".input[data-name='phone'] input")
SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[data-class-name='Submit']")
SUCCESS_MESSAGE = (By.CSS_SELECTOR, "[data-class-name='SuccessView']")

SEGMENTS = (By.CSS_SELECTOR, "a[class*='center-module-segments']")
STATISTICS = (By.CSS_SELECTOR, "a[class*='center-module-statistics']")
SEGMENTS_EXPECTED = (By.CSS_SELECTOR, "a[href='/segments/segments_list']")
STATISTICS_EXPECTED = (By.CSS_SELECTOR, "a[href='/statistics/summary']")





