# Tipalti QA Automation Framework

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-Framework-green?logo=pytest)
![Playwright](https://img.shields.io/badge/Playwright-UI%20Testing-orange?logo=playwright)
![POM](https://img.shields.io/badge/Pattern-Page%20Object%20Model-purple)
![SOLID](https://img.shields.io/badge/Principles-SOLID-red)

A robust test automation framework built with Python, Pytest, and Playwright for the Tipalti QA assignment. The framework implements clean architecture principles with Page Object Model (POM) design pattern and SOLID principles.

## Features

- **Dynamic Test Execution**: Automatically extracts menu items and executes tests dynamically
- **Page Object Model**: Clean separation of concerns with reusable page objects
- **Configuration Management**: Centralized JSON-based configuration
- **SOLID Principles**: Maintainable and extensible code structure
- **HTTP Client**: Reusable HTTP client with retry logic for API testing
- **Comprehensive Logging**: Built-in logging utilities for debugging
- **Cross-browser Support**: Playwright-based execution across multiple browsers

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
│   ├── http_client.py           # HTTP client with retry logic
│   ├── ui_driver.py             # UI driver wrapper
│   └── ui_element.py            # UI element wrapper
│
├── pages/
│   ├── __init__.py
│   ├── base_page.py             # Base page class
│   ├── menu_page.py             # Menu page object
│   └── contact_page.py          # Contact form page object
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   └── ui/
│       ├── __init__.py
│       └── test_dogs_ui.py      # UI test cases
│
├── utilities/
│   ├── __init__.py
│   ├── helpers.py               # Helper functions
│   └── logger.py                # Logging configuration
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

### Run specific test file
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

The automated test performs the following workflow for each dog page:

1. **Navigate** to the homepage
2. **Open** the hamburger menu
3. **Extract** menu items dynamically from the DOM
4. **Validate** each menu option exists
5. **Navigate** to each dog page (Kika, Lychee, Kimba)
6. **Fill** contact form with:
   - Name (from config)
   - Email (from config)
   - Dynamic message containing the dog's name
7. **Submit** the form
8. **Verify** error page loads (expected behavior)

### Example Dynamic Message
```
This is a message for Kika!
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

### Core Components

**UIDriver** (`core/ui_driver.py`)
- Provides clean UI interaction interface
- Wraps Playwright page object
- Single Responsibility Principle (SRP)

**UIElement** (`core/ui_element.py`)
- Encapsulates element interactions
- Provides fluent API for common actions

**ConfigManager** (`config/config_manager.py`)
- Loads and provides access to test configuration
- Centralized configuration management

**HttpClient** (`core/http_client.py`)
- Reusable HTTP client with automatic retry logic
- Configurable timeouts and retry strategies
- Dependency Inversion Principle (DIP)

### Page Objects

**MenuPage** (`pages/menu_page.py`)
- Opens hamburger menu
- Retrieves menu items dynamically
- Navigates to specific menu items

**ContactPage** (`pages/contact_page.py`)
- Fills contact form fields
- Submits form
- Validates form availability

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
