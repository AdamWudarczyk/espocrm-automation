from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from core.config import APP_URL

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open_hash(self, hash_path: str):
        self.driver.get(f"{APP_URL}#{hash_path}")
        self.wait.until(lambda d: f"#{hash_path}".lower() in d.current_url.lower())
        return self

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        self.wait_clickable(locator).click()
        return self

    def type(self, locator, text: str, clear: bool = True):
        el = self.wait_visible(locator)
        el.click()
        if clear:
            el.send_keys(Keys.CONTROL, "a")
            el.send_keys(Keys.BACKSPACE)
        el.send_keys(text)
        return self