from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class LeadsPage(BasePage):
    CREATE_BUTTON = (By.CSS_SELECTOR, '[data-action="create"]')
    EDIT_BUTTON = (By.CSS_SELECTOR, '[data-action="edit"], [data-name="edit"]')

    FIRST_NAME_INPUT = (By.CSS_SELECTOR, 'input[data-name="firstName"], input[name="firstName"]')
    LAST_NAME_INPUT = (By.CSS_SELECTOR, 'input[data-name="lastName"], input[name="lastName"]')

    STATUS_SELECT = (By.CSS_SELECTOR, 'select[data-name="status"], select[name="status"]')
    STATUS_INPUT_FALLBACK = (By.CSS_SELECTOR, '[data-name="status"] input[type="text"], [data-name="status"] input')

    SOURCE_SELECT = (By.CSS_SELECTOR, 'select[data-name="source"], select[name="source"]')
    SOURCE_INPUT_FALLBACK = (By.CSS_SELECTOR, '[data-name="source"] input[type="text"], [data-name="source"] input')
    SAVE_BUTTON = (By.CSS_SELECTOR, 'button[data-action="save"], button[data-name="save"], a[data-name="save"]')

    MORE_TOGGLE = (By.XPATH, '//div[starts-with(@id,"lead-detail-")]//button[contains(@class,"dropdown-toggle")][1]')
    REMOVE_ACTION = (By.CSS_SELECTOR, 'a[data-action="delete"]')

    MODAL_DIALOG = (By.CSS_SELECTOR, ".modal-dialog")
    MODAL_REMOVE_BTN = (By.CSS_SELECTOR, ".modal-dialog button.btn-danger")

    LIST_CONTAINER = (By.CSS_SELECTOR, ".list-container, .record-list, .page-content")
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Search"], input.global-search-input, input[type="search"]')

    def open(self):
        return self.open_hash("Lead")

    def _set_dropdown_if_present(self, select_locator, input_fallback_locator, value: str):
        selects = self.driver.find_elements(*select_locator)
        if selects:
            el = selects[0]
            el.click()
            el.send_keys(value)
            return self

        inputs = self.driver.find_elements(*input_fallback_locator)
        if inputs:
            el = inputs[0]
            el.click()
            el.send_keys(Keys.CONTROL, "a")
            el.send_keys(Keys.BACKSPACE)
            el.send_keys(value)
            el.send_keys(Keys.ENTER)
            return self

        return self

    def save(self):
        try:
            self.driver.switch_to.active_element.send_keys(Keys.TAB)
        except Exception:
            pass

        self.force_click_visible(self.SAVE_BUTTON)
        self.wait.until(lambda d: "create" not in d.current_url.lower())

        try:
            self.wait.until(EC.invisibility_of_element_located(self.MODAL_DIALOG))
        except Exception:
            pass

        return self

    def create_lead(
        self,
        first_name: str,
        last_name: str,
        status: str | None = None,
        source: str | None = None,
    ):
        self.click(self.CREATE_BUTTON)
        self.wait.until(lambda d: "create" in d.current_url.lower())

        self.type(self.FIRST_NAME_INPUT, first_name)
        self.type(self.LAST_NAME_INPUT, last_name)

        if status:
            self._set_dropdown_if_present(self.STATUS_SELECT, self.STATUS_INPUT_FALLBACK, status)

        if source:
            self._set_dropdown_if_present(self.SOURCE_SELECT, self.SOURCE_INPUT_FALLBACK, source)

        self.save()
        self.wait.until(lambda d: last_name.lower() in d.page_source.lower())
        return self

    def edit_lead_last_name(self, new_last_name: str):
        self.click(self.EDIT_BUTTON)

        el = self.wait_visible(self.LAST_NAME_INPUT)
        el.click()
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(new_last_name)

        self.save()
        self.wait.until(lambda d: new_last_name.lower() in d.page_source.lower())
        return self

    def delete_lead(self):
        self.force_click(self.MORE_TOGGLE)
        self.force_click(self.REMOVE_ACTION)

        self.wait.until(EC.visibility_of_element_located(self.MODAL_DIALOG))
        self.force_click(self.MODAL_REMOVE_BTN)

        self.wait.until(EC.invisibility_of_element_located(self.MODAL_DIALOG))
        self.wait.until(lambda d: "/view/" not in d.current_url.lower())
        return self

    def assert_lead_not_present(self, name_fragment: str):
        self.open_hash("Lead")
        self.wait_visible(self.LIST_CONTAINER)

        search = self.wait_visible(self.SEARCH_INPUT)
        search.click()
        search.send_keys(Keys.CONTROL, "a")
        search.send_keys(Keys.BACKSPACE)
        search.send_keys(name_fragment)
        search.send_keys(Keys.ENTER)

        self.wait.until(lambda d: True)

        assert name_fragment.lower() not in self.driver.page_source.lower()
        return self