from core.config import BASE_URL

def test_open_espocrm_homepage(driver):
    driver.get(BASE_URL)

    assert "EspoCRM" in driver.title