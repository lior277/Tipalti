import pytest
from pages.menu_page import MenuPage
from pages.contact_page import ContactPage


def test_dog_menu_flow(driver, config, menu_items):
    for dog in menu_items:
        driver.open(config.base_url)

        menu = MenuPage(driver)
        menu.open_menu()

        assert dog in menu_items, f"{dog} not found in menu"

        menu.click_menu_item(dog)

        contact = ContactPage(driver)
        contact.fill_form(
            name=config.contact_name,
            email=config.contact_email,
            message=config.contact_message_template.format(dog=dog)
        )

        contact.send()
