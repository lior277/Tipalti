import pytest
from playwright.sync_api import sync_playwright, ViewportSize

from core.ui_driver import UIDriver
from config.config_manager import ConfigManager
from pages.menu_page import MenuPage
from pages.contact_page import ContactPage


@pytest.fixture(scope="session")
def config():
    return ConfigManager()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture()
def driver(browser):
    viewport = ViewportSize(width=1920, height=1080)
    page = browser.new_page(viewport=viewport)
    driver = UIDriver(page)

    yield driver
    page.close()


@pytest.fixture()
def menu_page(driver):
    return MenuPage(driver)


@pytest.fixture()
def contact_page(driver):
    return ContactPage(driver)