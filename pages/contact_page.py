class ContactPage:
    def __init__(self, driver):
        self.driver = driver

        self.name = driver.by_css("input[name='name']")
        self.email = driver.by_css("input[name='email']")
        self.message = driver.by_css("textarea[name='message']")
        self.submit = driver.by_css("input[type='submit']")

    def fill_contact_details(self, name: str, email: str, message: str) -> None:
        self.name.fill(name)
        self.email.fill(email)
        self.message.fill(message)

    def send_details(self) -> None:
        self.submit.click()
