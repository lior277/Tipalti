from core.ui_element import UIElement


class UIDriver:
    def __init__(self, page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def element(self, selector: str):
        return UIElement(self.page.locator(selector))

    def element_by_text(self, selector: str, text: str):
        return UIElement(self.page.locator(selector, has_text=text).first)