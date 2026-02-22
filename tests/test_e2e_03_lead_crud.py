from pages.leads_page import LeadsPage

def test_e2e_03_lead_crud(authenticated_driver, unique_suffix):
    driver = authenticated_driver

    first_name = "E2E"
    last_name = f"Lead {unique_suffix}"
    updated_last_name = f"{last_name} UPDATED"

    leads = LeadsPage(driver).open()

    # CREATE
    leads.create_lead(
        first_name=first_name,
        last_name=last_name,
    )
    assert last_name.lower() in driver.page_source.lower()

    # EDIT
    leads.edit_lead_last_name(updated_last_name)
    assert updated_last_name.lower() in driver.page_source.lower()

    # DELETE
    leads.delete_lead()
    leads.assert_lead_not_present(updated_last_name)