from selenium.common import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, \
    ElementClickInterceptedException
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

    def force_click(self, locator):
        el = self.wait_visible(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        try:
            ActionChains(self.driver).move_to_element(el).pause(0.1).click(el).perform()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", el)
        return self

    def force_click_visible(self, locator):
        els = self.driver.find_elements(*locator)
        for el in els:
            if el.is_displayed() and el.is_enabled():
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                self.driver.execute_script("arguments[0].click();", el)
                return self
        raise TimeoutException(f"No visible enabled element for locator: {locator}")

    def smart_click(self, locator):
        el = self.wait_clickable(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

        try:
            el.click()
            return self
        except (WebDriverException, StaleElementReferenceException):
            pass

        try:
            el = self.wait_clickable(locator)
            ActionChains(self.driver).move_to_element(el).pause(0.05).click(el).perform()
            return self
        except (WebDriverException, StaleElementReferenceException):
            pass

        el = self.wait_clickable(locator)
        self.driver.execute_script("arguments[0].click();", el)
        return self

    def open_dropdown(self, toggle_locator, menu_locator, retries: int = 3):
        last_exc = None
        for _ in range(retries):
            try:
                self.smart_click_visible(toggle_locator)
                self.wait.until(lambda d: any(m.is_displayed() for m in d.find_elements(*menu_locator)))
                return self
            except Exception as e:
                last_exc = e
        raise last_exc

    def smart_click_visible(self, locator, retries: int = 3):
        last_exc = None
        for _ in range(retries):
            try:
                els = self.driver.find_elements(*locator)
                for el in els:
                    try:
                        if el.is_displayed() and el.is_enabled():
                            self._scroll_to(el)
                            try:
                                el.click()
                                return self
                            except (ElementClickInterceptedException, WebDriverException):
                                try:
                                    ActionChains(self.driver).move_to_element(el).pause(0.05).click(el).perform()
                                    return self
                                except WebDriverException:
                                    self.driver.execute_script("arguments[0].click();", el)
                                    return self
                    except StaleElementReferenceException:
                        continue

                raise TimeoutException(f"No visible enabled element for locator: {locator}")

            except (StaleElementReferenceException, TimeoutException, WebDriverException) as e:
                last_exc = e

        raise last_exc

    def _scroll_to(self, el):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)