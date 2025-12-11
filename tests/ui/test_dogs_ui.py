from models.form_data import FormData


def test_dog_contact_form_submission(driver, config, menu_page, contact_page):
    driver.open(config.base_url)

    menu_page.open_menu()
    all_menu_items = menu_page.get_menu_items()

    dog_names = [item for item in all_menu_items if item.lower() != "home"]

    for dog_name in dog_names:
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