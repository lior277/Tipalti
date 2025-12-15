class MenuPage:
    def __init__(self, driver):
        self.driver = driver
        self.menu_button = driver.by_css("a[href='#menu']:not(.close)")
        self.menu_items_selector = "#menu ul li a"

    def open_menu(self) -> None:
        self.menu_button.click()

    def get_menu_items(self) -> list[str]:
        return [
            text.strip()
            for text in self.driver.page
                .locator(self.menu_items_selector)
                .all_inner_texts()
            if text.strip() and text.strip().lower() != "home"
        ]

    def click_menu_item(self, name: str) -> None:
        self.driver.by_css_text(
            self.menu_items_selector,
            name
        ).click()
