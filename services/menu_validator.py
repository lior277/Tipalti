class MenuValidator:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config

    def get_valid_menu_items(self) -> list[str]:
        self.driver.open(self.config.base_url)

        from pages.menu_page import MenuPage
        menu = MenuPage(self.driver)
        menu.open_menu()
        all_items = menu.get_menu_items()

        return [item for item in all_items if self._has_form(item)]

    def _has_form(self, menu_item: str) -> bool:
        url = self._build_url(menu_item)
        self.driver.open(url)
        return self.driver.page.locator("#name").count() > 0

    def _build_url(self, menu_item: str) -> str:
        base = self.config.base_url.replace('index.html', '')
        return f"{base}{menu_item.lower()}.html"