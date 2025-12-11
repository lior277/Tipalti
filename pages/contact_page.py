from models.form_data import FormData


class ContactPage:
    def __init__(self, driver):
        self.driver = driver
        self.name_selector = "#name"
        self.email_selector = "#email"
        self.message_selector = "#message"
        self.submit_selector = "input[type='submit']"

    def is_form_available(self) -> bool:
        return self.driver.page.locator(self.name_selector).count() > 0

    def fill_name(self, name: str):
        self.driver.element(self.name_selector).fill(name)

    def fill_email(self, email: str):
        self.driver.element(self.email_selector).fill(email)

    def fill_message(self, message: str):
        self.driver.element(self.message_selector).fill(message)

    def fill_contact_details(self, name: str, email: str, message: str):
        self.fill_name(name)
        self.fill_email(email)
        self.fill_message(message)

    def fill_form(self, data: FormData):
        self.fill_contact_details(data.name, data.email, data.message)

    def send_details(self):
        self.driver.element(self.submit_selector).click()