class MenuPage:
    def __init__(self, driver):
        self.driver = driver
        self.menu_btn_selector = "a[href='#menu']:not(.close)"
        self.menu_items_selector = "#menu ul li a"

    def open_menu(self):
        self.driver.element(self.menu_btn_selector).click()

    def get_menu_items(self) -> list[str]:
        items = self.driver.page.locator(self.menu_items_selector).all()
        return [item.inner_text().strip() for item in items]

    def validate_menu_item_exists(self, item_name: str, menu_items: list[str]) -> bool:
        return item_name in menu_items

    def click_menu_item(self, text: str):
        self.driver.element_by_text(self.menu_items_selector, text).click()