from pages.accounts_page import AccountsPage

def test_e2e_01_account_crud(authenticated_driver, unique_suffix):
    driver = authenticated_driver

    name = f"E2E Account {unique_suffix}"
    updated_name = f"{name} UPDATED"
    accounts = AccountsPage(driver).open()

    # CREATE
    accounts.create_account(name)
    assert name in driver.page_source

    # EDIT
    accounts.edit_account_name(updated_name)
    assert updated_name in driver.page_source

    # DELETE
    accounts.delete_account()
    accounts.assert_account_not_present(updated_name)