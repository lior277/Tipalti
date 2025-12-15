from playwright.sync_api import Page

from core.ui_element import UIElement
from config.config_manager import ConfigManager


class UIDriver:
    def __init__(self, page: Page, config: ConfigManager):
        self.page = page
        self.timeout = config.ui_timeout_ms

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

    def by_text(self, text: str, *, exact: bool = True) -> UIElement:
        return UIElement(
            locator=self.page.get_by_text(text, exact=exact),
            timeout=self.timeout
        )

    def by_role(
        self,
        role: str,
        *,
        name: str | None = None,
        exact: bool = True
    ) -> UIElement:
        return UIElement(
            locator=self.page.get_by_role(  # type: ignore[arg-type]
                role,
                name=name,
                exact=exact
            ),
            timeout=self.timeout
        )

    def by_test_id(self, test_id: str) -> UIElement:
        return UIElement(
            locator=self.page.get_by_test_id(test_id),
            timeout=self.timeout
        )
