from pages.page_helper import PageHelper
from models.form_data import FormData


class ContactPage:
    def __init__(self, driver):
        self.driver = driver
        self.helper = PageHelper(driver)
        self.name_selector = "#name"
        self.email_selector = "#email"
        self.message_selector = "#message"
        self.submit_selector = "input[type='submit']"

    def open(self, url: str):
        self.helper.open(url)

    def get_title(self) -> str:
        return self.helper.get_title()

    def is_form_available(self) -> bool:
        return self.driver.page.locator(self.name_selector).count() > 0

    def fill_form(self, data: FormData):
        self.driver.element(self.name_selector).fill(data.name)
        self.driver.element(self.email_selector).fill(data.email)
        self.driver.element(self.message_selector).fill(data.message)

    def send(self):
        self.driver.element(self.submit_selector).click()