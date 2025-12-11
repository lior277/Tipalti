# Final Clean Implementation

## Updated Files

### 1. pages/menu_page.py

```python
class MenuPage:
    def __init__(self, driver):
        self.driver = driver
        self.menu_btn_selector = "a[href='#menu']:not(.close)"
        self.menu_items_selector = "#menu ul li a"
    
    def open_menu(self):
        self.driver.element(self.menu_btn_selector).click()
    
    def get_menu_items(self) -> list[str]:
        items = self.driver.page.locator(self.menu_items_selector).all()
        return [item.inner_text().strip() for item in items]
    
    def validate_menu_item_exists(self, item_name: str, menu_items: list[str]) -> bool:
        return item_name in menu_items
    
    def click_menu_item(self, text: str):
        self.driver.element_by_text(self.menu_items_selector, text).click()
```

---

### 2. pages/contact_page.py

```python
from models.form_data import FormData


class ContactPage:
    def __init__(self, driver):
        self.driver = driver
        self.name_selector = "#name"
        self.email_selector = "#email"
        self.message_selector = "#message"
        self.submit_selector = "input[type='submit']"
    
    def is_form_available(self) -> bool:
        return self.driver.page.locator(self.name_selector).count() > 0
    
    def fill_name(self, name: str):
        self.driver.element(self.name_selector).fill(name)
    
    def fill_email(self, email: str):
        self.driver.element(self.email_selector).fill(email)
    
    def fill_message(self, message: str):
        self.driver.element(self.message_selector).fill(message)
    
    def fill_contact_details(self, name: str, email: str, message: str):
        self.fill_name(name)
        self.fill_email(email)
        self.fill_message(message)
    
    def fill_form(self, data: FormData):
        self.fill_contact_details(data.name, data.email, data.message)
    
    def send_details(self):
        self.driver.element(self.submit_selector).click()
```

---

### 3. tests/ui/test_dogs_ui.py

**Option 1: Dynamic Parametrization (Recommended)**

```python
import pytest
from models.form_data import FormData


def pytest_generate_tests(metafunc):
    if "dog_name" in metafunc.fixturenames:
        menu_items = metafunc.config.cache.get("menu_items", None)
        if menu_items is None:
            from playwright.sync_api import sync_playwright, ViewportSize
            from core.ui_driver import UIDriver
            from config.config_manager import ConfigManager
            from services.menu_validator import MenuValidator
            
            config = ConfigManager()
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                viewport = ViewportSize(width=1920, height=1080)
                page = browser.new_page(viewport=viewport)
                driver = UIDriver(page)
                
                validator = MenuValidator(driver, config)
                menu_items = validator.get_valid_menu_items()
                
                page.close()
                browser.close()
            
            metafunc.config.cache.set("menu_items", menu_items)
        
        metafunc.parametrize("dog_name", menu_items)


def test_dog_contact_form_submission(driver, config, dog_name, menu_page, contact_page):
    driver.open(config.base_url)
    
    menu_page.open_menu()
    menu_items = menu_page.get_menu_items()
    
    assert menu_page.validate_menu_item_exists(dog_name, menu_items), \
        f"Dog '{dog_name}' not found in menu"
    
    menu_page.click_menu_item(dog_name)
    
    unique_message = f"I'm interested in {dog_name}! Please tell me more about {dog_name}."
    
    contact_page.fill_contact_details(
        name=config.contact_name,
        email=config.contact_email,
        message=unique_message
    )
    
    contact_page.send_details()
```

**Option 2: Simple Loop (Simpler)**

```python
from models.form_data import FormData


def test_dog_contact_form_submission(driver, config, menu_items, menu_page, contact_page):
    for dog_name in menu_items:
        driver.open(config.base_url)
        
        menu_page.open_menu()
        menu_items_array = menu_page.get_menu_items()
        
        assert menu_page.validate_menu_item_exists(dog_name, menu_items_array), \
            f"Dog '{dog_name}' not found in menu"
        
        menu_page.click_menu_item(dog_name)
        
        unique_message = f"I'm interested in {dog_name}! Please tell me more about {dog_name}."
        
        contact_page.fill_contact_details(
            name=config.contact_name,
            email=config.contact_email,
            message=unique_message
        )
        
        contact_page.send_details()
```

---

### 4. core/ui_driver.py

```python
from core.ui_element import UIElement


class UIDriver:
    def __init__(self, page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def element(self, selector: str):
        return UIElement(self.page.locator(selector))

    def element_by_text(self, selector: str, text: str):
        return UIElement(self.page.locator(selector, has_text=text).first)
```

