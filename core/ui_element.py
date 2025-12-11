# core/ui_element.py
from playwright.sync_api import Locator

class UIElement:
    def __init__(self, locator: Locator):
        self.locator = locator

    def click(self):
        self.locator.click()

    def fill(self, value: str):
        self.locator.fill(value)

    def text(self) -> str:
        return self.locator.text_content()

    def all_texts(self):
        return self.locator.all_text_contents()

    def locator_obj(self):
        return self.locator
