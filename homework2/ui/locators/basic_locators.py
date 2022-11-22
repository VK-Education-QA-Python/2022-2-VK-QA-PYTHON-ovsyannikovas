from selenium.webdriver.common.by import By


class BasePageLocators:
    CAMPAIGNS = (By.CSS_SELECTOR, "a[class*='center-module-campaigns']")
    SEGMENTS = (By.CSS_SELECTOR, "a[class*='center-module-segments']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "[class*='icon-success']")


class MainPageLocators(BasePageLocators):
    LOGIN_BUTTON_MENU = (
        By.CSS_SELECTOR, "[class^='responseHead-module-rightSide'] [class^='responseHead-module-button']")
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON_FORM = (By.CSS_SELECTOR, "[class^='authForm-module-button']")


class CampaignsPageLocators(MainPageLocators):
    # CREATE_CAMPAIGN_BUTTON1 = (By.CSS_SELECTOR, "a[href='/campaign/new']")
    CREATE_CAMPAIGN_BUTTON = (By.CSS_SELECTOR, "[class*='createButton'] [data-test='button']")
    AIM_BUTTON = (By.CSS_SELECTOR, "div[data-class-name='ColumnListItemView']:first-child")
    INPUT_URL = (By.CSS_SELECTOR, "input[data-gtm-id='ad_url_text']")
    BUDGET_SETTING = (By.CSS_SELECTOR, "li[data-scroll-to='setting-budget_setting']")
    FORMAT_ITEM = (By.CSS_SELECTOR, "[id*='patterns_carousel']")
    UPLOAD_IMG600_BUTTON = (By.CSS_SELECTOR, "input[data-test*='image_600x600']")

    @staticmethod
    def slide(n):
        return By.CSS_SELECTOR, f"li[data-id='{n}']"

    @staticmethod
    def slide_link(n):
        return By.CSS_SELECTOR, f"input[data-name='url_slide_{n + 1}']"

    @staticmethod
    def slide_title(n):
        return By.CSS_SELECTOR, f"input[data-name='title_25_slide_{n + 1}']"

    PRICE_SLIDER = (By.CSS_SELECTOR, "[data-class-name='Slider']")
    SAVE_IMG_BUTTON = (By.CSS_SELECTOR, "[data-translated-lit='Save image']")
    UPLOAD_IMG256_BUTTON = (By.CSS_SELECTOR, "input[data-test='icon_256x256']")
    TITLE_FIELD = (By.CSS_SELECTOR, "input[data-name='title_25']")
    TEXT_FIELD = (By.CSS_SELECTOR, "textarea[data-name='text_50']")
    SUBMIT_BANNER_BUTTON = (By.CSS_SELECTOR, "[data-test='submit_banner_button']")
    FINAL_CREATE_CAMPAIGN_BUTTON = (By.CSS_SELECTOR, ".footer__button button[data-class-name='Submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "[class*='icon-success']")


class SegmentsPageLocators(MainPageLocators):
    SEGMENTS_LIST = (By.CSS_SELECTOR, "a[href='/segments/segments_list']")
    # CREATE_SEGMENT_BUTTON = (By.XPATH, ".//div[contains(@class, 'js-create-button-wrap')]/button")
    CREATE_SEGMENT_BUTTON = (
        By.XPATH, "//a[@href='/segments/segments_list/new/'] | //div[contains(@class, 'js-create-button-wrap')]/button")
    CREATE_SEGMENT_BUTTON1 = (By.CSS_SELECTOR, "a[href='/segments/segments_list/new/']")
    CREATE_SEGMENT_BUTTON2 = (By.CSS_SELECTOR, ".js-create-button-wrap button")
    SEGMENT_TYPE_APPS = (By.CLASS_NAME, "adding-segments-item")
    CHECKBOX = (By.CSS_SELECTOR, "input[class*='adding-segments-source__checkbox']")
    ADD_SEGMENT_BUTTON = (By.CSS_SELECTOR, ".adding-segments-modal__footer button[data-class-name='Submit']")
    INPUT_NAME = (By.CSS_SELECTOR, ".input_create-segment-form input")
    FINAL_CREATE_SEGMENT_BUTTON = (By.CSS_SELECTOR, ".create-segment-form__btn-wrap button[data-class-name='Submit']")

    @staticmethod
    def created_segment(name):
        return By.CSS_SELECTOR, f"[title='{name}']"

    GROUPS_LIST_BUTTON = (By.CSS_SELECTOR, "a[href='/segments/groups_list']")
    INPUT_LINK = (By.CSS_SELECTOR, ".segments-groups-ok-list__suggester-wrap input")
    SELECT_ALL_BUTTON = (By.CSS_SELECTOR, "div[data-test='select_all']")
    ADD_SELECTED_BUTTON = (By.CSS_SELECTOR, "div[data-test='add_selected_items_button']")
    SEGMENT_TYPE_GROUPS = (By.CSS_SELECTOR, ".adding-segments-item:last-child")
    CREATED_SEGMENT_CHECKBOX = (By.CSS_SELECTOR, "[class*='main-module-CellFirst']:first-child input")
    ACTIONS_BUTTON = (By.CSS_SELECTOR, "div[class*='js-actions-button-wrap']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "[data-test='remove']")
    REMOVE_GROUP_BUTTON = (By.CSS_SELECTOR, "[data-class-name='RemoveView']")
    CONFIRM_REMOVE_BUTTON = (By.CSS_SELECTOR, "button[class*='button_confirm-remove']")
    ID_DIV = (By.CSS_SELECTOR, "[class*='main-module-CellFirst']:first-child span")
    FIRST_SEGMENT_NAME = (By.CSS_SELECTOR, "[class*='nameCell']:first-child a")

    @staticmethod
    def find_segment(segment_id):
        return By.CSS_SELECTOR, f"[data-test *=id-{segment_id}]"
