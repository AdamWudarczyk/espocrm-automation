# EspoCRM Automation Framework (Selenium + Pytest)

End-to-end automation framework built with Python, Selenium and Pytest, based on the Page Object Model (POM) pattern.The framework automates core CRM business flows such as Account and Opportunity lifecycle (CRUD operations).

## Tech Stack
- Python 3.x
- Selenium WebDriver
- Pytest
- Page Object Model (POM)
- Explicit waits (WebDriverWait)
- Custom BasePage abstraction

## Project Structure
├── core/\
│   └── config.py\
│\
├── pages/\
│   ├── base_page.py\
│   ├── login_page.py\
│   ├── accounts_page.py\
│   └── opportunities_page.py\
│\
├── tests/\
│   ├── test_login.py\
│   ├── test_open_app.py\
│   ├── test_e2e_01_account_crud.py\
│   └── test_e2e_02_opportunity_crud.py\
│\
├── conftest.py\
├── pytest.ini\
└── driver_factory.py

## Project Structure
Each CRM entity has its own Page Object:
- AccountsPage
- OpportunitiesPage

Each page encapsulates:
- Locators
- Business actions
- UI interaction logic
- Assertions related to the page

## How to Run Tests

```bash
pip install -r requirements.txt
pytest -v
```

## Key Automation Concepts Demonstrated
- Page Object Model design
- Handling dynamic UI elements (dropdowns, modals)
- Date picker automation
- Required field validation handling
- CRUD business flow testing
- Clean test structure with fixtures

## Future Improvements
- Add Contact, Lead CRUD
- Extract common CRUD behavior into BaseCrudPage
- Add reporting (Allure)
- Add CI integration (GitHub Actions)
- Add API tests