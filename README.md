# Tipalti QA Automation Framework

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-Framework-green?logo=pytest)
![Playwright](https://img.shields.io/badge/Playwright-UI%20Testing-orange?logo=playwright)
![POM](https://img.shields.io/badge/Pattern-Page%20Object%20Model-purple)
![SOLID](https://img.shields.io/badge/Principles-SOLID-red)

A clean test automation framework built with Python, Pytest, and Playwright for the Tipalti QA assignment. The framework implements SOLID principles, Page Object Model pattern, and composition over inheritance.

## Key Features

- **SOLID Design**: Single Responsibility, Dependency Inversion, Open/Closed principles
- **Composition Over Inheritance**: Flexible design without complex class hierarchies
- **Page Object Model**: Encapsulated page logic with reusable components
- **Type Safety**: FormData model prevents runtime errors
- **Dependency Injection**: Pytest fixtures manage object creation
- **Simple Architecture**: No unnecessary abstractions
- **Dynamic Discovery**: Automatically finds all dog pages from menu

## Project Structure

```
Tipalti/
│
├── config/
│   ├── __init__.py
│   ├── config.json              # Test configuration
│   └── config_manager.py        # Configuration loader
│
├── core/
│   ├── __init__.py
│   ├── ui_driver.py             # Browser driver abstraction
│   └── ui_element.py            # Element interaction wrapper
│
├── pages/
│   ├── __init__.py
│   ├── menu_page.py             # Menu page operations
│   └── contact_page.py          # Contact form operations
│
├── models/
│   ├── __init__.py
│   └── form_data.py             # Type-safe form data model
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   └── ui/
│       ├── __init__.py
│       └── test_dogs_ui.py      # Test cases
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

### Prerequisites

- Python 3.12+
- pip
- Git

### Setup Steps

1. **Clone repository**
   ```bash
   git clone https://github.com/lior277/Tipalti.git
   cd Tipalti
   ```

2. **Create virtual environment**
   
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

4. **Install Playwright**
   ```bash
   playwright install chromium
   ```

## Running Tests

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/ui/test_dogs_ui.py -v

# Run with HTML report
pytest --html=reports/report.html --self-contained-html

# Run in headless mode (edit conftest.py first)
pytest -v
```

## Test Workflow

The automated test executes these steps:

1. Navigate to homepage
2. Open hamburger menu
3. Get all menu items → array
4. Filter dog names (exclude "Home")
5. For each dog:
   - Validate dog exists in menu array
   - Click dog menu item
   - Fill contact form with unique message
   - Submit form

**Dynamic Discovery Output:**
```
Found menu items: ['Home', 'Kika', 'Lychee', 'Kimba']
Testing dogs: ['Kika', 'Lychee', 'Kimba']
```

**Unique Messages:**
```
"I'm interested in Kika! Please tell me more about Kika."
"I'm interested in Lychee! Please tell me more about Lychee."
"I'm interested in Kimba! Please tell me more about Kimba."
```

## Configuration

Edit `config/config.json`:

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

## Architecture & Design Principles

### SOLID Principles

#### Single Responsibility Principle (SRP)

Each class has one reason to change:

```python
# UIDriver: Only browser control
class UIDriver:
    def open(self, url: str):
        self.page.goto(url)
    
    def element(self, selector: str):
        return UIElement(self.page.locator(selector))

# MenuPage: Only menu operations
class MenuPage:
    def open_menu(self):
        pass
    
    def get_menu_items(self):
        pass

# ContactPage: Only form operations
class ContactPage:
    def fill_name(self, name: str):
        pass
    
    def send_details(self):
        pass
```

#### Dependency Inversion Principle (DIP)

High-level modules depend on abstractions:

```python
# MenuPage depends on UIDriver (abstraction), not Playwright (concrete)
class MenuPage:
    def __init__(self, driver):  # ← UIDriver abstraction
        self.driver = driver
    
    def open_menu(self):
        self.driver.element(selector).click()  # ← Not Playwright directly
```

**Benefit:** Switch from Playwright to Selenium by only changing `UIDriver`.

#### Open/Closed Principle (OCP)

Open for extension, closed for modification:

```python
class UIDriver:
    def element(self, selector: str):
        return UIElement(self.page.locator(selector))
    
    # Extended without modifying element()
    def element_by_text(self, selector: str, text: str):
        return UIElement(self.page.locator(selector, has_text=text).first)
```

### Composition Over Inheritance

**Why composition?**
- Loose coupling
- Greater flexibility  
- Easier to test
- Can swap implementations

**Implementation:**

```python
# ✅ Composition: MenuPage HAS-A driver
class MenuPage:
    def __init__(self, driver):
        self.driver = driver  # Flexible, can be swapped

# ❌ Inheritance: MenuPage IS-A BasePage  
class MenuPage(BasePage):
    pass  # Tight coupling, inflexible
```

### Component Overview

**UIDriver** (`core/ui_driver.py`)
- Abstracts Playwright page object
- Implements Dependency Inversion Principle
- Methods: `open()`, `element()`, `element_by_text()`

**UIElement** (`core/ui_element.py`)
- Wraps Playwright locator
- Playwright automatically waits for elements to be ready
- Methods: `click()`, `fill()`, `text()`

**MenuPage** (`pages/menu_page.py`)
- Encapsulates menu operations
- Methods: `open_menu()`, `get_menu_items()`, `validate_menu_item_exists()`, `click_menu_item()`

**ContactPage** (`pages/contact_page.py`)
- Encapsulates form operations
- Methods: `fill_name()`, `fill_email()`, `fill_message()`, `fill_contact_details()`, `send_details()`

**FormData** (`models/form_data.py`)
- Type-safe data container
- Prevents parameter errors

**ConfigManager** (`config/config_manager.py`)
- Centralized configuration access

## Code Examples

### Test Flow

```python
def test_dog_contact_form_submission(driver, config, menu_page, contact_page):
    driver.open(config.base_url)
    
    menu_page.open_menu()
    all_items = menu_page.get_menu_items()
    dog_names = [item for item in all_items if item.lower() != "home"]
    
    for dog_name in dog_names:
        driver.open(config.base_url)
        menu_page.open_menu()
        
        menu_items = menu_page.get_menu_items()
        assert menu_page.validate_menu_item_exists(dog_name, menu_items)
        
        menu_page.click_menu_item(dog_name)
        
        unique_message = f"I'm interested in {dog_name}!"
        contact_page.fill_contact_details(
            config.contact_name, 
            config.contact_email, 
            unique_message
        )
        
        contact_page.send_details()
```

### Composition Example

```python
# Page uses composition - HAS-A driver
class MenuPage:
    def __init__(self, driver):
        self.driver = driver  # Injected dependency
        self.menu_btn_selector = "a[href='#menu']:not(.close)"
    
    def open_menu(self):
        self.driver.element(self.menu_btn_selector).click()
```

### Type-Safe Form Data

```python
# Using FormData model
form_data = FormData(
    name="John Doe",
    email="john@example.com",
    message="Hello World!"
)

contact_page.fill_form(form_data)
```

### Dependency Injection with Fixtures

```python
# conftest.py
@pytest.fixture()
def menu_page(driver):
    return MenuPage(driver)

@pytest.fixture()
def contact_page(driver):
    return ContactPage(driver)

# test_dogs_ui.py
def test_something(menu_page, contact_page):
    menu_page.open_menu()
    contact_page.send_details()
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

## Critical Pre-Deployment Tests

### Navigation
- Menu opens  
- All menu items appear  
- Each item loads correct page  

### Form
- All fields visible  
- Can type into each field  
- Submit button works  
- Error page appears

## Why This Architecture?

### Simple & Clean
- No unnecessary abstractions
- Easy to understand
- Easy to maintain

### SOLID Principles
- Single responsibility per class
- Depend on abstractions (DIP)
- Open for extension (OCP)

### Composition Over Inheritance
- Flexible and loosely coupled
- Easy to swap implementations
- No fragile base class problem

### Type Safety
- FormData prevents errors
- Clear interfaces
- IDE support

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## Repository

[https://github.com/lior277/Tipalti](https://github.com/lior277/Tipalti)

---

**Built with Python, Pytest, and Playwright following SOLID principles**