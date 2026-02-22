from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from datetime import date

class OpportunitiesPage(BasePage):

    CREATE_BUTTONS = [
        (By.CSS_SELECTOR, '[data-action="create"]'),
        (By.CSS_SELECTOR, 'a[href*="#Opportunity/create"], a[data-name="create"]'),
        (By.XPATH, '//a[contains(normalize-space(.), "Create Opportunity")]'),
        (By.XPATH, '//button[contains(normalize-space(.), "Create Opportunity")]'),
    ]

    NAME_INPUT = (By.CSS_SELECTOR, 'input[data-name="name"], input[name="name"]')
    AMOUNT_INPUT = (By.CSS_SELECTOR, 'input[data-name="amount"], input[name="amount"]')
    SAVE_BUTTON = (
        By.CSS_SELECTOR,
        'button[data-action="save"][data-name="save"], [data-action="save"], [data-name="save"]'
    )
    EDIT_BUTTONS = [
        (By.CSS_SELECTOR, '[data-action="edit"]'),
        (By.CSS_SELECTOR, '[data-name="edit"]'),
        (By.XPATH, '//a[normalize-space(.)="Edit"] | //button[normalize-space(.)="Edit"]'),
    ]
    MORE_TOGGLE = (
        By.XPATH,
        '//div[starts-with(@id,"opportunity-detail-")]//button[contains(@class,"dropdown-toggle")][1]'
    )
    REMOVE_ACTION = (By.CSS_SELECTOR, 'a[data-action="delete"]')
    MODAL_DIALOG = (By.CSS_SELECTOR, ".modal-dialog")
    MODAL_REMOVE_BTN = (By.CSS_SELECTOR, ".modal-dialog button.btn-danger")
    LIST_CONTAINER = (By.CSS_SELECTOR, ".list-container, .record-list, .page-content")
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Search"], input.global-search-input, input[type="search"]')
    CLOSE_DATE_INPUT = (By.CSS_SELECTOR, 'input[data-name="closeDate"], input[name="closeDate"]')


    def open(self):
        return self.open_hash("Opportunity")

    def click_first_available(self, locators):
        last_error = None
        for loc in locators:
            try:
                self.click(loc)
                return self
            except Exception as e:
                last_error = e
        raise last_error

    def create_opportunity(
            self,
            name: str,
            amount: str | None = None,
            stage: str | None = None,
            close_date: str | None = None
    ):
        self.click_first_available(self.CREATE_BUTTONS)
        self.wait.until(lambda d: "create" in d.current_url.lower())

        self.type(self.NAME_INPUT, name)

        if amount is not None:
            self.type(self.AMOUNT_INPUT, amount)

        if close_date is None:
            close_date = date.today().strftime("%Y-%m-%d")

        self.set_close_date(close_date)

        self.click(self.SAVE_BUTTON)
        self.wait.until(lambda d: "create" not in d.current_url.lower())
        self.wait.until(lambda d: name.lower() in d.page_source.lower())
        return self

    def edit_opportunity_name(self, new_name: str):
        self.click_first_available(self.EDIT_BUTTONS)

        el = self.wait_visible(self.NAME_INPUT)
        el.click()
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(new_name)

        self.click(self.SAVE_BUTTON)
        self.wait.until(lambda d: new_name.lower() in d.page_source.lower())
        return self

    def delete_opportunity(self):
        import time

        time.sleep(2)

        btn = self.wait_visible(self.MORE_TOGGLE)
        self.driver.execute_script("arguments[0].click();", btn)

        time.sleep(1)

        remove = self.wait_clickable(self.REMOVE_ACTION)
        self.driver.execute_script("arguments[0].click();", remove)

        self.wait.until(EC.visibility_of_element_located(self.MODAL_DIALOG))
        confirm = self.wait.until(EC.element_to_be_clickable(self.MODAL_REMOVE_BTN))
        self.driver.execute_script("arguments[0].click();", confirm)

        self.wait.until(EC.invisibility_of_element_located(self.MODAL_DIALOG))
        self.wait.until(lambda d: "/view/" not in d.current_url.lower())
        return self

    def assert_opportunity_not_present(self, name: str):
        self.open_hash("Opportunity")
        self.wait_visible(self.LIST_CONTAINER)

        search = self.wait_visible(self.SEARCH_INPUT)
        search.click()
        search.send_keys(Keys.CONTROL, "a")
        search.send_keys(Keys.BACKSPACE)
        search.send_keys(name)
        search.send_keys(Keys.ENTER)

        self.wait.until(lambda d: True)
        assert name.lower() not in self.driver.page_source.lower()
        return self

    def set_close_date(self, date_str: str):
        el = self.wait_visible(self.CLOSE_DATE_INPUT)
        el.click()
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(date_str)
        el.send_keys(Keys.TAB)
        return self