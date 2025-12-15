def test_dog_contact_form_submission(
    driver,
    menu_page,
    contact_page,
    contact_data,
    config
):
    menu_page.open_menu()
    dog_names = menu_page.get_menu_items()

    for dog_name in dog_names:
        driver.open(config.base_url)

        menu_page.open_menu()
        menu_page.click_menu_item(dog_name)

        contact_page.fill_contact_details(
            name=contact_data["name"],
            email=contact_data["email"],
            message=f"I'm interested in {dog_name}! Please tell me more."
        )

        old_url = driver.page.url
        contact_page.submit()
        driver.page.wait_for_load_state("load")

        # Assert submit caused navigation
        assert driver.page.url != old_url
