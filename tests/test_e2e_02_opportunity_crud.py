from pages.opportunities_page import OpportunitiesPage


def test_e2e_02_opportunity_crud(authenticated_driver, unique_suffix):
    driver = authenticated_driver

    name = f"E2E Opportunity {unique_suffix}"
    updated_name = f"{name} UPDATED"
    opp = OpportunitiesPage(driver).open()

    # CREATE
    opp.create_opportunity(name=name, amount="1000")
    assert name in driver.page_source

    # EDIT
    opp.edit_opportunity_name(updated_name)
    assert updated_name in driver.page_source

    # DELETE
    opp.delete_opportunity()
    opp.assert_opportunity_not_present(updated_name)