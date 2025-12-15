from dataclasses import dataclass
from playwright.sync_api import Locator, TimeoutError


@dataclass(frozen=True)
class UIElement:
    locator: Locator
    timeout: int = 5000

    def _wait_visible(self) -> None:
        self.locator.wait_for(state="visible", timeout=self.timeout)

    def click(self) -> None:
        self._wait_visible()
        self.locator.scroll_into_view_if_needed()
        self.locator.click()

    def fill(self, value: str) -> None:
        self._wait_visible()
        self.locator.fill(value)

    def text(self) -> str:
        self._wait_visible()
        return self.locator.inner_text().strip()

    def is_visible(self) -> bool:
        try:
            self._wait_visible()
            return True
        except TimeoutError:
            return False
