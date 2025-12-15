from core.ui_driver import UIDriver


class MenuPage:
    def __init__(self, driver: UIDriver):
        self.driver = driver

        self.menu_button = driver.by_css("a[href='#menu']:not(.close)")
        self.menu_links = driver.by_css("#menu ul li a")

    def open_menu(self) -> None:
        self.menu_button.click()

    def get_menu_items(self) -> list[str]:
        return [
            text
            for text in self.menu_links.all_texts()
            if text.lower() != "home"
        ]

    def click_menu_item(self, name: str) -> None:
        self.menu_links.find_by_text(name).click()
        self.driver.page.wait_for_load_state("domcontentloaded")
