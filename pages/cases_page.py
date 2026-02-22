from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CasesPage(BasePage):
    CREATE_BUTTONS = [
        (By.CSS_SELECTOR, '[data-action="create"]'),
        (By.CSS_SELECTOR, 'a[href*="#Case/create"], a[data-name="create"]'),
        (By.XPATH, '//a[contains(normalize-space(.), "Create Case")]'),
        (By.XPATH, '//button[contains(normalize-space(.), "Create Case")]'),
    ]
    NAME_INPUT = (
        By.CSS_SELECTOR,
        'input[data-name="name"], input[name="name"], '
        'input[data-name="subject"], input[name="subject"]'
    )

    SAVE_BUTTON = (By.CSS_SELECTOR, 'button[data-action="save"], button[data-name="save"], a[data-name="save"]')
    EDIT_BUTTON = (By.CSS_SELECTOR, 'button[data-action="edit"], button[data-name="edit"], a[data-action="edit"], a[data-name="edit"]')
    MORE_TOGGLE = (
        By.XPATH,
        '//div[starts-with(@id,"case-detail-")]'
        '//div[contains(@class,"actions-btn-group")]'
        '//button[contains(@class,"dropdown-toggle")]'
    )
    REMOVE_ACTION = (
        By.XPATH,
        '//a[normalize-space(.)="Remove" or normalize-space(.)="Delete" '
        'or @data-action="delete" or @data-action="remove" '
        'or @data-name="delete" or @data-name="remove"]'
    )

    MODAL_DIALOG = (By.CSS_SELECTOR, ".modal-dialog")
    MODAL_REMOVE_BTN = (By.CSS_SELECTOR, ".modal-dialog button.btn-danger")

    LIST_CONTAINER = (By.CSS_SELECTOR, ".list-container, .record-list, .page-content")
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Search"], input.global-search-input, input[type="search"]')

    def open(self):
        return self.open_hash("Case")

    def click_first_available(self, locators):
        last_error = None
        for loc in locators:
            try:
                self.force_click_visible(loc)
                return self
            except Exception as e:
                last_error = e
        raise last_error

    def create_case(self, name: str):
        self.click_first_available(self.CREATE_BUTTONS)
        self.wait.until(lambda d: "create" in d.current_url.lower())

        self.type(self.NAME_INPUT, name)
        self.force_click_visible(self.SAVE_BUTTON)

        self.wait.until(lambda d: "create" not in d.current_url.lower())
        self.wait.until(lambda d: name.lower() in d.page_source.lower())
        return self

    def edit_case_name(self, new_name: str):
        self.force_click_visible(self.EDIT_BUTTON)

        el = self.wait_visible(self.NAME_INPUT)
        el.click()
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(new_name)

        self.force_click_visible(self.SAVE_BUTTON)
        self.wait.until(lambda d: new_name.lower() in d.page_source.lower())
        return self

    def delete_case(self):
        self.force_click(self.MORE_TOGGLE)
        clicked = False
        candidates = self.driver.find_elements(*self.REMOVE_ACTION)
        for el in candidates:
            try:
                if el.is_displayed() and el.is_enabled():
                    self.driver.execute_script("arguments[0].click();", el)
                    clicked = True
                    break
            except Exception:
                continue

        if not clicked:
            raise TimeoutException("Remove/Delete action not visible after opening Cases actions dropdown")

        self.wait.until(EC.visibility_of_element_located(self.MODAL_DIALOG))
        self.force_click(self.MODAL_REMOVE_BTN)

        self.wait.until(EC.invisibility_of_element_located(self.MODAL_DIALOG))
        self.wait.until(lambda d: "/view/" not in d.current_url.lower())
        return self

    def assert_case_not_present(self, name: str):
        self.open_hash("Case")
        self.wait_visible(self.LIST_CONTAINER)

        search = self.wait_visible(self.SEARCH_INPUT)
        search.click()
        search.send_keys(Keys.CONTROL, "a")
        search.send_keys(Keys.BACKSPACE)
        search.send_keys(name)
        search.send_keys(Keys.ENTER)

        assert name.lower() not in self.driver.page_source.lower()
        return self