import pytest
from models.form_data import FormData


def test_dog_menu_flow(driver, config, menu_items, menu_page, contact_page):
    for dog in menu_items:
        driver.open(config.base_url)

        menu_page.open_menu()

        assert dog in menu_items, f"{dog} not found in menu"

        menu_page.click_menu_item(dog)

        form_data = FormData(
            name=config.contact_name,
            email=config.contact_email,
            message=config.contact_message_template.format(dog=dog)
        )

        contact_page.fill_form(form_data)
        contact_page.send()