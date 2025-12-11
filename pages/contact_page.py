from core.ui_element import UIElement

class ContactPage:
    def __init__(self, driver):
        self.driver = driver
        self.name_input = driver.element("#name")
        self.email_input = driver.element("#email")
        self.message_input = driver.element("#message")
        self.send_button = driver.element("input[type='submit']")

    def is_form_available(self) -> bool:
        return self.driver.page.locator("#name").count() > 0

    def fill_form(self, name: str, email: str, message: str):
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.message_input.fill(message)

    def send(self):
        self.send_button.click()
