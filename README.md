# EspoCRM Automation Framework (Selenium + Pytest)

End-to-end test automation framework built with Python, Selenium and Pytest, following the Page Object Model (POM) design pattern.
The framework automates core CRM business flows including full CRUD operations across multiple modules.

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
│   ├── leads_page.py\
│   └── cases_page.py\
│\
├── tests/\
│   ├── test_login.py\
│   ├── test_e2e_01_account_crud.py\
│   └── test_e2e_02_opportunity_crud.py\
│   ├── test_e2e_03_lead_crud.py\
│   └── test_e2e_04_case_crud.py\
│\
├── conftest.py\
├── pytest.ini\
├── requirements.txt\
└── driver_factory.py

## Covered CRM Modules
The framework currently supports full E2E CRUD flows for:
- Accounts
- Opportunities
- Leads
- Cases

## Architecture

Each CRM entity has its own Page Object class encapsulating:
- Locators
- Business actions
- UI interaction logic
- Page-level assertions

This ensures:
- Clear separation of concerns
- High readability
- Easy scalability
- Reusable UI interaction logic

The framework includes a custom BasePage that provides:
- Centralized explicit wait handling
- Unified interaction methods
- Smart multi-layer click strategy:
- Standard click
- ActionChains click
- JavaScript click fallback
- Stable dropdown handling
- Modal interaction support

This significantly improves test stability against dynamic UI behavior.


## How to Run Tests

```bash
pip install -r requirements.txt
pytest -v
```
Optional:
```bash
pytest -v -s
```

## Key Automation Concepts Demonstrated
- Page Object Model design
- Handling dynamic UI elements (dropdowns, modals)
- Date picker automation
- Required field validation handling
- CRUD business flow testing
- Clean test structure with fixtures


## Current Framework Maturity
- Multiple CRM modules automated
- Stable click handling strategy
- Clean Page Object separation
- Reusable BasePage logic
- Extensible structure for future modules


## Future Improvements
- Extract common CRUD behavior into BaseCrudPage
- Add negative test scenarios (validation coverage)
- Add CI integration (GitHub Actions)
- Add API tests
- Add API layer tests
- Introduce test markers (smoke / regression)
- Improve logging & error reporting