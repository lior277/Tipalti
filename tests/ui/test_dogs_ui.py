def test_dog_contact_form_submission(driver, config, menu_page, contact_page):
    driver.open(config.base_url)

    driver.open(config.base_url)

    menu_page.open_menu()
    dog_names = menu_page.get_menu_items()

    for dog_name in dog_names:
        driver.open(config.base_url)
        menu_page.open_menu()

        menu_page.click_menu_item(dog_name)

        contact_page.fill_contact_details(
            name=config.contact_name,
            email=config.contact_email,
            message=f"I'm interested in {dog_name}! Please tell me more."
        )

        contact_page.send_details()
