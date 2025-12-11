from core.ui_element import UIElement

class MenuPage:
    def __init__(self, driver):
        self.driver = driver
        self.menu_btn = driver.element("a[href='#menu']:not(.close)")
        self.menu_items_locator = driver.page.locator("#menu ul li a")

    def open_menu(self):
        self.menu_btn.click()

    def get_menu_items(self) -> list[str]:
        items = self.menu_items_locator.all()
        return [item.inner_text().strip() for item in items]

    def click_menu_item(self, text: str):
        self.driver.page.locator("#menu ul li a", has_text=text).first.click()
