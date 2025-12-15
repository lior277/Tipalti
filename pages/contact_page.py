from core.ui_driver import UIDriver


class ContactPage:
    def __init__(self, driver: UIDriver):
        self.driver = driver

        self.name_input = driver.by_css("input#name")
        self.email_input = driver.by_css("input#email")
        self.message_input = driver.by_css("textarea#message")

        self.submit_button = driver.by_css("input[type='submit']")

    def fill_contact_details(self, name: str, email: str, message: str) -> None:
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.message_input.fill(message)

    def submit(self) -> None:
        self.submit_button.click()
