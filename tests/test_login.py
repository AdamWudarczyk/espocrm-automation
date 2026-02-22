from pages.login_page import LoginPage


def test_login_success(driver):
    login = LoginPage(driver).open()
    assert login.is_loaded()

    login.login_as("Administrator")

    assert "login" not in driver.current_url.lower()