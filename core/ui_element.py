from dataclasses import dataclass
from playwright.sync_api import Locator, TimeoutError


@dataclass(frozen=True)
class UIElement:
    locator: Locator
    timeout: int

    # ---------- waits ----------
    def _wait_visible(self) -> None:
        self.locator.wait_for(state="visible", timeout=self.timeout)

    # ---------- actions ----------
    def click(self) -> None:
        self._wait_visible()
        self.locator.scroll_into_view_if_needed()
        self.locator.click()

    def fill(self, value: str) -> None:
        self._wait_visible()
        self.locator.fill(value)

    # ---------- reads ----------
    def text(self) -> str:
        self._wait_visible()
        return self.locator.inner_text().strip()

    def all_texts(self) -> list[str]:
        # Wait until at least one element exists
        self.locator.first.wait_for(state="visible", timeout=self.timeout)
        return [t.strip() for t in self.locator.all_inner_texts()]

    # ---------- chaining ----------
    def find_by_text(self, text: str, *, exact: bool = True) -> "UIElement":
        return UIElement(
            locator=self.locator.get_by_text(text, exact=exact),
            timeout=self.timeout
        )

    # ---------- state ----------
    def is_visible(self) -> bool:
        try:
            self._wait_visible()
            return True
        except TimeoutError:
            return False
