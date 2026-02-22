import pytest
from core.driver_factory import create_driver
from core.config import HEADLESS


@pytest.fixture
def driver():
    driver = create_driver(headless=HEADLESS)
    yield driver
    driver.quit()