Tipalti QA Assignment – Automation + Manual Test Plan

Badges: Python 3.12 · Pytest · Playwright · POM · SOLID

This project implements UI automation for the Tipalti dog-site assignment using Python + Pytest + Playwright.
The framework dynamically extracts menu items, navigates to each dog page, fills the contact form, and submits it.
A full manual test plan is included at the end.

Project Structure
Tipalti/
│
├── config/
│   └── config.json
│
├── core/
│   ├── ui_driver.py
│   └── ui_element.py
│
├── pages/
│   ├── menu_page.py
│   └── contact_page.py
│
├── tests/
│   └── ui/
│       └── test_dogs_ui.py
│
└── README.md

Installation

Create virtual environment

python -m venv .venv


Activate (Windows)

.venv\Scripts\activate


Install dependencies

pip install -r requirements.txt

Running Tests
pytest -v

Automation Flow (Dog Menu UI Test)

The automation dynamically reads menu items from the DOM and executes the full workflow for each dog page.

Automation Steps

Open homepage

Click hamburger menu

Extract menu items dynamically

Validate each menu option exists

Navigate to each selected dog page

Fill contact form fields: Name, Email, Message

Insert dynamic message containing the dog name

Submit the form and verify the error page loads (expected behavior)

Dynamic Message Example:
This is a message for Kika!

Key Automation Files
test_dogs_ui.py

Loops through dynamically extracted menu items

Performs the entire workflow for each dog

Uses clean Page Object Model (POM) methods

menu_page.py

Opens hamburger menu

Reads menu items

Clicks the target menu button

contact_page.py

Fills Name, Email, Message fields

Submits the form

config.json

Stores:

base_url

contact form: name, email, message template

Manual Test Plan
Navigation Tests

1.1 Menu opens correctly

Click hamburger icon → menu expands

1.2 Menu items visible
Expected items: Home, Kika, Lychee, Kimba
Verify:

Items are clickable

No broken links

1.3 Navigation

Selecting each item loads the correct dog page

Header + dog name displayed correctly

Contact Form Tests

2.1 Valid input

Fill Name, Email, Message → Send

Expected: Redirects to error page

2.2 Empty fields

Try to submit empty form

Expected: Browser validation prevents submit

2.3 Invalid email

Enter "abc"

Expected: Email-format validation error

2.4 Long message

Paste long text

Expected: Field accepts content without layout break

UI & Layout Tests

3.1 Responsive menu

Menu should open/close correctly in desktop viewport

3.2 Page elements

Dog image loads

Title, text, and footer visible

Critical Tests (Must Run Before Deployment)
Navigation

Menu opens

All menu items visible

Each menu item loads correct dog page

Form

All fields visible

Able to type into Name, Email, Message

Submit button works

Error page appears after submission

Summary

This README includes:

Project explanation

Installation instructions

Test execution guide

Automation flow breakdown

Manual test plan

Critical deployment checks
