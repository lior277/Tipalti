from playwright.sync_api import Page
from core.ui_element import UIElement


class UIDriver:
    def __init__(self, page: Page, timeout: int = 5000):
        self.page = page
        self.timeout = timeout

    # ---------- navigation ----------
    def open(self, url: str) -> None:
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    # ---------- locators ----------
    def by_css(self, selector: str) -> UIElement:
        return UIElement(
            locator=self.page.locator(selector),
            timeout=self.timeout
        )

    def by_css_text(self, selector: str, text: str) -> UIElement:
        return UIElement(
            locator=self.page.locator(selector).get_by_text(text),
            timeout=self.timeout
        )

    def by_text(self, text: str) -> UIElement:
        return UIElement(
            locator=self.page.get_by_text(text),
            timeout=self.timeout
        )

    def by_role(self, role: str, name: str | None = None) -> UIElement:
        return UIElement(
            locator=self.page.get_by_role(role, name=name),
            timeout=self.timeout
        )

    def by_test_id(self, test_id: str) -> UIElement:
        return UIElement(
            locator=self.page.get_by_test_id(test_id),
            timeout=self.timeout
        )
