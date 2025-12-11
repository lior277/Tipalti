from core.ui_element import UIElement


class UIDriver:
    """SRP: Provides UI actions. No test logic."""
    def __init__(self, page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def element(self, selector: str):
        return UIElement(self.page.locator(selector))
