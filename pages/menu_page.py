from pages.page_helper import PageHelper


class MenuPage:
    def __init__(self, driver):
        self.driver = driver
        self.helper = PageHelper(driver)
        self.menu_btn_selector = "a[href='#menu']:not(.close)"
        self.menu_items_selector = "#menu ul li a"

    def open(self, url: str):
        self.helper.open(url)

    def get_title(self) -> str:
        return self.helper.get_title()

    def open_menu(self):
        self.driver.element(self.menu_btn_selector).click()

    def get_menu_items(self) -> list[str]:
        items = self.driver.page.locator(self.menu_items_selector).all()
        return [item.inner_text().strip() for item in items]

    def click_menu_item(self, text: str):
        self.driver.element_by_text(self.menu_items_selector, text).click()