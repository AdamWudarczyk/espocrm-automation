import pytest
from core.driver_factory import create_driver
from core.config import HEADLESS
from pages.login_page import LoginPage
from datetime import datetime

@pytest.fixture
def driver():
    driver = create_driver(headless=HEADLESS)
    yield driver
    driver.quit()

@pytest.fixture
def authenticated_driver(driver):
    LoginPage(driver).open().login_as("Administrator")
    return driver

@pytest.fixture
def unique_suffix():
    return datetime.now().strftime("%Y%m%d%H%M%S")