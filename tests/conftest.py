import pytest
from playwright.sync_api import sync_playwright, ViewportSize

from core.ui_driver import UIDriver
from config.config_manager import ConfigManager
from pages.menu_page import MenuPage


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
def driver(browser, config):
    viewport = ViewportSize(width=1920, height=1080)
    page = browser.new_page(viewport=viewport)
    driver = UIDriver(page)
    page.goto(config.base_url)

    yield driver
    page.close()


@pytest.fixture(scope="session")
def menu_items(browser, config):
    page = browser.new_page()
    page.goto(config.base_url)
    driver = UIDriver(page)
    menu = MenuPage(driver)
    menu.open_menu()
    all_items = menu.get_menu_items()
    valid = []

    for item in all_items:
        page.goto(f"{config.base_url.replace('index.html', '')}{item.lower()}.html")

        if page.locator("#name").count() > 0:
            valid.append(item)

    page.close()
    return valid