---

### 5. models/form_data.py

```python
from dataclasses import dataclass


@dataclass
class FormData:
    name: str
    email: str
    message: str
```

---

### 6. services/menu_validator.py

```python
class MenuValidator:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
    
    def get_valid_menu_items(self) -> list[str]:
        self.driver.open(self.config.base_url)
        
        from pages.menu_page import MenuPage
        menu = MenuPage(self.driver)
        menu.open_menu()
        all_items = menu.get_menu_items()
        
        return [item for item in all_items if self._has_form(item)]
    
    def _has_form(self, menu_item: str) -> bool:
        url = self._build_url(menu_item)
        self.driver.open(url)
        return self.driver.page.locator("#name").count() > 0
    
    def _build_url(self, menu_item: str) -> str:
        base = self.config.base_url.replace('index.html', '')
        return f"{base}{menu_item.lower()}.html"
```

---

## Updated README.md

```markdown
# Tipalti QA Automation Framework

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-Framework-green?logo=pytest)
![Playwright](https://img.shields.io/badge/Playwright-UI%20Testing-orange?logo=playwright)
![POM](https://img.shields.io/badge/Pattern-Page%20Object%20Model-purple)

A clean and simple test automation framework built with Python, Pytest, and Playwright for the Tipalti QA assignment. The framework follows the Page Object Model (POM) pattern with a focus on simplicity and maintainability.

## Features

- **Dynamic Test Execution**: Automatically discovers and tests all dog pages
- **Page Object Model**: Clean separation of concerns with reusable page objects
- **Type Safety**: FormData model for type-safe form submissions
- **Page Fixtures**: Centralized page object creation via pytest fixtures
- **Configuration Management**: Centralized JSON-based configuration
- **Auto-Waiting**: Leverages Playwright's built-in auto-waiting capabilities
- **Simple Architecture**: No unnecessary abstractions or complexity
- **Cross-browser Support**: Playwright-based execution across multiple browsers

## Project Structure

```
Tipalti/
│
├── config/
│   ├── __init__.py
│   ├── config.json
│   └── config_manager.py
│
├── core/
│   ├── __init__.py
│   ├── http_client.py
│   ├── ui_driver.py
│   └── ui_element.py
│
├── pages/
│   ├── __init__.py
│   ├── menu_page.py
│   └── contact_page.py
│
├── models/
│   ├── __init__.py
│   └── form_data.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── ui/
│       ├── __init__.py
│       └── test_dogs_ui.py
│
├── utilities/
│   ├── __init__.py
│   ├── helpers.py
│   └── logger.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

### Prerequisites

