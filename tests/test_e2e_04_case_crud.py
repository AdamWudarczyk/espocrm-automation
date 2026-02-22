from pages.cases_page import CasesPage


def test_e2e_04_case_crud(authenticated_driver, unique_suffix):
    driver = authenticated_driver

    name = f"E2E Case {unique_suffix}"
    updated_name = f"{name} UPDATED"

    cases = CasesPage(driver).open()

    # CREATE
    cases.create_case(name)
    assert name.lower() in driver.page_source.lower()

    # EDIT
    cases.edit_case_name(updated_name)
    assert updated_name.lower() in driver.page_source.lower()

    # DELETE
    cases.delete_case()
    cases.assert_case_not_present(updated_name)