from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from core.config import BASE_URL
from pages.base_page import BasePage

class LoginPage(BasePage):
    USER_SELECT = (By.NAME, "username")
    LOGIN_BUTTON = (By.ID, "btn-login")

    def open(self):
        self.driver.get(BASE_URL)
        return self

    def login_as(self, username: str):
        select_element = self.wait.until(
            EC.presence_of_element_located(self.USER_SELECT)
        )
        select = Select(select_element)
        select.select_by_visible_text(username)

        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        return self

    def is_loaded(self) -> bool:
        return len(self.driver.find_elements(*self.LOGIN_BUTTON)) > 0