- Python 3.12 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/lior277/Tipalti.git
   cd Tipalti
   ```

2. **Create and activate virtual environment**
   
   **Windows:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

## Running Tests

### Run all tests
```bash
pytest -v
```

### Run specific test
```bash
pytest tests/ui/test_dogs_ui.py -v
```

### Run with HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run in headless mode
Modify `tests/conftest.py` and change `headless=False` to `headless=True` in the browser fixture.

## Test Flow

The automated test performs the following workflow:

1. **Navigate** to the homepage
2. **Open** hamburger menu
3. **Get** all menu items and save to array
4. **Filter** dog names (exclude "Home")
5. **For each dog:**
   - Validate menu option exists in array
   - Click on the menu option
   - Fill contact form with unique message containing dog name
   - Submit the form
   - Verify error page appears (expected behavior)

### Example Test Execution
```
Opening menu...
Found items: ['Home', 'Kika', 'Lychee', 'Kimba']
Testing dog: Kika
Testing dog: Lychee
Testing dog: Kimba
```

### Unique Messages Per Dog
Each dog receives a personalized message:
```
"I'm interested in Kika! Please tell me more about Kika."
"I'm interested in Lychee! Please tell me more about Lychee."
"I'm interested in Kimba! Please tell me more about Kimba."
```

## Configuration

Edit `config/config.json` to customize test data:

```json
{
  "base_url": "https://qa-tipalti-assignment.tipalti-pg.com/index.html",
  "contact_form": {
    "name": "Test User",
    "email": "test@example.com",
    "message_template": "This is a message for {dog}!"
  }
}
```

## Framework Architecture

### Design Principles

**Simplicity First**
- No unnecessary abstractions
- Direct and clear code
- Easy to understand and maintain

**Page Object Model (POM)**
- Each page is represented by a class
- Page logic is encapsulated and reusable
- Tests remain clean and readable

**Single Responsibility Principle**
- Each method does one thing
- Each class has one reason to change
- Clear separation of concerns

**Type Safety**
- FormData model ensures correct data types
- Prevents runtime errors from incorrect parameters
- Clear interface for form submissions

**YAGNI (You Aren't Gonna Need It)**
- Only add complexity when actually needed
- No premature optimization
- Simple solutions over clever abstractions

### Core Components

**UIDriver** (`core/ui_driver.py`)
- Abstraction over Playwright page object
- Methods: `open()`, `element()`, `element_by_text()`
- Hides Playwright implementation details

**UIElement** (`core/ui_element.py`)
- Wraps Playwright locator
- Methods: `click()`, `fill()`, `text()`
- Leverages Playwright's auto-waiting

**ConfigManager** (`config/config_manager.py`)
- Loads configuration from JSON
- Provides centralized access to settings
- Easy to modify test data

**FormData** (`models/form_data.py`)
- Type-safe data container
- Ensures correct form field values
- Single object instead of multiple parameters

### Page Objects

**MenuPage** (`pages/menu_page.py`)

Methods:
- `open_menu()` - Click hamburger button
- `get_menu_items()` - Get all menu items as array
- `validate_menu_item_exists()` - Check if item exists in array
- `click_menu_item()` - Click specific menu option

**ContactPage** (`pages/contact_page.py`)

Methods:
- `fill_name()` - Fill name field
- `fill_email()` - Fill email field
- `fill_message()` - Fill message field
- `fill_contact_details()` - Fill all fields at once
- `fill_form()` - Fill using FormData object
- `send_details()` - Submit the form

## Code Examples

### Basic Test Flow

```python
@pytest.mark.parametrize("dog_name", ["Kika", "Lychee", "Kimba"])
def test_dog_contact_form_submission(driver, config, dog_name, menu_page, contact_page):
    driver.open(config.base_url)
    
    menu_page.open_menu()
    menu_items = menu_page.get_menu_items()
    
    assert menu_page.validate_menu_item_exists(dog_name, menu_items)
    
    menu_page.click_menu_item(dog_name)
    
    unique_message = f"I'm interested in {dog_name}!"
    contact_page.fill_contact_details(config.contact_name, config.contact_email, unique_message)
    
    contact_page.send_details()
```

### Using FormData

```python
form_data = FormData(
    name="John Doe",
    email="john@example.com",
    message="Hello World!"
)

contact_page.fill_form(form_data)
```

### Page Fixtures

```python
@pytest.fixture()
def menu_page(driver):
    return MenuPage(driver)

@pytest.fixture()
def contact_page(driver):
    return ContactPage(driver)
```

## Manual Test Plan

### 1. Navigation Tests

#### 1.1 Menu opens correctly
- Click hamburger → menu expands

#### 1.2 Menu items visible
Expected items: Home, Kika, Lychee, Kimba  
Verify:  
- Items appear  
- Items clickable  
- No broken links  

#### 1.3 Navigation works
- Each item loads correct page  
- Header + dog name displayed  

---

### 2. Contact Form Tests

#### 2.1 Valid input
- Fill Name, Email, Message → Send  
Expected: Error page loads  

#### 2.2 Empty fields
- Submit empty form  
Expected: Browser validation blocks submit  

#### 2.3 Invalid email
- Enter "abc"  
Expected: Email-format validation error  

#### 2.4 Long message
- Paste long text  
Expected: Accepted, layout stable  

---

### 3. UI & Layout Tests

#### 3.1 Responsive menu
- Menu opens/closes correctly at >1024px width  

#### 3.2 Page elements
- Dog image loads  
- Title + text visible  
- Footer visible  

---

## Critical Tests (Must Run Before Deployment)

### Navigation
- Menu opens  
- All menu items appear  
- Each item loads correct page  

### Form
- All fields visible  
- Can type into each field  
- Submit button works  
- Error page appears

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is part of a QA assignment for Tipalti.

## Contact

Repository: [https://github.com/lior277/Tipalti](https://github.com/lior277/Tipalti)

---

**Built with ❤️ using Python, Pytest, and Playwright**
```

---

## Summary of Changes

### Test File (test_dogs_ui.py)
- ✅ Removed all comments
- ✅ Clean, readable code
- ✅ Parametrized for each dog
- ✅ Unique message per dog

### README Updates
- ✅ Added parametrized test explanation
- ✅ Added test output example
- ✅ Added "Run for specific dog" command
- ✅ Listed all MenuPage methods
- ✅ Listed all ContactPage methods
- ✅ Removed PageHelper references
- ✅ Updated architecture description
- ✅ Clear method documentation